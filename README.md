# Plagiarism Detection Tool

This is a GUI-based Python application for detecting potential plagiarism using N-gram matching and Trie-based lookup.

## Features

- Load `.txt` files from a specified directory.
- Tokenizes, removes stopwords, and lemmatizes text using NLTK.
- Computes similarity based on N-gram overlap (default: trigrams).
- Displays detailed plagiarism report including Longest Common Substring (LCS).
- Saves submitted input text with timestamps.

## Requirements

- Python 3.6+
- `nltk`
- `tkinter` (usually included with Python)
- Internet connection for first-time NLTK corpus download

## Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/plagiarism-detector.git
    cd plagiarism-detector
    ```

2. Install dependencies:
    ```bash
    pip install nltk
    ```

3. Download required NLTK corpora (run once):
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    ```

4. Set up your text data:
    - Place `.txt` documents for comparison in a directory.
    - Update the `folder_path` in `updatedChecker.py`:
      ```python
      folder_path = '/path/to/your/txt_files'
      ```

## Usage

Simply run the script:

```bash
python updatedChecker.py
```
Paste your text into the window and click Submit. A report will appear showing matching documents and longest matching phrases.

## Notes

- The default similarity threshold is 0.1.

- The tool currently supports only .txt files.

- Input texts are saved to the same folder for record-keeping.
