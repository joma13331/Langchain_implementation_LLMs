import re
import nltk
import requests
from bs4 import BeautifulSoup



def remove_reference_tags(content):
    # Remove reference tags enclosed in square brackets [4], [5], etc.
    content = re.sub(r'\[\d+\]', '', content)
    
    return content

def separate_sentences(text, output_file_path):
  
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    
    # Save each separated sentence to a new text file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for sentence in sentences:
            sentence = remove_reference_tags(sentence)
            sentence = sentence.strip()  # Remove leading/trailing whitespaces
            
            if sentence:  # Check if the sentence is not empty
                output_file.write(sentence + '\n')

def scrape_wikipedia_page(url):
    # Send a GET request to the Wikipedia page
    response = requests.get(url)
    
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all paragraph elements
    paragraphs = soup.find_all('p')
    
    # Extract the text from the paragraphs
    text = '\n'.join([p.get_text() for p in paragraphs])
    
    # Save the text to a file
    return text

# Example usage
wikipedia_url = 'https://www.theguardian.com/environment/2023/jun/08/the-planets-economist-has-kate-raworth-found-a-model-for-sustainable-living?utm_source=pocket-newtab-intl-en'
output_file_path = './Docs/The planet’s economist.txt'
text = scrape_wikipedia_page(wikipedia_url)
separate_sentences(text=text, output_file_path=output_file_path)