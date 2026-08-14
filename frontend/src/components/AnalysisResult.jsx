import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  AlertTriangle, 
  XCircle, 
  Volume2, 
  VolumeX, 
  ExternalLink, 
  Globe, 
  Languages,
  CheckCircle, 
  Sparkles, 
  FileText, 
  ArrowRight,
  Info,
  HelpCircle,
  Tag,
  Link,
  ShieldAlert
} from 'lucide-react';
import BeforeYouShare from './BeforeYouShare';
import { getTranslation, getLocalizedTopic } from '../services/localization';

export default function AnalysisResult({ result, onReset }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [voices, setVoices] = useState([]);
  const [voiceNotice, setVoiceNotice] = useState(null);

  // Initialize Speech Synthesis and subscribe to voice changes
  useEffect(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      const updateVoices = () => {
        try {
          const available = window.speechSynthesis.getVoices();
          setVoices(available || []);
        } catch (e) {
          console.warn('Could not load browser voices:', e);
        }
      };

      updateVoices();
      window.speechSynthesis.onvoiceschanged = updateVoices;

      return () => {
        if (window.speechSynthesis) {
          window.speechSynthesis.onvoiceschanged = null;
        }
      };
    }
  }, []);

  if (!result) return null;

  const {
    detected_language = 'English',
    preferred_language = 'English',
    extracted_text = '',
    claim_topic = 'General',
    assessment = 'Needs Verification',
    trust_score = null,
    explanation = '',
    recommendation = '',
    risk_indicators = [],
    url_check = null,
    url_checks = [],
    sources = [],
    before_you_share = null
  } = result;

  const allUrlChecks = url_checks && url_checks.length > 0 ? url_checks : (url_check ? [url_check] : []);
  const isUrlOnlyInput = allUrlChecks.length > 0 && (!sources || sources.length === 0) && trust_score === null;

  const isNotRelevant = trust_score === null && (!allUrlChecks || allUrlChecks.length === 0) && (assessment?.toUpperCase().includes('NOT RELEVANT') || assessment?.includes('సూక్తవాగిಲ್ಲ') || assessment?.includes('సంబంధిత') || assessment?.includes('प्रासंगिक नहीं'));

  // Handle NOT RELEVANT UI State (PART 13)
  if (isNotRelevant) {
    return (
      <div className="max-w-2xl mx-auto my-8 animate-fadeIn">
        <div className="glass-panel rounded-3xl p-8 border border-slate-700 bg-slate-900/90 text-center shadow-xl space-y-6">
          <div className="w-16 h-16 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center mx-auto text-amber-400">
            <HelpCircle className="w-10 h-10" />
          </div>

          <div className="space-y-2">
            <h2 className="text-2xl font-black text-white font-['Outfit'] tracking-tight">
              {getTranslation(preferred_language, 'not_relevant_title')}
            </h2>
            <p className="text-sm text-slate-300 max-w-lg mx-auto leading-relaxed">
              {getTranslation(preferred_language, 'not_relevant_msg')}
            </p>
          </div>

          {extracted_text && (
            <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-400 max-w-md mx-auto italic">
              "{extracted_text.slice(0, 150)}{extracted_text.length > 150 ? '...' : ''}"
            </div>
          )}

          <div className="pt-2">
            <button
              onClick={onReset}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-sm transition-all shadow-glow-indigo"
            >
              {getTranslation(preferred_language, 'try_another_btn')} <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Category Styling
  const isGreen = trust_score !== null && trust_score >= 70;
  const isRed = trust_score !== null && trust_score < 40;

  const getBadgeStyle = () => {
    if (isGreen) return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 shadow-glow-teal';
    if (isRed) return 'bg-rose-500/10 text-rose-400 border-rose-500/30 shadow-glow-rose';
    return 'bg-amber-500/10 text-amber-400 border-amber-500/30 shadow-glow-amber';
  };

  const getAssessmentIcon = () => {
    if (isGreen) return <ShieldCheck className="w-8 h-8 text-emerald-400" />;
    if (isRed) return <XCircle className="w-8 h-8 text-rose-400" />;
    return <AlertTriangle className="w-8 h-8 text-amber-400" />;
  };

  // Browser Voice Matching
  const getMatchingVoice = (lang, voiceList) => {
    if (!voiceList || voiceList.length === 0) return null;
    const target = (lang || 'English').toLowerCase().trim();

    const searchMap = {
      english: ['en-in', 'en-us', 'en_in', 'en_us', 'en'],
      kannada: ['kn-in', 'kn_in', 'kn', 'kannada'],
      telugu: ['te-in', 'te_in', 'te', 'telugu'],
      tamil: ['ta-in', 'ta_in', 'ta', 'tamil'],
      hindi: ['hi-in', 'hi_in', 'hi', 'hindi']
    };

    const terms = searchMap[target] || [target];

    for (const term of terms) {
      const found = voiceList.find(v => 
        (v.lang || '').toLowerCase() === term || 
        (v.lang || '').toLowerCase().replace('_', '-') === term
      );
      if (found) return found;
    }

    return null;
  };

  const matchingVoice = getMatchingVoice(preferred_language, voices);

  const handleSpeak = () => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      setVoiceNotice(`Speech synthesis is not supported in this browser.`);
      return;
    }

    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      return;
    }

    window.speechSynthesis.cancel();

    if (!matchingVoice && preferred_language !== 'English') {
      setVoiceNotice(`A native ${preferred_language} voice was not found on this device/browser. Playing with the closest available voice instead.`);
    } else {
      setVoiceNotice(null);
    }

    const speechText = `${assessment}. ${explanation} ${recommendation}`;
    const utterance = new SpeechSynthesisUtterance(speechText);

    const bcp47Map = {
      English: 'en-IN',
      Kannada: 'kn-IN',
      Telugu: 'te-IN',
      Tamil: 'ta-IN',
      Hindi: 'hi-IN'
    };

    utterance.lang = matchingVoice ? matchingVoice.lang : (bcp47Map[preferred_language] || 'en-IN');
    utterance.rate = 0.92;

    if (matchingVoice) utterance.voice = matchingVoice;

    utterance.onend = () => setIsPlaying(false);
    utterance.onerror = () => setIsPlaying(false);

    setIsPlaying(true);
    window.speechSynthesis.speak(utterance);
  };

  const getEvidenceStatusBadge = (status) => {
    if (status === 'SUPPORTS CLAIM') {
      return (
        <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-300 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-800">
          {getTranslation(preferred_language, 'supports_claim')}
        </span>
      );
    }
    if (status === 'CONTRADICTS CLAIM') {
      return (
        <span className="text-[10px] font-bold uppercase tracking-wider text-rose-300 bg-rose-950/80 px-2 py-0.5 rounded border border-rose-800">
          {getTranslation(preferred_language, 'contradicts_claim')}
        </span>
      );
    }
    return (
      <span className="text-[10px] font-bold uppercase tracking-wider text-amber-300 bg-amber-950/80 px-2 py-0.5 rounded border border-amber-800">
        {getTranslation(preferred_language, 'inconclusive_claim')}
      </span>
    );
  };

  const getUrlStatusBadge = (status, statusLabel) => {
    if (status === 'TRUSTED') {
      return <span className="text-xs font-bold text-emerald-400 bg-emerald-950/80 px-2.5 py-1 rounded-lg border border-emerald-800">{statusLabel}</span>;
    }
    if (status === 'SUSPICIOUS' || status === 'INVALID') {
      return <span className="text-xs font-bold text-rose-400 bg-rose-950/80 px-2.5 py-1 rounded-lg border border-rose-800">{statusLabel}</span>;
    }
    return <span className="text-xs font-bold text-amber-400 bg-amber-950/80 px-2.5 py-1 rounded-lg border border-amber-800">{statusLabel}</span>;
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto my-6 animate-fadeIn">
      
      {/* Header Banner */}
      <div className={`glass-panel rounded-3xl p-6 sm:p-8 border ${getBadgeStyle()} relative overflow-hidden`}>
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
          
          <div className="flex items-center gap-4">
            <div className="p-3.5 rounded-2xl bg-slate-950/80 border border-slate-800 shadow-inner">
              {getAssessmentIcon()}
            </div>
            <div>
              <div className="flex flex-wrap items-center gap-2 mb-1.5">
                <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
                  {getTranslation(preferred_language, 'trust_engine')}
                </span>
                
                {/* Domain Topic Badge */}
                <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-purple-950 border border-purple-800 text-purple-300 font-semibold flex items-center gap-1">
                  <Tag className="w-3 h-3 text-purple-400" />
                  {getTranslation(preferred_language, 'topic')}: {getLocalizedTopic(preferred_language, claim_topic)}
                </span>

                <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-slate-900 border border-slate-700 text-teal-400 font-semibold flex items-center gap-1">
                  <Globe className="w-3 h-3" />
                  {getTranslation(preferred_language, 'detected_language')}: {detected_language}
                </span>

                <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-indigo-950 border border-indigo-700 text-indigo-300 font-semibold flex items-center gap-1 shadow-sm">
                  <Languages className="w-3 h-3 text-indigo-400" />
                  {getTranslation(preferred_language, 'response_language')}: {preferred_language}
                </span>
              </div>

              <h2 className="text-2xl sm:text-3xl font-black text-white font-['Outfit'] tracking-tight">
                {assessment}
              </h2>
            </div>
          </div>

          {/* Dynamic Trust Score Circle Meter */}
          {trust_score !== null && (
            <div className="flex items-center gap-4 bg-slate-950/80 px-5 py-3 rounded-2xl border border-slate-800 self-stretch sm:self-auto justify-between">
              <div className="text-left">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                  {getTranslation(preferred_language, 'evidence_trust_score')}
                </span>
                <span className="text-2xl font-black text-white font-['Outfit']">
                  {trust_score}<span className="text-sm font-normal text-slate-400">/100</span>
                </span>
              </div>
              <div className="w-12 h-12 rounded-full border-4 border-slate-800 flex items-center justify-center relative">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    className="text-slate-800"
                    strokeWidth="3.5"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path
                    className={isGreen ? 'text-emerald-400' : isRed ? 'text-rose-500' : 'text-amber-400'}
                    strokeDasharray={`${trust_score}, 100`}
                    strokeWidth="3.5"
                    strokeLinecap="round"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                </svg>
                <Sparkles className="w-4 h-4 text-indigo-400 absolute" />
              </div>
            </div>
          )}

        </div>
      </div>

      {/* 🔗 Dedicated Link Check Section (Single or Multiple URLs) */}
      {allUrlChecks && allUrlChecks.length > 0 && (
        <div className="space-y-4">
          {allUrlChecks.map((uCheck, idx) => (
            <div key={idx} className="glass-panel rounded-2xl p-6 border border-slate-800 bg-slate-900/80 shadow-md">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-3 pb-3 border-b border-slate-800">
                <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2 font-['Outfit']">
                  <Link className="w-4 h-4 text-teal-400" />
                  {getTranslation(preferred_language, 'link_check_title')} {allUrlChecks.length > 1 ? `#${idx + 1}` : ''}
                </h3>
                {getUrlStatusBadge(uCheck.status, uCheck.status_label)}
              </div>

              <div className="space-y-2">
                <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 font-mono text-xs text-indigo-300 break-all">
                  {uCheck.url}
                </div>
                <p className="text-xs text-slate-300 leading-relaxed font-medium pt-1">
                  <span className="font-semibold text-slate-200">Why: </span>{uCheck.reason}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Risk Indicators Section */}
      {risk_indicators && risk_indicators.length > 0 && (
        <div className="glass-panel rounded-2xl p-5 border border-rose-500/30 bg-rose-950/20">
          <h3 className="text-xs font-bold text-rose-400 uppercase tracking-wider mb-2.5 flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-rose-400" />
            {getTranslation(preferred_language, 'risk_indicators_title')}
          </h3>
          <ul className="space-y-1.5 text-xs text-rose-200 font-medium">
            {risk_indicators.map((ind, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-rose-400 font-bold">•</span>
                <span>{ind}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Grid Content: Message Analysis, Explanation, Action, Sources */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Left 2 Cols: Message Analysis & Localized Explanation */}
        <div className="md:col-span-2 space-y-6">
          
          {/* Message Analysis (Complete Original Input Message) */}
          <div className="glass-panel rounded-2xl p-6 border border-slate-800 bg-slate-900/60">
            <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-2">
              <FileText className="w-4 h-4 text-indigo-400" />
              {getTranslation(preferred_language, 'message_analysis')}
            </h3>
            
            <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-slate-200 text-sm font-medium leading-relaxed">
              {isUrlOnlyInput ? (
                "No factual message was detected in the submission."
              ) : extracted_text ? (
                `"${extracted_text}"`
              ) : (
                "No text message detected."
              )}
            </div>
          </div>

          {/* Localized Explanation */}
          <div className="glass-panel rounded-2xl p-6 border border-slate-800 bg-slate-900/60">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-800/80">
              <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                <Info className="w-4 h-4 text-teal-400" />
                {getTranslation(preferred_language, 'why_header')}
              </h3>

              <div className="flex items-center gap-2">
                <button
                  onClick={handleSpeak}
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                    isPlaying
                      ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40 animate-pulse'
                      : 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 hover:bg-indigo-600/30'
                  }`}
                >
                  {isPlaying ? (
                    <>
                      <VolumeX className="w-3.5 h-3.5" /> {getTranslation(preferred_language, 'stop_voice')}
                    </>
                  ) : (
                    <>
                      <Volume2 className="w-3.5 h-3.5 text-teal-400" />
                      {getTranslation(preferred_language, 'listen')} ({preferred_language})
                    </>
                  )}
                </button>
              </div>
            </div>

            {voiceNotice && (
              <div className="mb-3 text-[11px] text-amber-300 bg-amber-950/40 border border-amber-800/60 p-2.5 rounded-lg leading-relaxed">
                ℹ️ {voiceNotice}
              </div>
            )}

            <p className="text-slate-200 text-sm leading-relaxed whitespace-pre-line bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
              {explanation}
            </p>
          </div>

        </div>

        {/* Right Col: Localized Recommended Action & Sources (Hidden for URL-only input!) */}
        <div className="space-y-6">
          
          {/* Localized Recommended Action */}
          <div className="glass-panel rounded-2xl p-6 border border-indigo-500/30 bg-slate-900/80 shadow-glow-indigo">
            <h3 className="text-sm font-bold text-indigo-300 uppercase tracking-wider mb-3 flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-teal-400" />
              {getTranslation(preferred_language, 'recommended_action')}
            </h3>
            <div className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-500/30 text-indigo-100 text-sm font-semibold leading-relaxed">
              {recommendation}
            </div>
          </div>

          {/* Evidence Sources (Rendered ONLY if message evidence sources exist; Hidden for URL-only input!) */}
          {!isUrlOnlyInput && (
            <div className="glass-panel rounded-2xl p-6 border border-slate-800 bg-slate-900/60">
              <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3 flex items-center justify-between">
                <span>{getTranslation(preferred_language, 'evidence_and_sources')}</span>
                <span className="text-xs text-slate-500 font-normal">
                  {sources.length} {getTranslation(preferred_language, 'sources_checked')}
                </span>
              </h3>

              {sources && sources.length > 0 ? (
                <div className="space-y-3">
                  {sources.map((source, index) => (
                    <a
                      key={index}
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-indigo-500/50 hover:bg-slate-900 transition-all group"
                    >
                      <div className="flex flex-wrap items-center justify-between gap-1 mb-2">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-teal-400 bg-teal-950/60 px-2 py-0.5 rounded border border-teal-800">
                          {source.source_type || 'Official Source'}
                        </span>
                        {getEvidenceStatusBadge(source.evidence_status)}
                      </div>

                      <div className="flex items-center justify-between gap-2 mb-1">
                        <h4 className="text-xs font-semibold text-slate-200 group-hover:text-white line-clamp-1">
                          {source.title}
                        </h4>
                        <ExternalLink className="w-3.5 h-3.5 text-slate-500 group-hover:text-indigo-400 transition-colors flex-shrink-0" />
                      </div>

                      <p className="text-[11px] text-slate-400 line-clamp-2 leading-tight">
                        {source.relevance}
                      </p>
                    </a>
                  ))}
                </div>
              ) : (
                <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 text-center">
                  <p className="text-xs text-slate-400 leading-relaxed">
                    {getTranslation(preferred_language, 'no_sources_found')}
                  </p>
                </div>
              )}
            </div>
          )}

        </div>

      </div>

      {/* Localized Digital Trust Checklist */}
      <BeforeYouShare items={before_you_share} language={preferred_language} />

      {/* Action bar */}
      <div className="flex justify-center pt-4">
        <button
          onClick={onReset}
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-sm font-semibold transition-all shadow-md border border-slate-700"
        >
          {getTranslation(preferred_language, 'verify_another')} <ArrowRight className="w-4 h-4" />
        </button>
      </div>

    </div>
  );
}
