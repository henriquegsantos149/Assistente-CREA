const fs = require('fs');
const pdf = require('pdf-parse');

const file = process.argv[2];
const out = process.argv[3];

pdf(fs.readFileSync(file)).then(data => {
    fs.writeFileSync(out, data.text);
    console.log('PDF extraido para ' + out);
}).catch(console.error);
