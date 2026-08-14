import React, { useState } from 'react';
import { ShieldCheck, Mail, Lock, ArrowRight, AlertCircle, CheckCircle2, Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Login({ onNavigate }) {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    if (!email || !password) {
      setError('Please enter both email and password.');
      return;
    }

    try {
      setSubmitting(true);
      await login({ email, password });
      setSuccess(true);
      // Small delay so user sees the success flash, then App.jsx useEffect handles redirect
      setTimeout(() => onNavigate('dashboard'), 300);
    } catch (err) {
      console.error('Login error:', err);
      setError(err.message || 'Sign in failed. Please check your credentials and try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-md mx-auto my-12 px-4">
      <div className="glass-panel rounded-3xl p-8 border border-slate-800 bg-slate-900/80 shadow-2xl">

        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center mx-auto mb-3 text-teal-400">
            <ShieldCheck className="w-7 h-7" />
          </div>
          <h2 className="text-2xl font-bold text-white font-['Outfit']">Sign In to Verity AI</h2>
          <p className="text-xs text-slate-400 mt-1">Access your Digital Trust dashboard & analysis history</p>
        </div>

        {/* Error Banner */}
        {error && (
          <div className="mb-6 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-start gap-2.5">
            <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Success Banner */}
        {success && (
          <div className="mb-6 p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span>Sign in successful! Redirecting to dashboard...</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                autoComplete="email"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                autoComplete="current-password"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting || success}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-blue-600 hover:from-indigo-600 hover:to-blue-700 text-white font-bold text-sm shadow-md shadow-indigo-500/20 transition-all flex items-center justify-center gap-2 disabled:opacity-60"
          >
            {submitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" /> Authenticating...
              </>
            ) : success ? (
              <>
                <CheckCircle2 className="w-4 h-4" /> Signed In!
              </>
            ) : (
              <>
                Sign In <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="mt-6 pt-6 border-t border-slate-800 text-center text-xs text-slate-400">
          Don't have an account?{' '}
          <button
            onClick={() => onNavigate('register')}
            className="text-indigo-400 font-semibold hover:text-indigo-300 transition-colors"
          >
            Register Here
          </button>
        </div>

      </div>
    </div>
  );
}
