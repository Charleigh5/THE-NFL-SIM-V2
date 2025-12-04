import pypdf
import sys

pdf_path = r'c:\Users\cweir\Documents\GitHub\THE NFL SIM\docs\references\Football_Data_Reconstruction.pdf'

try:
    reader = pypdf.PdfReader(pdf_path)

    print(f"=== PDF METADATA ===")
    print(f"Number of pages: {len(reader.pages)}")

    if reader.metadata:
        print(f"\nMetadata:")
        for key, value in reader.metadata.items():
            print(f"  {key}: {value}")

    print(f"\n=== PAGE ANALYSIS ===")
    for i, page in enumerate(reader.pages[:3]):  # Check first 3 pages
        print(f"\nPage {i+1}:")
        print(f"  MediaBox: {page.mediabox}")
        print(f"  CropBox: {page.cropbox if hasattr(page, 'cropbox') else 'N/A'}")

        # Check for images
        if '/XObject' in page['/Resources']:
            xobjects = page['/Resources']['/XObject'].get_object()
            print(f"  Number of XObjects (likely images): {len(xobjects)}")
            for key in list(xobjects.keys())[:3]:  # Show first 3
                print(f"    - {key}")

        # Try to get text one more time
        text = page.extract_text()
        print(f"  Text length: {len(text)}")
        if text and text.strip():
            print(f"  Sample text: {text[:200]}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
