import os
import fitz  # PyMuPDF
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, redirect, url_for
from transformers import BertTokenizer, BertModel
import torch

app = Flask(__name__)
UPLOADS_DIR = "static/uploads"

# Preprocessing function
def preprocess_text(text):
    text = text.replace("\r", " ").replace("\n", " ").strip()
    text = re.sub(r"\s{2,}", " ", text)
    return text

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to get BERT embeddings for a sentence
def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)  # Use mean of all tokens

# Function to calculate similarity using BERT embeddings
def calculate_similarity_bert(text1, text2):
    embeddings1 = get_bert_embeddings(text1)
    embeddings2 = get_bert_embeddings(text2)
    similarity = torch.cosine_similarity(embeddings1, embeddings2)
    return similarity.item()

# Extract Q&A pairs from PDF
def extract_qa_pairs(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()

        # Preprocess the text
        text = preprocess_text(text)

        # Regex for Q&A pairs (Assumes questions are numbered, for example "1. Question")
        qa_pairs = [
            (match.split(".", 1)[0] + ".", match.split(".", 1)[1].strip()) 
            for match in re.findall(r"(\d+\.\s.*?)(?=(?:\d+\.\s)|\Z)", text, re.DOTALL)
            if "." in match
        ]

        return qa_pairs
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return []

# Calculate overall similarity between teacher and student answers
def calculate_similarity(teacher_qa_pairs, student_qa_pairs):
    teacher_answers = [answer for _, answer in teacher_qa_pairs]
    student_answers = [answer for _, answer in student_qa_pairs]

    min_length = min(len(teacher_answers), len(student_answers))
    teacher_answers = teacher_answers[:min_length]
    student_answers = student_answers[:min_length]

    if not teacher_answers or not student_answers:
        return 0.0, []

    similarities = []
    for i in range(min_length):
        # Compare teacher question and student answer for relevance
        question_similarity = calculate_similarity_bert(teacher_qa_pairs[i][0], student_qa_pairs[i][0])
        
        # Only consider the answers if the question similarity is above a certain threshold
        if question_similarity > 0.7:  # Adjust the threshold as needed
            answer_similarity = calculate_similarity_bert(teacher_answers[i], student_answers[i])
            similarities.append((teacher_answers[i], student_answers[i], answer_similarity))

    if not similarities:
        return 0.0, []

    # Calculate the average similarity score
    overall_similarity = sum([sim[2] for sim in similarities]) / len(similarities) * 100
    return overall_similarity, similarities

# Route for results page
@app.route("/")
def results():
    teacher_files = [f for f in os.listdir(UPLOADS_DIR) if f.startswith("teacher_")]
    student_files = [f for f in os.listdir(UPLOADS_DIR) if f.startswith("student_")]

    results_data = []

    for teacher_file in teacher_files:
        # Extract subject and assignment number from teacher file name
        subject, assignment_number = teacher_file.split("_")[1], teacher_file.split("_")[2].split(".")[0]
        teacher_qa_pairs = extract_qa_pairs(os.path.join(UPLOADS_DIR, teacher_file))

        # Find corresponding student files
        subject_students = [f for f in student_files if f.endswith(f"_{subject}_{assignment_number}.pdf")]

        for student_file in subject_students:
            student_name = student_file.split("_")[1]  # Extract student name
            student_qa_pairs = extract_qa_pairs(os.path.join(UPLOADS_DIR, student_file))

            similarity_score, _ = calculate_similarity(teacher_qa_pairs, student_qa_pairs)
            results_data.append({
                "student_name": student_name, 
                "subject": subject, 
                "assignment_number": assignment_number,
                "score": round(similarity_score, 2), 
                "file": student_file
            })

    return render_template("results.html", results=results_data)

# Route for comparison page
@app.route("/compare/<student_file>")
def compare(student_file):
    subject = student_file.split("_")[2]
    assignment_number = student_file.split("_")[3].split(".")[0]
    teacher_file = f"teacher_{subject}_{assignment_number}.pdf"
    
    teacher_qa_pairs = extract_qa_pairs(os.path.join(UPLOADS_DIR, teacher_file))
    student_qa_pairs = extract_qa_pairs(os.path.join(UPLOADS_DIR, student_file))

    _, comparisons = calculate_similarity(teacher_qa_pairs, student_qa_pairs)

    return render_template("comparison.html", subject=subject, assignment_number=assignment_number, comparisons=comparisons)

if __name__ == "__main__":
    app.run(port=5001)
