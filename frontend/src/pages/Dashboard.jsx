import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  Upload, 
  FileText, 
  Globe, 
  Search, 
  Sparkles, 
  History as HistoryIcon, 
  CheckCircle2, 
  AlertTriangle, 
  XCircle, 
  Image as ImageIcon,
  ArrowRight,
  RefreshCw,
  Loader2,
  Check,
  Link as LinkIcon
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { analyzeContent, extractOcrText, fetchUserAnalyses } from '../services/api';
import LoadingProgress from '../components/LoadingProgress';
import AnalysisResult from '../components/AnalysisResult';
import StatCard from '../components/StatCard';
import { isUrlOnlyAnalysis, isNotRelevantAnalysis } from '../services/analysisHelpers';

export default function Dashboard({ onNavigate }) {
  const { user, profile } = useAuth();
  
  // Tabs: 'text' or 'screenshot'
  const [activeInputTab, setActiveInputTab] = useState('text');
  const [inputText, setInputText] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  
  // OCR Extraction State
  const [ocrLoading, setOcrLoading] = useState(false);
  const [ocrStatus, setOcrStatus] = useState(null);
  const [ocrMessage, setOcrMessage] = useState(null);

  // State
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [recentAnalyses, setRecentAnalyses] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    supported: 0,
    needsVerification: 0,
    misleading: 0,
    urlChecksCount: 0
  });

  useEffect(() => {
    fetchUserDataAndStats();
  }, [user]);

  const fetchUserDataAndStats = async () => {
    if (!user) return;
    try {
      const data = await fetchUserAnalyses(user.id);
      if (data) {
        setRecentAnalyses(data.slice(0, 5));
        computeStats(data);
      }
    } catch (err) {
      console.error('Dashboard stats fetch exception:', err);
    }
  };

  const computeStats = (dataList) => {
    let supported = 0;
    let needsVerif = 0;
    let misleading = 0;
    let urlChecksCount = 0;

    dataList.forEach(item => {
      if (isNotRelevantAnalysis(item)) return;
      if (isUrlOnlyAnalysis(item)) {
        urlChecksCount++;
        return;
      }
      const a = (item.assessment || '').toLowerCase();
      if (a.includes('supported') || a.includes('ದೃಢೀಕರಿಸಲಾಗಿದೆ') || a.includes('నిర్ధారించబడింది') || a.includes('உறுதிப்படுத்தப்பட்டது') || a.includes('प्रमाणित')) {
        supported++;
      } else if (a.includes('misleading') || a.includes('ತಪ್ಪಿಸುವ') || a.includes('తప్పుదోవ') || a.includes('வழிநடத்த') || a.includes('भ्रामक')) {
        misleading++;
      } else if (a.includes('needs verification') || a.includes('ಪರಿಶೀಲನೆ ಅಗತ್ಯವಿದೆ') || a.includes('ధృవీకరణ అవసరం') || a.includes('சரிபார்ப்பு தேவை') || a.includes('सत्यापन की आवश्यकता')) {
        needsVerif++;
      }
    });

    setStats({
      total: dataList.length,
      supported,
      needsVerification: needsVerif,
      misleading,
      urlChecksCount
    });
  };

  const handleImageChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      setErrorMessage('Please upload a valid image file (PNG, JPG, WEBP).');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setErrorMessage('Image size must be under 5MB.');
      return;
    }

    setImageFile(file);
    setErrorMessage(null);
    setOcrStatus(null);
    setOcrMessage(null);

    const reader = new FileReader();
    reader.onload = async (event) => {
      const dataUrl = event.target.result;
      setImagePreview(dataUrl);
      const b64 = dataUrl.split(',')[1] || dataUrl;

      setOcrLoading(true);
      try {
        const res = await extractOcrText({
          imageBase64: b64,
          preferredLanguage: profile?.preferred_language || 'English'
        });

        setOcrStatus(res.status);
        setOcrMessage(res.message);

        if (res.extracted_text && res.extracted_text.trim()) {
          setInputText(res.extracted_text);
        }
      } catch (ocrErr) {
        console.warn('OCR error:', ocrErr);
        setOcrStatus('ocr_engine_missing');
        setOcrMessage('Tesseract OCR engine is not active. Please type or paste the message text manually below.');
      } finally {
        setOcrLoading(false);
      }
    };
    reader.readAsDataURL(file);
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setErrorMessage(null);

    const textToAnalyze = inputText.trim();

    if (!textToAnalyze) {
      if (activeInputTab === 'screenshot' && !imageFile) {
        setErrorMessage('Please select a screenshot image or enter content text to verify.');
      } else if (activeInputTab === 'screenshot' && imageFile) {
        setErrorMessage('No text found in screenshot. Please type or paste the message text in the editable box below.');
      } else {
        setErrorMessage('Please enter digital content or news claim text to verify.');
      }
      return;
    }

    setAnalyzing(true);
    setAnalysisResult(null);

    try {
      let imageBase64 = null;
      if (activeInputTab === 'screenshot' && imagePreview && !textToAnalyze) {
        imageBase64 = imagePreview.split(',')[1] || imagePreview;
      }

      const resultData = await analyzeContent({
        text: textToAnalyze,
        imageBase64: imageBase64,
        preferredLanguage: profile?.preferred_language || 'English',
        userId: user.id,
        inputType: activeInputTab,
      });

      setAnalysisResult(resultData);
      fetchUserDataAndStats();

    } catch (err) {
      console.error('Analysis error:', err);
      setErrorMessage(err.message || "We couldn't verify this claim right now. Please check backend connection and try again.");
    } finally {
      setAnalyzing(false);
    }
  };


  const handleReset = () => {
    setAnalysisResult(null);
    setInputText('');
    setImageFile(null);
    setImagePreview(null);
    setOcrStatus(null);
    setOcrMessage(null);
  };

  return (
    <div className="max-w-7xl mx-auto my-6 px-4 space-y-8">
      
      {/* Welcome Banner */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-indigo-500/20 bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-bold uppercase tracking-widest text-teal-400 block mb-1">
            DIGITAL TRUST WORKSPACE
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white font-['Outfit']">
            {profile?.full_name?.trim() ? `Welcome, ${profile.full_name.trim()}` : 'Welcome back'}
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 mt-1">
            Target Language: <span className="text-indigo-300 font-semibold">{profile?.preferred_language || 'English'}</span> • Regional OCR & Fact-Check Engine Active
          </p>
        </div>

        <button
          onClick={() => onNavigate('profile')}
          className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-200 transition-colors"
        >
          Change Language Settings
        </button>
      </div>

      {/* Personal Trust Statistics Cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3.5">
        <StatCard
          title="Total Checks"
          value={stats.total}
          icon={Search}
          colorClass="bg-indigo-500/10 text-indigo-400"
          subtitle="Lifetime verifications"
        />
        <StatCard
          title="Evidence Supported"
          value={stats.supported}
          icon={CheckCircle2}
          colorClass="bg-emerald-500/10 text-emerald-400"
          badgeText="🟢 Green"
          subtitle="Corroborated claims"
        />
        <StatCard
          title="Needs Verification"
          value={stats.needsVerification}
          icon={AlertTriangle}
          colorClass="bg-amber-500/10 text-amber-400"
          badgeText="🟡 Yellow"
          subtitle="Factual claims"
        />
        <StatCard
          title="Potentially Misleading"
          value={stats.misleading}
          icon={XCircle}
          colorClass="bg-rose-500/10 text-rose-400"
          badgeText="🔴 Red"
          subtitle="Contradicted claims"
        />
        <StatCard
          title="Link Checks"
          value={stats.urlChecksCount}
          icon={LinkIcon}
          colorClass="bg-teal-500/10 text-teal-400"
          badgeText="🔗 Link"
          subtitle="URL safety checks"
        />
      </div>

      {/* Main Verification Input Section / Result */}
      {analyzing ? (
        <LoadingProgress />
      ) : analysisResult ? (
        <AnalysisResult result={analysisResult} onReset={handleReset} />
      ) : (
        <div className="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/80 shadow-2xl">
          
          <div className="text-center max-w-2xl mx-auto mb-8">
            <div className="w-12 h-12 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center mx-auto mb-3 text-teal-400">
              <ShieldCheck className="w-7 h-7" />
            </div>
            <h2 className="text-2xl font-bold text-white font-['Outfit']">What would you like to verify?</h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Submit text, web links, or a screenshot of a forwarded message in Kannada, Telugu, Tamil, Hindi, or English.
            </p>
          </div>

          {errorMessage && (
            <div className="mb-6 max-w-2xl mx-auto p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2.5">
              <AlertTriangle className="w-4 h-4 text-rose-400 flex-shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          {/* Input Method Tabs */}
          <div className="flex items-center justify-center gap-2 mb-6">
            <button
              onClick={() => setActiveInputTab('text')}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold transition-all ${
                activeInputTab === 'text'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/20'
                  : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              <FileText className="w-4 h-4" /> Text / Link Input
            </button>

            <button
              onClick={() => setActiveInputTab('screenshot')}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold transition-all ${
                activeInputTab === 'screenshot'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/20'
                  : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              <ImageIcon className="w-4 h-4" /> Screenshot + OCR Upload
            </button>
          </div>

          <form onSubmit={handleAnalyze} className="max-w-2xl mx-auto space-y-6">
            
            {activeInputTab === 'text' ? (
              <div>
                <textarea
                  rows="5"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Paste message, web URL link, viral claim, or news paragraph here (Supports Kannada, Telugu, Tamil, Hindi, English)..."
                  className="w-full p-4 rounded-2xl bg-slate-950/90 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all leading-relaxed"
                />
              </div>
            ) : (
              <div className="space-y-5">
                {/* Upload Drag & Drop Area */}
                <div className="border-2 border-dashed border-slate-800 hover:border-indigo-500/50 rounded-2xl p-6 text-center bg-slate-950/60 transition-all cursor-pointer relative">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                  <Upload className="w-8 h-8 text-indigo-400 mx-auto mb-2" />
                  <p className="text-sm font-semibold text-slate-200">
                    Click or drag WhatsApp screenshot to upload
                  </p>
                  <p className="text-xs text-slate-500 mt-1">PNG, JPG, WEBP up to 5MB (Supports English, Kannada, Telugu, Tamil, Hindi)</p>
                </div>

                {/* Screenshot Preview & OCR Progress */}
                {imagePreview && (
                  <div className="p-4 rounded-2xl bg-slate-950/90 border border-slate-800 flex flex-col sm:flex-row items-center gap-4">
                    <img
                      src={imagePreview}
                      alt="Uploaded Screenshot Preview"
                      className="w-24 h-24 object-cover rounded-xl border border-slate-800 flex-shrink-0"
                    />
                    <div className="space-y-1 text-left flex-1">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-teal-400 block">Screenshot Attached</span>
                        {ocrLoading && (
                          <span className="text-xs text-indigo-400 font-medium flex items-center gap-1.5 animate-pulse">
                            <Loader2 className="w-3.5 h-3.5 animate-spin" /> Extracting text...
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-slate-400">{imageFile?.name} ({(imageFile?.size / 1024).toFixed(1)} KB)</p>

                      {/* OCR Status Notice */}
                      {ocrStatus && (
                        <div className="pt-2">
                          {ocrStatus === 'success' ? (
                            <span className="text-[11px] font-semibold text-emerald-400 bg-emerald-950/60 border border-emerald-800/80 px-2.5 py-1 rounded-lg inline-flex items-center gap-1">
                              ✓ Text extracted successfully from screenshot
                            </span>
                          ) : (
                            <div className="text-[11px] text-amber-300 bg-amber-950/40 border border-amber-800/60 p-2 rounded-lg leading-relaxed">
                              ℹ️ {ocrMessage || 'Please review, type or edit text manually below.'}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Editable Extracted Text Area */}
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2 flex items-center justify-between">
                    <span>Text Extracted from Screenshot (Review / Edit below)</span>
                    <span className="text-[11px] text-indigo-400 font-normal">Editable</span>
                  </label>
                  <textarea
                    rows="4"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="OCR text will appear here automatically upon uploading screenshot. You can review, edit, or add missing text before verifying..."
                    className="w-full p-4 rounded-2xl bg-slate-950/90 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all leading-relaxed"
                  />
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={ocrLoading}
              className="w-full py-4 rounded-2xl bg-gradient-to-r from-indigo-500 via-blue-600 to-teal-500 hover:from-indigo-600 hover:to-teal-600 text-white font-bold text-base shadow-lg shadow-indigo-500/25 transition-all flex items-center justify-center gap-2 transform hover:-translate-y-0.5 disabled:opacity-50"
            >
              {ocrLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" /> Processing OCR...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" /> Analyze Content & Verify Link / Evidence
                </>
              )}
            </button>
          </form>

        </div>
      )}

      {/* Recent Verification History Table/Cards */}
      {!analysisResult && recentAnalyses.length > 0 && (
        <div className="glass-panel rounded-3xl p-6 border border-slate-800 bg-slate-900/60 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white font-['Outfit'] flex items-center gap-2">
              <HistoryIcon className="w-4 h-4 text-indigo-400" />
              Recent Verification History
            </h3>
            <button
              onClick={() => onNavigate('history')}
              className="text-xs text-indigo-400 font-semibold hover:text-indigo-300 flex items-center gap-1"
            >
              View All History <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recentAnalyses.map((item) => {
              const isUrlOnly = isUrlOnlyAnalysis(item);
              return (
                <div
                  key={item.id}
                  onClick={() => setAnalysisResult(item)}
                  className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800/80 hover:border-indigo-500/40 cursor-pointer transition-all flex flex-col justify-between space-y-2 group"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-semibold text-slate-400">
                      {new Date(item.created_at).toLocaleDateString()}
                    </span>
                    <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                      isUrlOnly
                        ? 'bg-teal-500/10 text-teal-400 border border-teal-500/30'
                        : item.assessment?.toLowerCase().includes('supported') || item.assessment?.toLowerCase().includes('ದೃಢೀಕರಿಸಲಾಗಿದೆ')
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                        : item.assessment?.toLowerCase().includes('misleading') || item.assessment?.toLowerCase().includes('ತಪ್ಪಿಸುವ')
                        ? 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
                        : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                    }`}>
                      {isUrlOnly ? `🔗 Link Check: ${item.assessment}` : item.assessment}
                    </span>
                  </div>

                  <p className="text-xs font-medium text-slate-200 line-clamp-2 leading-relaxed group-hover:text-indigo-300 transition-colors">
                    "{item.input_text}"
                  </p>

                  <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-900">
                    <span>Language: {item.detected_language || 'English'}</span>
                    {isUrlOnly || item.trust_score === null || item.trust_score === undefined ? (
                      <span className="font-bold text-teal-400 font-['Outfit']">Link Check Result</span>
                    ) : (
                      <span className="font-bold text-white font-['Outfit']">Trust Score: {item.trust_score}/100</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

    </div>
  );
}
