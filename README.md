# Verity AI

> **"Check before you trust."**

Verity AI is a multilingual Digital Trust platform designed to help citizens identify, understand, and respond to misinformation and misleading digital content, with a dedicated focus on Indian regional languages (Kannada, Telugu, Tamil, Hindi, and English).

---

## 1. Project Overview

Digital misinformation often spreads rapidly through private messaging apps and social platforms in regional languages. Existing tools often output binary labels like "FAKE" or "REAL" without context, reasoning, or evidence. 

Verity AI shifts the paradigm from simple binary classification to transparent **Digital Trust**:
`IDENTIFY → VERIFY → UNDERSTAND → RESPOND`

---

## 2. Official Problem Statement

> *"How can technology help people identify, understand, and respond to misinformation and misleading content, especially in regional languages?"*

---

## 3. Solution Philosophy

Verity AI breaks down digital content verification into four core steps:
1. **IDENTIFY**: Isolate key factual claims from submitted text or WhatsApp screenshots using OCR and claim extraction algorithms.
2. **VERIFY**: Cross-reference extracted claims against official government portals (`.gov.in`, `pib.gov.in`), certified fact-checkers (`altnews.in`, `boomlive.in`, `factly.in`, `newschecker.in`), and reputable news publishers.
3. **UNDERSTAND**: Provide intuitive, non-technical explanations in plain language, categorized into Green (Evidence Supported), Yellow (Needs Verification), and Red (Potentially Misleading).
4. **RESPOND**: Supply clear, actionable advice on what to do before forwarding or sharing on social media.

---

## 4. Key Features

- **Multilingual Input & Detection**: Direct support for **Kannada, Telugu, Tamil, Hindi, and English**. Real-time script detection using Unicode boundary analysis and NLP models.
- **Screenshot Upload & Tesseract OCR**: Upload forwarded WhatsApp messages or social media images. Extract text automatically before verification.
- **Claim Isolation**: Automatic identification of specific verifiable claims (monetary amounts, government circulars, health alerts).
- **Evidence Cross-Referencing**: Live query matching against official government and fact-checking domains.
- **Voice Read Aloud (Browser Speech Synthesis)**: Audio explanation in the user's preferred language using native Web Speech API integration.
- **Before-You-Share Educational Checklist**: Interactive guidance promoting responsible digital sharing habits.
- **Personal Trust Dashboard & History**: Saved verifications and aggregate user statistics (Total checks, Evidence Supported, Needs Verification, Potentially Misleading).

---

## 5. User Workflow

```
[User Input: Text / WhatsApp Screenshot]
            │
            ▼
[FastAPI Backend /api/analyze]
            │
            ├─► 1. Tesseract OCR (Image Text Extraction)
            ├─► 2. Language Detection (Unicode Script & langdetect)
            ├─► 3. Claim Extraction (Factual Sentence Isolation)
            ├─► 4. Evidence Verification (DuckDuckGo / Official Domain Query)
            └─► 5. Trust Engine (Score 0-100, Explanation & Recommendation)
            │
            ▼
[Frontend Analysis Result View]
            │
            ├─► 🟢 Supported / 🟡 Needs Verification / 🔴 Misleading
            ├─► 🔊 Listen Explanation (Web Speech TTS)
            └─► Persist to Neon PostgreSQL Database (analyses & sources)
```

---

## 6. System Architecture

Verity AI uses a decoupled **Backend-for-Frontend (BFF)** architecture:
- **Frontend App**: SPA built with React 18, Vite, and Tailwind CSS.
- **Backend API**: Python FastAPI server providing OCR, NLP, and evidence verification microservices.
- **Database & Auth**: Neon PostgreSQL Database + FastAPI Custom User Service.

---

## 7. Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.10+, FastAPI, Pydantic, Uvicorn, psycopg2
- **OCR Engine**: Tesseract OCR (`pytesseract`, Pillow)
- **Language & NLP**: `langdetect`, regex script analysis, DuckDuckGo Search API
- **Database**: Neon PostgreSQL (`profiles`, `analyses`, `sources`)

---

## 8. AI/NLP Pipeline

The AI/NLP engine operates modularly:
- **Rule & Search NLP Pipeline**: Analyzes claims against search results and urgency patterns.
- **Modular AI API**: Configurable via `AI_API_KEY` and `AI_PROVIDER` environment variables (e.g. Gemini / OpenAI API).

---

## 9. OCR Integration

Integrated with **Tesseract OCR**:
- Decodes uploaded base64 image strings.
- Applies image preprocessing (conversion to RGB format).
- Executes multilingual character recognition (`eng+kan+tel+tam+hin`).

---

## 10. Regional Language Support

Native script recognition and display for:
- **Kannada (ಕನ್ನಡ)**: Script range `U+0C80` - `U+0CFF`
- **Telugu (తెలుగు)**: Script range `U+0C00` - `U+0C7F`
- **Tamil (தமிழ்)**: Script range `U+0B80` - `U+0BFF`
- **Hindi (हिंदी)**: Script range `U+0900` - `U+097F`
- **English**: Standard Latin script

---

## 11. Database Schema (Neon PostgreSQL)

### `profiles`
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
full_name TEXT
email TEXT UNIQUE
preferred_language TEXT DEFAULT 'English'
created_at TIMESTAMPTZ DEFAULT NOW()
```

### `analyses`
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE
input_type TEXT NOT NULL
input_text TEXT NOT NULL
detected_language TEXT
claims JSONB
assessment TEXT
trust_score INTEGER
explanation TEXT
recommendation TEXT
created_at TIMESTAMPTZ DEFAULT NOW()
```

### `sources`
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
analysis_id UUID NOT NULL REFERENCES public.analyses(id) ON DELETE CASCADE
title TEXT
url TEXT
source_type TEXT
relevance TEXT
created_at TIMESTAMPTZ DEFAULT NOW()
```

---

## 12. Authentication

Uses direct email/profile authentication integrated with **Neon PostgreSQL**.

---

## 13. API Endpoints

### `GET /api/health`
Checks backend health and service status.

### `POST /api/analyze`
Main verification endpoint.

---

## 14. Environment Variables

### Backend (`backend/.env`)
```env
DATABASE_URL=postgresql://neondb_owner:npg_HqwPkmy6upU8@ep-aged-shadow-axkukdm6-pooler.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require
AI_API_KEY=
AI_PROVIDER=gemini
```

---

## 15. Setup & Running Locally

### Prerequisites
- Node.js (v18+) & npm
- Python (v3.10+)
- Tesseract OCR (Optional for local OCR binary execution)

### Step 1: Install Frontend Dependencies
```bash
cd frontend
npm install
```

### Step 2: Install Backend Dependencies
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3: Run Backend API
```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 4: Run Frontend App
```bash
cd frontend
npm run dev
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173) in your browser.

---

## 16. Verification & Automated Tests

To run the backend test suite:
```bash
cd backend
pytest
```

---

## 17. Deployment Strategy

- **Frontend**: Suitable for deployment on Vercel or Netlify (`npm run build`).
- **Backend**: Suitable for deployment on Railway, Render, or AWS App Runner.

---

## 18. External APIs & Datasets Used

- **DuckDuckGo Search API**: Real-time evidence search across official government domains (`.gov.in`, `pib.gov.in`) and certified fact-checking databases.
- **Browser Web Speech API**: Native client-side text-to-speech synthesis for regional audio explanations.

---

## 19. Limitations

- Web evidence retrieval depends on active internet connectivity and indexable public fact-check records.
- OCR quality depends on image resolution and clarity of screenshot text.

---

## 20. Future Scope

- Integration with official WhatsApp Business API bot for instant chat verification.
- Offline lightweight regional language models for zero-connectivity environments.
- Video keyframe extraction for verifying manipulated video claims.

---

## 21. Project Team

Developed for the Digital Trust Hackathon by **Team Verity AI**.
