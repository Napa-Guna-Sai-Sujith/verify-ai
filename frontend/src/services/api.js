const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

/**
 * Send screenshot image base64 to dedicated OCR endpoint to extract text
 */
export async function extractOcrText({ imageBase64, preferredLanguage }) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/ocr`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image_b64: imageBase64,
        preferred_language: preferredLanguage || 'English',
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'OCR service error');
    }

    return await response.json();
  } catch (error) {
    console.warn('OCR endpoint request failed:', error.message);
    return {
      extracted_text: '',
      status: 'ocr_engine_missing',
      message: 'Tesseract OCR engine is not active on backend. Please type or paste text manually below.',
      ocr_engine_available: false,
      available_languages: []
    };
  }
}

/**
 * Send content (text or screenshot image base64) to FastAPI backend for analysis
 */
export async function analyzeContent({ text, imageBase64, preferredLanguage, userId, inputType }) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text || '',
        image_b64: imageBase64 || null,
        preferred_language: preferredLanguage || 'English',
        user_id: userId || null,
        input_type: inputType || 'text',
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Analysis service returned an error');
    }

    return await response.json();
  } catch (error) {
    console.warn('FastAPI backend request failed:', error.message);
    if (error.name === 'TypeError' || error.message.includes('fetch') || error.message.includes('NetworkError')) {
      throw new Error(`Unable to connect to backend server at ${API_BASE_URL}. Please verify the backend is running.`);
    }
    throw error;
  }
}

/**
 * Check backend health
 */
export async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Register a new user profile into Neon PostgreSQL via FastAPI
 */
export async function registerUserProfile({ email, fullName, preferredLanguage }) {
  const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      full_name: fullName,
      preferred_language: preferredLanguage || 'English',
    }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    // 409 Conflict = email already registered
    if (response.status === 409) {
      throw new Error('An account with this email already exists. Please sign in instead.');
    }
    throw new Error(err.detail || 'Registration failed. Please try again.');
  }

  return await response.json();
}

/**
 * Update an existing user profile in Neon PostgreSQL via FastAPI
 */
export async function updateUserProfile({ email, fullName, preferredLanguage }) {
  const response = await fetch(`${API_BASE_URL}/api/auth/profile`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      full_name: fullName,
      preferred_language: preferredLanguage || 'English',
    }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to update profile.');
  }

  return await response.json();
}

/**
 * Fetch user profile directly from Neon PostgreSQL DB via FastAPI
 * Returns null if user not found (404), throws on real errors
 */
export async function getUserProfile(email) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}/api/auth/profile?email=${encodeURIComponent(email)}`);
  } catch (netErr) {
    // Network / connection error
    throw new Error(`Cannot connect to backend server. Please make sure the backend is running at ${API_BASE_URL}.`);
  }

  if (response.status === 404) {
    return null; // User simply doesn't exist
  }

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to communicate with authentication database.');
  }

  return await response.json();
}

/**
 * Fetch saved analyses and sources from Neon PostgreSQL DB for user
 */
export async function fetchUserAnalyses(userId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/analyses?user_id=${encodeURIComponent(userId)}`);
    if (!response.ok) return [];
    return await response.json();
  } catch (err) {
    console.error('Database analyses fetch error:', err);
    return [];
  }
}
