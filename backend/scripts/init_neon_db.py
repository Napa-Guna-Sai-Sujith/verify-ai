import psycopg2

conn_str = "postgresql://neondb_owner:npg_HqwPkmy6upU8@ep-aged-shadow-axkukdm6-pooler.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require"

sql_script = """
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT,
    email TEXT UNIQUE,
    preferred_language TEXT DEFAULT 'English',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    input_type TEXT NOT NULL,
    input_text TEXT NOT NULL,
    detected_language TEXT,
    claims JSONB,
    assessment TEXT,
    trust_score INTEGER,
    explanation TEXT,
    recommendation TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID REFERENCES analyses(id) ON DELETE CASCADE,
    title TEXT,
    url TEXT,
    source_type TEXT,
    relevance TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

try:
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    cur.execute(sql_script)
    conn.commit()
    print("Schema created successfully!")

    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = cur.fetchall()
    print("Public Tables in Neon DB:", [t[0] for t in tables])
    
    cur.close()
    conn.close()
except Exception as e:
    print("Error:", e)
