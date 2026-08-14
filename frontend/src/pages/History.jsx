import React, { useState, useEffect } from 'react';
import { History as HistoryIcon, ShieldCheck, AlertTriangle, XCircle, Search, ExternalLink, Calendar, Filter, Trash2, Link as LinkIcon } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { fetchUserAnalyses } from '../services/api';
import AnalysisResult from '../components/AnalysisResult';
import { isUrlOnlyAnalysis, isNotRelevantAnalysis } from '../services/analysisHelpers';

export default function History() {
  const { user } = useAuth();
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [filterType, setFilterType] = useState('ALL');

  useEffect(() => {
    fetchHistory();
  }, [user]);

  const fetchHistory = async () => {
    if (!user) return;
    setLoading(true);
    try {
      const data = await fetchUserAnalyses(user.id);
      setAnalyses(data || []);
    } catch (err) {
      console.error('History fetch exception:', err);
    } finally {
      setLoading(false);
    }
  };

  const getBadgeStyle = (item) => {
    if (isUrlOnlyAnalysis(item)) return 'bg-teal-500/10 text-teal-400 border-teal-500/30';
    const assessment = item.assessment || '';
    if (assessment.toLowerCase().includes('supported')) return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    if (assessment.toLowerCase().includes('misleading') || assessment.toLowerCase().includes('fake')) return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
    return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
  };

  const filteredAnalyses = analyses.filter(item => {
    const isUrl = isUrlOnlyAnalysis(item);
    const isNotRel = isNotRelevantAnalysis(item);

    if (filterType === 'LINK_CHECKS') return isUrl;
    if (filterType === 'FACTUAL_CLAIMS') return !isUrl && !isNotRel;
    
    // When filtering by factual statuses, EXCLUDE URL-only checks!
    if (filterType === 'SUPPORTED') return !isUrl && item.assessment?.toLowerCase().includes('supported');
    if (filterType === 'VERIFICATION') return !isUrl && (item.assessment?.toLowerCase().includes('verification') || item.assessment?.toLowerCase().includes('needs'));
    if (filterType === 'MISLEADING') return !isUrl && (item.assessment?.toLowerCase().includes('misleading') || item.assessment?.toLowerCase().includes('fake'));
    
    return true;
  });

  return (
    <div className="max-w-6xl mx-auto my-8 px-4">
      
      {/* If an analysis item is selected to view full details */}
      {selectedAnalysis ? (
        <div>
          <button
            onClick={() => setSelectedAnalysis(null)}
            className="mb-4 text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800"
          >
            ← Back to History List
          </button>
          <AnalysisResult result={selectedAnalysis} onReset={() => setSelectedAnalysis(null)} />
        </div>
      ) : (
        <div className="space-y-6">
          
          {/* Header */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-slate-800">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
                <HistoryIcon className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white font-['Outfit']">Verification History</h2>
                <p className="text-xs text-slate-400">Your personal trust analysis archive secured by Neon PostgreSQL DB</p>
              </div>
            </div>

            {/* Filter Tabs */}
            <div className="flex flex-wrap items-center gap-1.5 p-1 rounded-xl bg-slate-900 border border-slate-800">
              {[
                { id: 'ALL', label: 'All Checks' },
                { id: 'FACTUAL_CLAIMS', label: 'Factual Messages' },
                { id: 'LINK_CHECKS', label: '🔗 Link Checks' },
                { id: 'SUPPORTED', label: 'Supported' },
                { id: 'VERIFICATION', label: 'Needs Verification' },
                { id: 'MISLEADING', label: 'Misleading' },
              ].map(f => (
                <button
                  key={f.id}
                  onClick={() => setFilterType(f.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    filterType === f.id ? 'bg-indigo-600 text-white font-semibold' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>

          {/* List Content */}
          {loading ? (
            <div className="text-center py-16 text-slate-400 text-sm">
              Loading your verification history...
            </div>
          ) : filteredAnalyses.length === 0 ? (
            <div className="glass-panel rounded-3xl p-12 text-center border border-slate-800 max-w-md mx-auto my-8">
              <Search className="w-12 h-12 text-slate-600 mx-auto mb-3" />
              <h3 className="text-lg font-bold text-white font-['Outfit'] mb-1">No Verifications Found</h3>
              <p className="text-xs text-slate-400 leading-relaxed mb-4">
                You haven't run any content checks in this category yet. Submit text or screenshots on the Dashboard to get started.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredAnalyses.map((item) => {
                const isUrl = isUrlOnlyAnalysis(item);
                return (
                  <div
                    key={item.id}
                    onClick={() => setSelectedAnalysis(item)}
                    className="glass-panel-interactive rounded-2xl p-5 border border-slate-800/80 cursor-pointer flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 group"
                  >
                    <div className="space-y-1.5 max-w-2xl">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className={`text-xs px-2.5 py-0.5 rounded-full border font-semibold ${getBadgeStyle(item)}`}>
                          {isUrl ? `🔗 Link Check: ${item.assessment}` : item.assessment}
                        </span>
                        <span className="text-[11px] px-2 py-0.5 rounded bg-slate-900 text-indigo-300 font-mono">
                          Language: {item.detected_language || 'English'}
                        </span>
                        <span className="text-[11px] text-slate-400 flex items-center gap-1">
                          <Calendar className="w-3 h-3 text-slate-500" />
                          {new Date(item.created_at).toLocaleDateString()}
                        </span>
                      </div>

                      <p className="text-sm font-medium text-slate-200 line-clamp-2 leading-relaxed group-hover:text-indigo-300 transition-colors">
                        "{item.input_text}"
                      </p>
                    </div>

                    <div className="flex items-center gap-4 self-end sm:self-center flex-shrink-0">
                      {isUrl || item.trust_score === null || item.trust_score === undefined ? (
                        <div className="text-right">
                          <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Verification</span>
                          <span className="text-sm font-bold text-teal-400 font-['Outfit']">Link Check</span>
                        </div>
                      ) : (
                        <div className="text-right">
                          <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Trust Score</span>
                          <span className="text-lg font-black text-white font-['Outfit']">{item.trust_score}/100</span>
                        </div>
                      )}
                      <ExternalLink className="w-4 h-4 text-slate-500 group-hover:text-indigo-400 transition-colors" />
                    </div>
                  </div>
                );
              })}
            </div>
          )}

        </div>
      )}

    </div>
  );
}
