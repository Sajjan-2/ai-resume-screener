import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "YourNewPassword123!",
    "database": "resume_screening",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def save_result(resume_name, match_score, matched_skills, missing_skills, resume_skills):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO screening_results
                (resume_name, match_score, matched_skills, missing_skills, resume_skills)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            resume_name,
            match_score,
            ", ".join(matched_skills),
            ", ".join(missing_skills),
            ", ".join(resume_skills),
        ))
        conn.commit()
    except Error as e:
        print(f"[DB ERROR] save_result failed: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def get_all_results():
    conn = None
    results = []
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM screening_results ORDER BY created_at DESC")
        results = cursor.fetchall()
    except Error as e:
        print(f"[DB ERROR] get_all_results failed: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return results