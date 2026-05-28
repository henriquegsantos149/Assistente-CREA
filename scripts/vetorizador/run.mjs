import fs from 'fs';
import path from 'path';
import { pipeline } from '@huggingface/transformers';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';

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
    console.log("📥 Baixando e carregando modelo de IA (Xenova/all-MiniLM-L6-v2) - isso pode demorar na 1ª vez...");
    const generateEmbedding = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');

    const docDir = path.join(__dirname, '../../Documentos');
    const files = fs.readdirSync(docDir).filter(f => f.endsWith('.md'));

    console.log(`📄 Encontrados ${files.length} arquivos MD. Iniciando vetorização...`);

    for (const file of files) {
        console.log(`⏳ Processando: ${file}...`);
        const content = fs.readFileSync(path.join(docDir, file), 'utf-8');
        const chunks = chunkText(content, 180); // Cerca de 180 palavras por bloco

        for (let i = 0; i < chunks.length; i++) {
            const chunk = chunks[i];
            // Gera o vetor semântico
            const output = await generateEmbedding(chunk, { pooling: 'mean', normalize: true });
            const embedding = Array.from(output.data);

            // Insere no banco
            const { error } = await supabase.from('documentos_crea').insert({
                content: chunk,
                metadata: { file: file, chunk_index: i },
                embedding: embedding
            });

            if (error) {
                console.error(`❌ Erro ao inserir chunk de ${file}:`, error.message);
            }
        }
        console.log(`✅ ${file} (${chunks.length} partes) processado e enviado!`);
    }
    console.log("🎉 Vetorização concluída com sucesso no Supabase!");
}

main().catch(console.error);
