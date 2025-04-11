# Answer_Grading_System
# 📝 Automated Subjective Answer Grading Platform

An intelligent web-based platform to automatically grade students’ subjective answers by comparing them with a model solution provided by the teacher. The system uses **BERT-based NLP** techniques to understand context, accuracy, and relevance, helping educators save time and maintain consistency in evaluation.

---

## 🚀 Features

- 🔍 **BERT-powered similarity check** between student answers and ideal solutions
- 📊 **Score generation** based on semantic understanding, not just keyword matching
- 📁 **Teacher interface** for uploading questions and reference answers
- 🧠 **ML backend** using `sklearn`, `transformers`, and fine-tuned models
- 🌐 Web interface built with **HTML, CSS, JavaScript, and Flask**

---

## 🛠️ Tech Stack

| Category         | Technologies                         |
|------------------|--------------------------------------|
| Frontend         | HTML, CSS, JavaScript                |
| Backend          | Python, Flask                        |
| NLP Model        | BERT (via HuggingFace Transformers)  |
| ML Algorithms    | Sklearn, Sentence Embedding          |
| Hosting / APIs   | Flask Local Server                   |

---

## 📂 Project Structure

```bash
Answer_Grading_System/
├── static/                  # CSS and JS files
├── templates/               # HTML templates (Jinja)
├── app.py                   # Flask backend
├── test.py         # BERT-based scoring logic
└── README.md

---


⚙️ Installation
Clone the repository and install the requirements:

bash
git clone https://github.com/Nikita-Chavan001/Answer_Grading_System.git
cd Answer_Grading_System

---

▶️ Run the Application
bash
python app.py
Visit http://localhost:5000 in your browser to use the platform.

---

🤖 Model Logic
Converts both student and reference answers into embeddings using BERT

Calculates cosine similarity & other distance metrics

Applies basic NLP cleaning and normalization before scoring

Can be extended with grammar and fluency checks for richer evaluation

---

📌 Future Enhancements

📈 Analytics dashboard for performance tracking

📝 Feedback suggestions for low-scoring answers

🌍 Multilingual answer grading (future scope)

---
🙋‍♀️ Author
Nikita Balu Chavan




