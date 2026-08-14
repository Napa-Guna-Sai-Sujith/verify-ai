import React from 'react';
import { ShieldCheck, User, LogOut, History as HistoryIcon, LayoutDashboard, Sparkles, Globe } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar({ activePage, setActivePage }) {
  const { user, profile, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    setActivePage('landing');
  };

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Tagline */}
          <div 
            className="flex items-center gap-3 cursor-pointer group"
            onClick={() => setActivePage(user ? 'dashboard' : 'landing')}
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-blue-500 to-teal-400 p-0.5 shadow-glow-indigo transition-transform group-hover:scale-105">
              <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <ShieldCheck className="w-6 h-6 text-teal-400" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-xl tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-slate-300 font-['Outfit']">
                  VERITY AI
                </span>
                <span className="text-[10px] font-semibold uppercase tracking-widest px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  Trust Engine
                </span>
              </div>
              <p className="text-xs text-slate-400 font-medium tracking-wide">
                "Check before you trust."
              </p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="flex items-center gap-2 sm:gap-4">
            {user ? (
              <>
                <button
                  onClick={() => setActivePage('dashboard')}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    activePage === 'dashboard'
                      ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                  }`}
                >
                  <LayoutDashboard className="w-4 h-4" />
                  <span className="hidden sm:inline">Dashboard</span>
                </button>

                <button
                  onClick={() => setActivePage('history')}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    activePage === 'history'
                      ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                  }`}
                >
                  <HistoryIcon className="w-4 h-4" />
                  <span className="hidden sm:inline">History</span>
                </button>

                <button
                  onClick={() => setActivePage('profile')}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    activePage === 'profile'
                      ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                  }`}
                >
                  <User className="w-4 h-4" />
                  <span className="hidden sm:inline">Profile</span>
                </button>

                <div className="h-4 w-[1px] bg-slate-800 mx-1 hidden sm:block"></div>

                <div className="flex items-center gap-3 pl-2">
                  <div className="hidden md:flex flex-col text-right">
                    <span className="text-xs font-semibold text-slate-200">
                      {profile?.full_name?.trim() ? profile.full_name.trim() : (profile?.email || user?.email || 'Account')}
                    </span>
                    <span className="text-[11px] text-teal-400 flex items-center justify-end gap-1">
                      <Globe className="w-3 h-3" />
                      {profile?.preferred_language || 'English'}
                    </span>
                  </div>

                  <button
                    onClick={handleLogout}
                    title="Logout"
                    className="p-2 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                  </button>
                </div>
              </>
            ) : (
              <>
                <button
                  onClick={() => setActivePage('landing')}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    activePage === 'landing' ? 'text-white font-semibold' : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  Home
                </button>

                <button
                  onClick={() => setActivePage('login')}
                  className="px-4 py-2 rounded-lg text-sm font-medium text-slate-200 hover:text-white hover:bg-slate-800/60 transition-all border border-slate-700/60"
                >
                  Sign In
                </button>

                <button
                  onClick={() => setActivePage('register')}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-semibold bg-gradient-to-r from-indigo-500 to-blue-600 hover:from-indigo-600 hover:to-blue-700 text-white shadow-md shadow-indigo-500/20 transition-all"
                >
                  <Sparkles className="w-4 h-4" />
                  Get Started
                </button>
              </>
            )}
          </nav>

        </div>
      </div>
    </header>
  );
}
