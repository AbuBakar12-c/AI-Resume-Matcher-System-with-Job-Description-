🚀 AI Resume Matcher System With Job Descriptions

An intelligent AI-powered system that matches resumes with job descriptions using Natural Language Processing (NLP)
and Cosine Similarity to help recruiters find the best candidates efficiently.

📌 Features

✔️ Extracts text from PDF, DOCX, and TXT resumes

✔️ Uses TF-IDF Vectorization & Cosine Similarity for matching

✔️ Supports multiple resume uploads

✔️ Filters and ranks resumes based on similarity score

✔️ Simple web interface for job description input

📝 Introduction

The AI Resume Matcher System is designed to streamline the hiring process by automatically analyzing resumes and ranking them based on relevance to a given job description.
Instead of manually reviewing hundreds of resumes, recruiters can use this system to quickly identify the best candidates.
The tool utilizes NLP techniques to extract and process resume content, applying Cosine Similarity to determine the most relevant matches.

⚙️ How It Works

1️⃣ Upload Resumes: The user uploads multiple resumes in PDF, DOCX, or TXT format.

2️⃣ Text Extraction: The system extracts text from each resume using PyPDF2 and docx2txt.

3️⃣ Job Description Processing: The job description provided by the recruiter is vectorized using TF-IDF (Term Frequency-Inverse Document Frequency).

4️⃣ Similarity Matching: The cosine similarity algorithm compares resumes with the job description and assigns a match score.

5️⃣ Displaying Results: The system ranks and displays the top-matching resumes with a similarity score above a certain threshold (e.g., 30%).

🔧 Installation & Setup

# Create a virtual environment (optional but recommended)

python -m venv venv

venv\Scripts\activate  

# Install dependencies

pip install -r requirements.txt

# Run the application it is better

python main.py
