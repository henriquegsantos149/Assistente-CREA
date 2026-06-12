import fs from 'fs';
import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf.mjs';

const filePath = process.argv[2];
const outPath = process.argv[3];

async function extract() {
    const data = new Uint8Array(fs.readFileSync(filePath));
    const loadingTask = pdfjsLib.getDocument({data: data});
    const pdf = await loadingTask.promise;
    
    let fullText = "";
    for(let i = 1; i <= pdf.numPages; i++) {
        if(i % 100 === 0) console.log(`Extraindo página ${i}/${pdf.numPages}...`);
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent();
        const pageText = textContent.items.map(item => item.str).join(' ');
        fullText += pageText + "\n\n";
    }
    
    fs.writeFileSync(outPath, fullText);
    console.log('PDF extraído!');
}

extract().catch(console.error);
