import { pipeline } from '@huggingface/transformers';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
dotenv.config({ path: path.join(__dirname, '../../.env') });

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error("Missing Supabase credentials.");
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function extractText(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    if (ext === '.pdf') {
        console.log(`Lendo PDF: ${filePath}`);
        const dataBuffer = fs.readFileSync(filePath);
        const mod = await import('pdf-parse');
        const pdfParse = mod.default || mod;
        const data = await pdfParse(dataBuffer);
        return data.text;
    } else if (ext === '.md' || ext === '.txt') {
        console.log(`Lendo Texto: ${filePath}`);
        return fs.readFileSync(filePath, 'utf8');
    } else {
        throw new Error(`Extensão não suportada: ${ext}`);
    }
}

function chunkText(text, maxWords = 180) {
    const paragraphs = text.split('\n\n');
    const chunks = [];
    let currentChunk = '';
    let currentWords = 0;

    for (const p of paragraphs) {
        const words = p.split(/\s+/).length;
        if (currentWords + words > maxWords && currentChunk) {
            chunks.push(currentChunk.trim());
            currentChunk = '';
            currentWords = 0;
        }
        currentChunk += p + '\n\n';
        currentWords += words;
    }
    if (currentChunk.trim()) {
        chunks.push(currentChunk.trim());
    }
    return chunks.filter(c => c.length > 20); // Ignora chunks muito curtos
}

async function main() {
    const args = process.argv.slice(2);
    if (args.length < 2) {
        console.log("Uso: node ingest_local.mjs <caminho_do_arquivo> <nome_da_tabela>");
        console.log("Ex: node ingest_local.mjs ../../QGIS.pdf documentos_cursos");
        process.exit(1);
    }

    const filePath = path.resolve(args[0]);
    const tableName = args[1];
    const fileName = path.basename(filePath);

    if (!fs.existsSync(filePath)) {
        console.error(`Arquivo não encontrado: ${filePath}`);
        process.exit(1);
    }

    const text = await extractText(filePath);
    if (!text || text.trim().length === 0) {
        console.error("Nenhum texto extraído do arquivo.");
        process.exit(1);
    }

    const chunks = chunkText(text, 180);
    console.log(`Texto extraído e dividido em ${chunks.length} chunks.`);

    console.log("Carregando modelo de embeddings localmente (Xenova/all-MiniLM-L6-v2)...");
    const generateEmbedding = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2', {
        progress_callback: null
    });

    console.log("Iniciando vetorização e inserção no banco de dados...");
    
    // Processar em lotes de 10 para não estourar a memória
    const batchSize = 10;
    for (let i = 0; i < chunks.length; i += batchSize) {
        const batchChunks = chunks.slice(i, i + batchSize);
        console.log(`Processando lote ${Math.floor(i/batchSize) + 1} de ${Math.ceil(chunks.length/batchSize)} (Chunks ${i} a ${i + batchChunks.length - 1})`);
        
        const rows = [];
        for (let j = 0; j < batchChunks.length; j++) {
            const chunk = batchChunks[j];
            const output = await generateEmbedding(chunk, { pooling: 'mean', normalize: true });
            const embedding = Array.from(output.data);
            
            rows.push({
                id: Date.now() + Math.floor(Math.random() * 1000000) + j,
                content: chunk,
                metadata: { file: fileName, chunk_index: i + j },
                embedding: embedding
            });
        }
        
        const { error } = await supabase.from(tableName).insert(rows);
        if (error) {
            console.error(`Erro ao inserir no Supabase no lote ${Math.floor(i/batchSize) + 1}:`, error.message);
        }
    }

    console.log("✅ Ingestão finalizada com sucesso!");
}

main().catch(e => {
    console.error("Erro fatal:", e);
    process.exit(1);
});
