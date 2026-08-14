/**
 * Utility functions for classifying analysis records in Dashboard Statistics and History.
 * Ensures strict separation between Factual Message Assessments and URL-Only Verifications.
 */

export const isUrlOnlyAnalysis = (item) => {
  if (!item) return false;

  // 1. If trust_score is null/undefined and url_check / url_checks is present
  if ((item.trust_score === null || item.trust_score === undefined) && (item.url_check || (item.url_checks && item.url_checks.length > 0))) {
    return true;
  }

  // 2. If detected_content_types contains 'URL' and NOT 'MESSAGE_TEXT' or 'FACTUAL_CLAIM'
  if (item.detected_content_types && item.detected_content_types.includes('URL') && !item.detected_content_types.includes('MESSAGE_TEXT') && !item.detected_content_types.includes('FACTUAL_CLAIM')) {
    return true;
  }

  // 3. If assessment string matches explicit URL status labels
  // (Kept in sync with the exact status_label strings produced by
  // backend/app/services/url_service.py's analyze_url_safety().)
  const a = (item.assessment || '').toUpperCase();
  if (
    a.includes('TRUSTED DOMAIN') ||
    a.includes('UNVERIFIED URL') ||
    a.includes('UNVERIFIED SHORTENED LINK') ||
    a.includes('UNVERIFIED LINK') ||
    a.includes('SUSPICIOUS') && a.includes('URL') ||
    a.includes('SUSPICIOUS LINK') ||
    a.includes('INVALID URL') ||
    a === 'TRUSTED' ||
    a === 'UNVERIFIED' ||
    a === 'SUSPICIOUS' ||
    a === 'INVALID'
  ) {
    return true;
  }

  return false;
};

export const isNotRelevantAnalysis = (item) => {
  if (!item) return false;
  const a = (item.assessment || '').toUpperCase();
  return a.includes('NOT RELEVANT') || a.includes('సూక్తవాగిల్ల') || a.includes('సంబంధిత') || a.includes('प्रासंगिक नहीं');
};
