import pypdf

pdf_path = r'c:\Users\cweir\Documents\GitHub\THE NFL SIM\docs\references\Football_Data_Reconstruction.pdf'
output_path = r'c:\Users\cweir\Documents\GitHub\THE NFL SIM\football_data_extracted.txt'

try:
    reader = pypdf.PdfReader(pdf_path)
    print(f"PDF has {len(reader.pages)} pages")

    text = ""
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        print(f"Page {i+1}: {len(page_text)} characters")
        text += f"\n\n=== PAGE {i+1} ===\n\n"
        text += page_text

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"\nTotal extracted: {len(text)} characters")
    print(f"Output saved to: {output_path}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
