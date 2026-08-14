import React, { useState } from 'react';
import { User, Mail, Globe, Save, CheckCircle2, AlertCircle, Loader2, Shield } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Profile() {
  const { user, profile, updateProfile } = useAuth();
  
  const [fullName, setFullName] = useState(profile?.full_name || '');
  const [preferredLanguage, setPreferredLanguage] = useState(profile?.preferred_language || 'English');
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  React.useEffect(() => {
    if (profile) {
      setFullName(profile.full_name || '');
      if (profile.preferred_language) {
        setPreferredLanguage(profile.preferred_language);
      }
    }
  }, [profile]);

  const handleSave = async (e) => {
    e.preventDefault();
    setSuccessMsg(null);
    setErrorMsg(null);

    try {
      setSaving(true);
      await updateProfile({
        fullName,
        preferredLanguage,
      });
      setSuccessMsg('Profile updated successfully!');
      setTimeout(() => setSuccessMsg(null), 4000);
    } catch (err) {
      console.error('Profile update failed:', err);
      setErrorMsg(err.message || 'Failed to update profile.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto my-8 px-4">
      <div className="glass-panel rounded-3xl p-8 border border-slate-800 bg-slate-900/80 shadow-2xl">
        
        {/* Header */}
        <div className="flex items-center gap-4 mb-8 pb-6 border-b border-slate-800">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-teal-400 p-0.5 shadow-glow-indigo">
            <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center text-teal-400">
              <User className="w-7 h-7" />
            </div>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white font-['Outfit']">User Profile & Settings</h2>
            <p className="text-xs text-slate-400">Manage account information & regional language preferences</p>
          </div>
        </div>

        {successMsg && (
          <div className="mb-6 p-3.5 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-300 text-xs flex items-center gap-2.5">
            <CheckCircle2 className="w-4 h-4 text-teal-400 flex-shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {errorMsg && (
          <div className="mb-6 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2.5">
            <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-6">
          
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
              Full Name
            </label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-slate-100 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
              Email Address (Account ID)
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              <input
                type="email"
                value={profile?.email || user?.email || ''}
                disabled
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/40 border border-slate-900 text-slate-400 text-sm cursor-not-allowed"
              />
            </div>
            <p className="text-[11px] text-slate-500 mt-1">Managed securely by Neon PostgreSQL Database</p>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
              Preferred Language for Analysis & Voice Read Aloud
            </label>
            <div className="relative">
              <Globe className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5 pointer-events-none" />
              <select
                value={preferredLanguage}
                onChange={(e) => setPreferredLanguage(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-slate-100 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all appearance-none cursor-pointer"
              >
                <option value="English">English</option>
                <option value="Kannada">Kannada (ಕನ್ನಡ)</option>
                <option value="Telugu">Telugu (తెలుగు)</option>
                <option value="Tamil">Tamil (தமிழ்)</option>
                <option value="Hindi">Hindi (हिंदी)</option>
              </select>
            </div>
          </div>

          {/* Account Details Box */}
          <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-2 text-xs">
            <div className="flex items-center gap-2 text-slate-300 font-semibold mb-1">
              <Shield className="w-4 h-4 text-teal-400" /> Account Security & Direct Neon DB Connection
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Account User ID:</span>
              <span className="font-mono text-slate-300">{user?.id?.slice(0, 18)}...</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Member Since:</span>
              <span>{profile?.created_at ? new Date(profile.created_at).toLocaleDateString() : 'Active User'}</span>
            </div>
          </div>

          <button
            type="submit"
            disabled={saving}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-teal-500 hover:from-indigo-600 hover:to-teal-600 text-white font-bold text-sm shadow-md shadow-indigo-500/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {saving ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" /> Saving Changes...
              </>
            ) : (
              <>
                <Save className="w-4 h-4" /> Save Profile Preferences
              </>
            )}
          </button>
        </form>

      </div>
    </div>
  );
}
