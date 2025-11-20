import pdfplumber
import json
import os
import re

PDF_FOLDER_PATH = 'data/calls'
JSON_OUTPUT_PATH = 'data/extracted_text.json'

def main():
    if os.path.exists(JSON_OUTPUT_PATH):
        print('extracted_text exists')
        with open('data/extracted_text.json', 'r', encoding='utf-8') as f:
            all_transcripts = json.load(f)
    else:
        print('Extracting Text')
        extract_text_from_pdfs(PDF_FOLDER_PATH, JSON_OUTPUT_PATH)
        with open('data/extracted_text.json', 'r', encoding='utf-8') as f:
            all_transcripts = json.load(f)

def extract_text_from_pdfs(pdf_folder_path, output_json_path):
    
    all_transcripts = []

    
    for filename in os.listdir(pdf_folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, filename)
            print(f"Processing: {filename}...")

    
            transcript_data = {
                "file_name": filename,
                "quarter": "Unknown", # You can automate this later with Regex
                "full_text": "",
                "pages": [] # We keep per-page text just in case you need to debug
            }

            # 3. Extract text using pdfplumber
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    full_text_list = []
                    
                    for page in pdf.pages:
                        # Extract text from the page
                        text = page.extract_text()
                        
                        if text:
                            # Optional: Basic cleaning to remove page numbers like "Page 1 of 18"
                            # This regex looks for "Page X of Y" patterns often found in footers
                            clean_text = re.sub(r'Page \d+ of \d+', '', text)
                            
                            transcript_data["pages"].append(clean_text)
                            full_text_list.append(clean_text)
                    
                    # Join all pages into one massive string for NLP analysis
                    transcript_data["full_text"] = "\n".join(full_text_list)
                    
                    # 4. Attempt to extract Quarter from filename (Simple logic)
                    # Assumes filename format like "2023-24Q1.pdf"
                    if "Q1" in filename: transcript_data["quarter"] = "Q1"
                    elif "Q2" in filename: transcript_data["quarter"] = "Q2"
                    elif "Q3" in filename: transcript_data["quarter"] = "Q3"
                    elif "Q4" in filename: transcript_data["quarter"] = "Q4"

                    all_transcripts.append(transcript_data)

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # 5. Save everything to a single JSON file
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_transcripts, f, indent=4, ensure_ascii=False)

    print(f"\nSuccess! Extracted {len(all_transcripts)} transcripts to {output_json_path}")


if __name__=="__main__":
# The program starts
    main()
