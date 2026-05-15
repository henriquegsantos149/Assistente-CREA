const fs = require('fs');
const PDFParser = require("pdf2json");

function parsePDF(file) {
    return new Promise((resolve, reject) => {
        let pdfParser = new PDFParser(this, 1);
        pdfParser.on("pdfParser_dataError", errData => reject(errData.parserError));
        pdfParser.on("pdfParser_dataReady", pdfData => {
            resolve(pdfParser.getRawTextContent());
        });
        pdfParser.loadPDF(file);
    });
}

async function main() {
    try {
        let text1 = await parsePDF('Comprovante de Registro no CREA.pdf');
        console.log("=== COMPROVANTE ===");
        console.log(text1);

        let text2 = await parsePDF('Ofício nº 09470_2025 - Registro no CREA-RJ.pdf');
        console.log("=== OFICIO ===");
        console.log(text2);

        let text3 = await parsePDF('PPC GGSR.pdf');
        console.log("=== PPC GGSR ===");
        console.log(text3.substring(0, 5000)); // Print just the beginning of PPC to avoid huge output
    } catch(e) {
        console.error(e);
    }
}

main();
