import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import History from './pages/History';

function MainLayout() {
  const { user, loading } = useAuth();
  const [activePage, setActivePage] = useState('landing');

  // Whenever user auth state changes:
  // - If user just logged IN and is on a public page → go to dashboard
  // - If user just logged OUT and is on a protected page → go to landing
  useEffect(() => {
    if (!loading) {
      if (user && ['landing', 'login', 'register'].includes(activePage)) {
        setActivePage('dashboard');
      } else if (!user && ['dashboard', 'profile', 'history'].includes(activePage)) {
        setActivePage('landing');
      }
    }
  }, [user, loading]);

  // Protect authenticated routes
  const handleNavigate = (page) => {
    if (!user && ['dashboard', 'profile', 'history'].includes(page)) {
      setActivePage('login');
      return;
    }
    setActivePage(page);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-300">
        <div className="text-center space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 animate-pulse mx-auto flex items-center justify-center text-teal-400 font-bold font-['Outfit']">
            V
          </div>
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Loading Verity AI Trust Engine...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 font-sans">
      <Navbar activePage={activePage} setActivePage={handleNavigate} />
      
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activePage === 'landing' && <Landing onNavigate={handleNavigate} />}
        {activePage === 'login' && <Login onNavigate={handleNavigate} />}
        {activePage === 'register' && <Register onNavigate={handleNavigate} />}
        {activePage === 'dashboard' && (user ? <Dashboard onNavigate={handleNavigate} /> : <Login onNavigate={handleNavigate} />)}
        {activePage === 'profile' && (user ? <Profile /> : <Login onNavigate={handleNavigate} />)}
        {activePage === 'history' && (user ? <History /> : <Login onNavigate={handleNavigate} />)}
      </main>

      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MainLayout />
    </AuthProvider>
  );
}
