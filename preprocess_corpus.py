import fitz  # PyMuPDF   ENSURE YOU DOWNLOAD THIS
import re
import os


output_folder = "PATH TO YOUR DIR"

def extract_tuples_from_pdf(pdf_path):
    
    with fitz.open(pdf_path) as pdf_document:
        file_name, _ = os.path.splitext(pdf_path)
        txt_filename = file_name + ".txt"
        # out_path=out_path + '.txt'
        print("Name ",txt_filename)
        output_file_path = os.path.join(output_folder, txt_filename)

        with open(output_file_path, 'w') as f:
            tuples_list = []
            file_name, _ = os.path.splitext(os.path.basename(pdf_path))

# Replace hyphens with spaces and capitalize the first letter of each word
            book_name = [word.capitalize() for word in file_name.split('-')]
            book_name=1
            print(book_name)       
            # book_name = "Mahatma Gandhi: Collected Works, Volume 1"
            # page_number = 1
            paragraph_number = 0
            sentence_number = 0
            start_offset = 0
            cnt=0
            common_abbreviations = {"Mr.": "Mr*", "Mrs.": "Mrs*", "Dr.": "Dr*", "MR.": "MR*"

    , "Rs.": "Rs*", "St.":"St*", "Ch.":"Ch*" , "Pt.": "Pt*", "Vol.":"Vol*", "VOL.":"VOL*",
    "1.":"1*",
    "2.":"2*",
    "3.":"3*",
    "4.":"4*",
    "5.":"5*",
    "6.":"6*",
    "7.":"7*",
    "8.":"8*",
    "9.":"9*",
    "0.":"0*"}

            
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                page_text = page.get_text("text")
                
                blocks = page.get_text("blocks")
                paragraphs = []
                current_paragraph = []
                
                for block in blocks:
                    block_text = block[4]
                    
                    
                    
                    if block_text.strip():  # Ignore empty blocks
                        # print("New Block ",block_text)
                        for abbreviation, modified_version in common_abbreviations.items():
                            block_text = block_text.replace(abbreviation, modified_version)
                        pattern = r'(?<![A-Z])\b([A-Z])\.(?![A-Z])'

    # Replace the matched period part with "*"
                        result = re.sub(pattern, r'\1*', block_text)
                        paragraphs.append(result)
                        
                    # else:
                    #     print("hi")
                    #     if len(current_paragraph)>=0:
                    #         print(current_paragraph)
                    #         paragraphs.append(" ".join(current_paragraph))
                    #     current_paragraph = []

                
                for paragraph in paragraphs:
                    if not paragraph.strip():  # Skip empty paragraphs
                        continue
                    
                    # Split the paragraph into sentences
                    # print("New Para: ",paragraph, file = f)
                    sentences = re.split(r'(?<=[.!?])\s+', paragraph)

                    
                    
                    # Process each sentence
                    for sentence in sentences:
                        sentence = sentence.strip()
                        # if cnt ==1:
                        sentence = re.sub(r'-', ' ', sentence)
                        sentence = re.sub(r'\n', ' ', sentence)
                        sentence = re.sub(r'\s{2,}', ' ', sentence)
                        sentence = re.sub(r'[^\x00-\x7F]+', '', sentence)
                        sentence = re.sub(r'\s+', ' ', sentence)
                        sentence = re.sub(r'^\s+', '', sentence)


                        if len(sentence) < 7:
                            continue  # Ignore short sentences
                        sentence_number += 1
                        pattern = r'(?<![A-Z])\b([A-Z])\*(?![A-Z])'

                        sentence = re.sub(pattern, r'\1.', sentence)
                        for abbreviation, modified_version in common_abbreviations.items():
                            sentence = sentence.replace(modified_version, abbreviation)
                        

                        tuples_list.append((book_name, page_num, paragraph_number, sentence_number, start_offset))
                        start_offset += len(sentence) + 1  # Update start offset for the next sentence
                        print(tuples_list[cnt], sentence, file=f)

                        cnt+=1
                    
                    paragraph_number += 1
                
                # Reset sentence and paragraph counters for the next page
                sentence_number = 0
                paragraph_number = 0
                
            return tuples_list

# PDF file path
pdf_path = 'mahatma-gandhi-collected-works-volume-1.pdf'
# Extract tuples from the PDF
extracted_tuples = extract_tuples_from_pdf(pdf_path)

