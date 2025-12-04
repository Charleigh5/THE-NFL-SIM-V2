import pdfplumber

pdf_path = r'c:\Users\cweir\Documents\GitHub\THE NFL SIM\docs\references\Football_Data_Reconstruction.pdf'
output_path = r'c:\Users\cweir\Documents\GitHub\THE NFL SIM\football_data_extracted.txt'

with pdfplumber.open(pdf_path) as pdf:
    text = '\n'.join([page.extract_text() for page in pdf.pages])

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Extracted {len(text)} characters to {output_path}")
