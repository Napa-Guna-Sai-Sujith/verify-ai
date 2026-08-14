import psycopg2
from psycopg2.extras import RealDictCursor
import logging

from app.config import settings

logger = logging.getLogger(__name__)

def get_db_connection():
    if not settings.DATABASE_URL:
        return None
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        return conn
    except Exception as e:
        logger.error(f"Error connecting to Neon PostgreSQL database: {e}")
        return None

def create_user_profile(user_id: str, full_name: str, email: str, preferred_language: str = "English"):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO profiles (id, full_name, email, preferred_language)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (email) 
                DO UPDATE SET full_name = EXCLUDED.full_name, preferred_language = EXCLUDED.preferred_language
                RETURNING *;
                """,
                (user_id, full_name, email, preferred_language)
            )
            profile = cur.fetchone()
            conn.commit()
            return dict(profile) if profile else None
    except Exception as e:
        logger.error(f"Database error in create_user_profile: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()

def get_user_profile(email: str):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM profiles WHERE email = %s;", (email,))
            profile = cur.fetchone()
            return dict(profile) if profile else None
    except Exception as e:
        logger.error(f"Database error in get_user_profile: {e}")
        return None
    finally:
        if conn:
            conn.close()

def save_analysis_record(user_id: str, input_type: str, input_text: str, detected_language: str, claims: list, assessment: str, trust_score: int, explanation: str, recommendation: str, sources: list = None):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        import json
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO analyses (user_id, input_type, input_text, detected_language, claims, assessment, trust_score, explanation, recommendation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (user_id, input_type, input_text, detected_language, json.dumps(claims or []), assessment, trust_score, explanation, recommendation)
            )
            analysis = cur.fetchone()
            analysis_id = analysis["id"] if analysis else None

            if analysis_id and sources:
                for src in sources:
                    cur.execute(
                        """
                        INSERT INTO sources (analysis_id, title, url, source_type, relevance)
                        VALUES (%s, %s, %s, %s, %s);
                        """,
                        (analysis_id, src.get("title", ""), src.get("url", ""), src.get("source_type", "Official Domain"), src.get("relevance", ""))
                    )
            conn.commit()
            return dict(analysis) if analysis else None
    except Exception as e:
        logger.error(f"Database error in save_analysis_record: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()

def get_user_analyses(user_id: str):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT a.*, 
                       COALESCE(
                         json_agg(
                           json_build_object(
                             'id', s.id,
                             'title', s.title,
                             'url', s.url,
                             'source_type', s.source_type,
                             'relevance', s.relevance
                           )
                         ) FILTER (WHERE s.id IS NOT NULL), '[]'
                       ) as sources
                FROM analyses a
                LEFT JOIN sources s ON s.analysis_id = a.id
                WHERE a.user_id = %s
                GROUP BY a.id
                ORDER BY a.created_at DESC;
                """,
                (user_id,)
            )
            records = cur.fetchall()
            return [dict(r) for r in records]
    except Exception as e:
        logger.error(f"Database error in get_user_analyses: {e}")
        return []
    finally:
        if conn:
            conn.close()

