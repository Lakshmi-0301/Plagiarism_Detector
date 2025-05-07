import os
import tkinter as tk
from tkinter import scrolledtext
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from datetime import datetime


class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, n_gram: tuple):
        node = self.root
        for token in n_gram:
            if token not in node.children:
                node.children[token] = TrieNode()
            node = node.children[token]
            node.count += 1

    def search(self, n_gram: tuple) -> int:
        node = self.root
        for token in n_gram:
            if token not in node.children:
                return 0
            node = node.children[token]
        return node.count


def load_text_files_from_folder(folder_path: str) -> dict:
    text_files_content = {}

    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return text_files_content

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    text_files_content[filename] = content
            except Exception as e:
                print(f"Error reading file '{filename}': {e}")

    return text_files_content


def preprocess_text(text: str, remove_stop: bool = True) -> list:
    tokens = tokenize(text)
    if remove_stop:
        tokens = remove_stopwords(tokens)
    lemmatized_tokens = lemmatize(tokens)
    return lemmatized_tokens


def tokenize(text: str) -> list:
    return word_tokenize(text)


def remove_stopwords(tokens: list) -> list:
    stop_words = set(stopwords.words('english'))
    return [token for token in tokens if token.lower() not in stop_words]


def lemmatize(tokens: list) -> list:
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def generate_n_grams(tokens: list, n: int) -> list:
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def check_plagiarism(input_text: str, loaded_files: dict, n: int = 3, threshold: float = 0.5) -> dict:
    input_tokens = preprocess_text(input_text, remove_stop=False) 
    input_n_grams = generate_n_grams(input_tokens, n)
    input_n_gram_count = len(input_n_grams)

    results = {}

    for filename, content in loaded_files.items():
        file_tokens = preprocess_text(content, remove_stop=False)
        file_n_grams = generate_n_grams(file_tokens, n)

        trie = Trie()
        for n_gram in file_n_grams:
            trie.insert(n_gram)

        intersection_count = 0
        for n_gram in input_n_grams:
            if trie.search(n_gram) > 0:
                intersection_count += 1

        similarity_ratio = intersection_count / input_n_gram_count if input_n_gram_count > 0 else 0

        if similarity_ratio >= threshold:
            results[filename] = similarity_ratio

    return results


def longest_common_substring(doc1: str, doc2: str) -> str:
    m, n = len(doc1), len(doc2)
    lcs_matrix = [[0] * (n + 1) for _ in range(m + 1)]
    lcs_length, lcs_end = 0, 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if doc1[i - 1] == doc2[j - 1]:
                lcs_matrix[i][j] = lcs_matrix[i - 1][j - 1] + 1
                if lcs_matrix[i][j] > lcs_length:
                    lcs_length = lcs_matrix[i][j]
                    lcs_end = i
            else:
                lcs_matrix[i][j] = 0

    return doc1[lcs_end - lcs_length:lcs_end] if lcs_length > 0 else ""


def generate_report(plagiarism_results: dict, input_text: str, loaded_files: dict) -> str:
    report = ""
    if plagiarism_results:
        for filename, ratio in plagiarism_results.items():
            report += f"Potential plagiarism detected in '{filename}' with similarity ratio: {ratio:.4f}\n"
            file_content = loaded_files[filename]
            lcs = longest_common_substring(input_text, file_content)
            report += f"Longest Common Substring: '{lcs}'\n\n"
    else:
        report = "No plagiarism detected."
    return report


def display_report(report: str) -> None:
    window = tk.Tk()
    window.title("Plagiarism Detection Report")

    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10)

    text_area.insert(tk.END, report)
    text_area.configure(state='disabled')

    window.mainloop()


def save_input_text(input_text: str, folder_path: str) -> None:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"submitted_text_{timestamp}.txt"
    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(input_text)

    print(f"Input text saved to '{file_path}'")


def submit_content():
    content = text_area.get("1.0", tk.END).strip()
    plagiarism_results = check_plagiarism(content, loaded_files, n=3, threshold=0.1)

    report = generate_report(plagiarism_results, content, loaded_files)
    display_report(report)

    save_input_text(content, folder_path)


app = tk.Tk()
app.title("Plagiarism Detector Input")

label = tk.Label(app, text="Enter your text content below:")
label.pack(pady=10)

text_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=50, height=15)
text_area.pack(padx=10, pady=10)

submit_button = tk.Button(app, text="Submit", command=submit_content)
submit_button.pack(pady=10)

folder_path = os.path.join(os.getcwd(), 'data')
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
loaded_files = load_text_files_from_folder(folder_path)

app.mainloop()
