import PyPDF2
import sys

def extract(pdf_path, txt_path):
    print(f"Extraindo {pdf_path}...")
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for i, page in enumerate(reader.pages):
            text += page.extract_text() or ""
            if i % 100 == 0:
                print(f"Página {i}/{len(reader.pages)}")
                
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Concluído!")

if __name__ == '__main__':
    extract(sys.argv[1], sys.argv[2])
