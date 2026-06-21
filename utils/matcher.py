from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match(resume_skills, job_skills):
    matched_skills = [skill for skill in job_skills if skill in resume_skills]
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]
    return matched_skills, missing_skills


def calculate_skill_score(matched_skills, job_skills):
    if len(job_skills) == 0:
        return 0.0

    return round((len(matched_skills) / len(job_skills)) * 100, 2)


def calculate_text_similarity(resume_text, job_description):
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)


def calculate_final_score(skill_score, similarity_score):
    final_score = (skill_score * 0.9) + (similarity_score * 0.1)
    return round(final_score, 2)