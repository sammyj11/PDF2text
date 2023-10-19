import fitz  # PyMuPDF
import re


def extract_tuples_from_pdf(pdf_path):
    # Open the PDF file
    with fitz.open(pdf_path) as pdf_document:
        with open('output.txt', 'w') as f:
            # Initialize variables to store the extracted tuples
            tuples_list = []
            book_name = "Mahatma Gandhi: Collected Works, Volume 1"
            # page_number = 1
            paragraph_number = 0
            sentence_number = 0
            start_offset = 0
            cnt=0
            common_abbreviations = {"Mr.": "Mr*", "Mrs.": "Mrs*", "Dr.": "Dr*", "MR.": "MR*"

    , "Rs.": "Rs*", "St.":"St*", "Ch.":"Ch*" , "Pt.": "Pt*",
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

            
            # Loop through each page in the PDF
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                page_text = page.get_text("text")
                
                
                # Split the page text into paragraphs
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

                
                # Process each paragraph
                for paragraph in paragraphs:
                    if not paragraph.strip():  # Skip empty paragraphs
                        continue
                    
                    # Split the paragraph into sentences
                    
                        # print('freeCodeCamp', file=f)
                    print("New Para: ",paragraph, file = f)
                    sentences = re.split(r'(?<=[.!?])\s+', paragraph)

                    
                    
                    # Process each sentence
                    for sentence in sentences:
                        sentence = sentence.strip()
                        # if cnt ==1:
                        sentence = re.sub(r'\n', ' ', sentence)
                        sentence = re.sub(r'\s{2,}', ' ', sentence)


                        if len(sentence) < 7:
                            continue  # Ignore short sentences
                        sentence_number += 1
                        pattern = r'(?<![A-Z])\b([A-Z])\*(?![A-Z])'

    # Replace the matched period part with "*"
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

# Print the extracted tuples
# for idx, tup in enumerate(extracted_tuples):
#     print(f"Tuple {idx + 1}: {tup}")


import fitz  # PyMuPDF
import re

def find_part_in_pdf(pdf_path, target_tuple):
    # Open the PDF file
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            page_text = page.get_text("text")

            # Split the page text into paragraphs
            paragraphs = re.split(r'(?<=[.!?])\n', page_text)

            for paragraph_number, paragraph in enumerate(paragraphs, start=1):
                # Split the paragraph into sentences
                sentences = re.split(r'(?<=[.!?]) +', paragraph)

                for sentence_number, sentence in enumerate(sentences, start=1):
                    if len(sentence) < 7:
                        continue  # Ignore short sentences
                    if (page_num, paragraph_number, sentence_number) == (target_tuple[1], target_tuple[2], target_tuple[3]):
                        # Found the matching part in the PDF
                        return {
                            "Page Number": target_tuple[1],
                            "Paragraph Number": paragraph_number,
                            "Sentence Number": sentence_number,
                            "Text": sentence
                        }
    return None

# PDF file path
pdf_path = 'mahatma-gandhi-collected-works-volume-1.pdf'

# Target tuple to find
target_tuple = ('Mahatma Gandhi: Collected Works, Volume 1', 473, 3, 14, 1092768)

# Find the part in the PDF corresponding to the target tuple
result = find_part_in_pdf(pdf_path, target_tuple)

if result:
    print(f"Found matching part in the PDF:")
    print(f"Page Number: {result['Page Number']}")
    print(f"Paragraph Number: {result['Paragraph Number']}")
    print(f"Sentence Number: {result['Sentence Number']}")
    print(f"Text: {result['Text']}")
else:
    print("Target tuple not found in the PDF.")
