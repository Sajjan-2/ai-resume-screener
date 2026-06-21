from flask import Flask, render_template, request
import pdfplumber
import os

from utils.skill_extractor import extract_skills
from utils.matcher import (
    calculate_match,
    calculate_skill_score,
    calculate_text_similarity,
    calculate_final_score,
)

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Analyze Resume
@app.route('/analyze', methods=['POST'])
def analyze():

    # Get uploaded file
    resume = request.files['resume']

    # Get job description
    job_description = request.form['job_description']

    # Save uploaded PDF
    filename = resume.filename

    # Create uploads folder if it doesn't exist
    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", filename)
    resume.save(file_path)

    # Extract text from PDF
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

    # Extract skills from resume
    found_skills = extract_skills(text)

    # Extract skills from job description
    job_skills = extract_skills(job_description)

    # Calculate scores
    matched_skills, missing_skills = calculate_match(found_skills, job_skills)
    skill_score = calculate_skill_score(matched_skills, job_skills)
    similarity_score = calculate_text_similarity(text, job_description)
    match_score = calculate_final_score(skill_score, similarity_score)

    return render_template(
        "result.html",
        score=match_score,
        skill_score=skill_score,
        similarity_score=similarity_score,
        matched=matched_skills,
        missing=missing_skills,
        resume_skills=found_skills,
        filename=filename
    )


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)