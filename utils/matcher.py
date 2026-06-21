from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match(resume_skills, job_skills):
    """Compares resume skills against job-required skills."""
    matched_skills = [skill for skill in job_skills if skill in resume_skills]
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]
    return matched_skills, missing_skills


def calculate_skill_score(matched_skills, job_skills):
    """Percentage of job-required skills found in the resume."""
    if len(job_skills) == 0:
        return 0.0
    return round((len(matched_skills) / len(job_skills)) * 100, 2)


def calculate_text_similarity(resume_text, job_description):
    """
    Converts both texts into TF-IDF vectors and measures cosine
    similarity between them. Captures overall contextual closeness,
    not just exact skill-keyword overlap.
    """
    documents = [resume_text, job_description]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)


def calculate_final_score(skill_score, similarity_score, skill_weight=0.6, similarity_weight=0.4):
    """
    Blends both scores. Skill matches are weighted higher since exact
    keyword matches are the strongest signal for resume screening;
    TF-IDF similarity adds broader contextual relevance.
    """
    final = (skill_score * skill_weight) + (similarity_score * similarity_weight)
    return round(final, 2)