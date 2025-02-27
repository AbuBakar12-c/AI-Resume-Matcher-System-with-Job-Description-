from flask import Flask, request, render_template, redirect, url_for
import os
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Function to extract text from PDF files
def extract_text_from_pdf(file_path):
    try:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Function to extract text from DOCX files
def extract_text_from_docx(file_path):
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

# Function to extract text from TXT files
def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error extracting text from TXT: {e}")
        return ""

# Main function to extract text based on file type
def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        print(f"Unsupported file format: {file_path}")
        return ""

@app.route("/")
def index():
    return render_template('matchresume.html')

@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form.get('job_description')
        resume_files = request.files.getlist('resumes')

        # Validate input
        if not job_description:
            return render_template('matchresume.html', message="Please provide a job description.")
        if not resume_files:
            return render_template('matchresume.html', message="Please upload at least one resume.")

        resumes = []
        filenames = []

        # Process uploaded resumes
        for resume_file in resume_files:
            if resume_file.filename.endswith(('.pdf', '.docx', '.txt')):
                # Save the file
                filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
                resume_file.save(filename)

                # Extract text
                text = extract_text(filename)
                if text.strip():
                    resumes.append(text)
                    filenames.append(resume_file.filename)
                else:
                    print(f"No text extracted from file: {resume_file.filename}")
            else:
                return render_template('matchresume.html', message="Unsupported file format. Only PDF, DOCX, and TXT are allowed.")

        if not resumes:
            return render_template('matchresume.html', message="No valid text extracted from resumes. Please check your files.")

        # TF-IDF Vectorization and Cosine Similarity
        vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
        vectors = vectorizer.toarray()

        job_vector = vectors[0]
        resume_vectors = vectors[1:]
        similarities = cosine_similarity([job_vector], resume_vectors)[0]

        # Filter top matches with scores above 30%
        top_matches = sorted(zip(filenames, similarities), key=lambda x: x[1], reverse=True)
        top_matches = [match[0] for match in top_matches if match[1] > 0.3][:4]  

        # If no matches are found
        if not top_matches:
            message = "No resumes matched above 30%."
        else:
            message = f"Top {len(top_matches)} Matching Resumes!"

        # Render results with only resume names
        return render_template(
            'matchresume.html',
            message=message,
            top_resume_names=top_matches
        )

    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
