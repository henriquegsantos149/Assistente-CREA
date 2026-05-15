const fs = require('fs');
const pdf = require('pdf-parse');

async function extractText(filename) {
    console.log(`\n\n=== EXTRATCTING ${filename} ===\n`);
    try {
        let dataBuffer = fs.readFileSync(filename);
        let data = await pdf(dataBuffer);
        console.log(data.text);
    } catch (e) {
        console.error("Error extracting", filename, e);
    }
}

async function main() {
    await extractText('Comprovante de Registro no CREA.pdf');
    await extractText('Ofício nº 09470_2025 - Registro no CREA-RJ.pdf');
    await extractText('PPC GGSR.pdf');
}

main();
