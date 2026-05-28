import fs from 'fs';
import path from 'path';
import { pipeline } from '@huggingface/transformers';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import pdf from 'pdf-parse';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.join(__dirname, '../../.env') });

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error("ERRO: SUPABASE_URL ou SUPABASE_KEY não encontrados no arquivo .env");
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

function chunkText(text, maxWords = 150) {
    const paragraphs = text.split(/\n\s*\n/);
    const chunks = [];
    let currentChunk = "";
    let currentWords = 0;

    for (const p of paragraphs) {
        const words = p.split(/\s+/).length;
        if (currentWords + words > maxWords && currentChunk.length > 0) {
            chunks.push(currentChunk.trim());
            currentChunk = "";
            currentWords = 0;
        }
        currentChunk += p + "\n\n";
        currentWords += words;
    }
    if (currentChunk.trim()) {
        chunks.push(currentChunk.trim());
    }
    return chunks;
}

async function main() {
    const args = process.argv.slice(2);
    if (args.length < 2) {
        console.error("Uso: node processar_pdf.mjs <caminho_do_pdf> <tabela_destino>");
        process.exit(1);
    }

    const pdfPath = args[0];
    const tableName = args[1];

    if (!fs.existsSync(pdfPath)) {
        console.error(`ERRO: Arquivo não encontrado: ${pdfPath}`);
        process.exit(1);
    }

    console.log(`📥 Extraindo texto do PDF: ${path.basename(pdfPath)}`);
    const dataBuffer = fs.readFileSync(pdfPath);
    const data = await pdf(dataBuffer);
    const textContent = data.text;

    if (!textContent || textContent.trim().length === 0) {
        console.error("ERRO: Nenhum texto encontrado no PDF.");
        process.exit(1);
    }

    console.log("📥 Carregando modelo de IA (Xenova/all-MiniLM-L6-v2)...");
    const generateEmbedding = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');

    const chunks = chunkText(textContent, 180);
    console.log(`📄 Texto dividido em ${chunks.length} partes. Iniciando vetorização para tabela '${tableName}'...`);

    for (let i = 0; i < chunks.length; i++) {
        const chunk = chunks[i];
        if (!chunk.trim()) continue;

        // Gera o vetor semântico
        const output = await generateEmbedding(chunk, { pooling: 'mean', normalize: true });
        const embedding = Array.from(output.data);

        // Insere no banco
        const { error } = await supabase.from(tableName).insert({
            content: chunk,
            metadata: { file: path.basename(pdfPath), chunk_index: i },
            embedding: embedding
        });

        if (error) {
            console.error(`❌ Erro ao inserir bloco ${i+1}:`, error.message);
        }
    }
    console.log(`✅ Sucesso! Arquivo processado e salvo na tabela ${tableName}.`);
}

main().catch(console.error);
