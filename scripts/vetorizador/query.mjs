import { pipeline } from '@huggingface/transformers';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
dotenv.config({ path: path.join(__dirname, '../../.env') });

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error(JSON.stringify({ error: "Missing Supabase credentials." }));
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);
const query = process.argv[2];
const rpcFunction = process.argv[3] || 'match_documentos_crea';

if (!query) {
    console.error(JSON.stringify({ error: "No query provided." }));
    process.exit(1);
}

async function main() {
    // Esconde os logs verbosos do Transformers.js
    const generateEmbedding = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2', {
        progress_callback: null
    });

    const output = await generateEmbedding(query, { pooling: 'mean', normalize: true });
    const embedding = Array.from(output.data);

    const { data, error } = await supabase.rpc(rpcFunction, {
        query_embedding: embedding,
        match_threshold: 0.2, // Limite de similaridade
        match_count: 5 // Traz os 5 blocos mais relevantes
    });

    if (error) {
        console.error(JSON.stringify({ error: error.message }));
        process.exit(1);
    }

    // Retorna apenas a string JSON na saída padrão
    console.log(JSON.stringify(data));
}

main().catch(e => { 
    console.error(JSON.stringify({ error: e.toString() })); 
    process.exit(1); 
});
