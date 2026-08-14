import React from 'react';
import { 
  ShieldCheck, 
  Search, 
  Brain, 
  CheckSquare, 
  Languages, 
  FileSearch, 
  Volume2, 
  ArrowRight, 
  Lock, 
  Sparkles,
  Award
} from 'lucide-react';

export default function Landing({ onNavigate }) {
  return (
    <div className="space-y-20 pb-16">
      
      {/* HERO SECTION */}
      <section className="relative pt-12 pb-16 sm:pt-20 sm:pb-24 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/30 via-slate-950 to-slate-950 -z-10"></div>
        <div className="max-w-5xl mx-auto px-4 text-center">
          
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold uppercase tracking-widest mb-6 shadow-glow-indigo">
            <Sparkles className="w-3.5 h-3.5 text-teal-400" />
            Multilingual Digital Trust Platform
          </div>

          {/* Title & Tagline */}
          <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white font-['Outfit'] leading-tight mb-4">
            Check before you trust.
          </h1>
          <p className="text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto font-normal leading-relaxed mb-8">
            Understand digital information before you believe it or share it. Instant claim verification & explainable AI across Indian regional languages.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto">
            <button
              onClick={() => onNavigate('register')}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-indigo-500 via-blue-600 to-teal-500 hover:from-indigo-600 hover:to-teal-600 text-white font-bold text-base shadow-lg shadow-indigo-500/25 transition-all transform hover:-translate-y-0.5 flex items-center justify-center gap-2"
            >
              Start Verifying Content <ArrowRight className="w-5 h-5" />
            </button>
            
            <button
              onClick={() => onNavigate('login')}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 font-semibold text-base border border-slate-700 transition-all"
            >
              Sign In to Account
            </button>
          </div>

          {/* Core Workflow Visual Flow */}
          <div className="mt-16 pt-12 border-t border-slate-800/80">
            <span className="text-xs font-bold uppercase tracking-widest text-slate-400 block mb-6">
              THE VERITY AI DIGITAL TRUST PIPELINE
            </span>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              
              <div className="glass-panel rounded-2xl p-4 text-center border border-slate-800">
                <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center mx-auto mb-2 font-bold text-sm">
                  01
                </div>
                <h4 className="font-bold text-white text-sm font-['Outfit']">IDENTIFY</h4>
                <p className="text-[11px] text-slate-400 mt-1">Extract factual claims from text or WhatsApp screenshots</p>
              </div>

              <div className="glass-panel rounded-2xl p-4 text-center border border-slate-800">
                <div className="w-10 h-10 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center mx-auto mb-2 font-bold text-sm">
                  02
                </div>
                <h4 className="font-bold text-white text-sm font-['Outfit']">VERIFY</h4>
                <p className="text-[11px] text-slate-400 mt-1">Cross-check official government & news evidence</p>
              </div>

              <div className="glass-panel rounded-2xl p-4 text-center border border-slate-800">
                <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center mx-auto mb-2 font-bold text-sm">
                  03
                </div>
                <h4 className="font-bold text-white text-sm font-['Outfit']">UNDERSTAND</h4>
                <p className="text-[11px] text-slate-400 mt-1">Non-technical human reasoning & voice read aloud</p>
              </div>

              <div className="glass-panel rounded-2xl p-4 text-center border border-slate-800">
                <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto mb-2 font-bold text-sm">
                  04
                </div>
                <h4 className="font-bold text-white text-sm font-['Outfit']">RESPOND</h4>
                <p className="text-[11px] text-slate-400 mt-1">Actionable guidance before sharing on social media</p>
              </div>

            </div>
          </div>

        </div>
      </section>

      {/* PROBLEM & SOLUTION SECTION */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          
          <div className="glass-panel rounded-3xl p-8 border border-rose-500/20 bg-gradient-to-b from-slate-900 to-slate-950">
            <div className="w-10 h-10 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 flex items-center justify-center mb-4">
              <Lock className="w-5 h-5" />
            </div>
            <h2 className="text-2xl font-bold text-white font-['Outfit'] mb-3">
              The Problem: Misinformation in Regional Languages
            </h2>
            <p className="text-slate-300 text-sm leading-relaxed mb-4">
              Millions of citizens receive unverified viral messages, fake government scheme circulars, and panic-inducing health alerts on messaging apps in Kannada, Telugu, Tamil, and Hindi every day.
            </p>
            <ul className="space-y-2 text-xs text-slate-400">
              <li className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-rose-400"></span>
                Language barriers prevent non-English speakers from fact-checking.
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-rose-400"></span>
                Generic AI tools output binary "FAKE" claims without evidence explanations.
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-rose-400"></span>
                Users lack clear guidance on how to respond responsibly before forwarding.
              </li>
            </ul>
          </div>

          <div className="glass-panel rounded-3xl p-8 border border-teal-500/20 bg-gradient-to-b from-slate-900 to-slate-950 shadow-glow-teal">
            <div className="w-10 h-10 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center mb-4">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h2 className="text-2xl font-bold text-white font-['Outfit'] mb-3">
              The Solution: Verity AI Digital Trust Engine
            </h2>
            <p className="text-slate-300 text-sm leading-relaxed mb-4">
              Verity AI provides transparent evidence-backed trust assessments. We don't blindly label content; we explain the exact signals and provide official source links.
            </p>
            <ul className="space-y-2 text-xs text-slate-300">
              <li className="flex items-center gap-2">
                <CheckSquare className="w-4 h-4 text-teal-400 flex-shrink-0" />
                Supports text & WhatsApp screenshot uploads via Tesseract OCR.
              </li>
              <li className="flex items-center gap-2">
                <CheckSquare className="w-4 h-4 text-teal-400 flex-shrink-0" />
                Live language detection for Kannada, Telugu, Tamil, Hindi, and English.
              </li>
              <li className="flex items-center gap-2">
                <CheckSquare className="w-4 h-4 text-teal-400 flex-shrink-0" />
                Browser voice explanation (Text-to-Speech) for accessible listening.
              </li>
            </ul>
          </div>

        </div>
      </section>

      {/* REGIONAL LANGUAGE FOCUS */}
      <section className="max-w-6xl mx-auto px-4">
        <div className="glass-panel rounded-3xl p-8 border border-indigo-500/20 bg-slate-900/60 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-300 text-xs font-semibold mb-4">
            <Languages className="w-4 h-4 text-teal-400" />
            Built for Multilingual Accessibility
          </div>
          <h2 className="text-3xl font-extrabold text-white font-['Outfit'] mb-2">
            First-Class Regional Language Support
          </h2>
          <p className="text-slate-400 text-sm max-w-xl mx-auto mb-8">
            Verity AI analyzes Indian regional language scripts directly and provides explanations in your preferred mother tongue.
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
            {[
              { lang: 'Kannada', script: 'ಕನ್ನಡ', desc: 'Full script recognition & evidence check' },
              { lang: 'Telugu', script: 'తెలుగు', desc: 'Claim extraction & official source matching' },
              { lang: 'Tamil', script: 'தமிழ்', desc: 'Regional language detection & voice readout' },
              { lang: 'Hindi', script: 'हिंदी', desc: 'Government circular & news cross-reference' },
              { lang: 'English', script: 'English', desc: 'Global digital trust & fact-checking' },
            ].map((item, i) => (
              <div key={i} className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 text-center hover:border-indigo-500/40 transition-colors">
                <span className="text-2xl font-bold text-indigo-300 block mb-1 font-['Outfit']">{item.script}</span>
                <span className="text-xs font-bold text-white block mb-1">{item.lang}</span>
                <span className="text-[10px] text-slate-400 block leading-tight">{item.desc}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* KEY FEATURES GRID */}
      <section className="max-w-6xl mx-auto px-4">
        <h2 className="text-3xl font-extrabold text-white font-['Outfit'] text-center mb-8">
          Core Digital Trust Capabilities
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div className="glass-panel-interactive rounded-2xl p-6 border border-slate-800">
            <FileSearch className="w-8 h-8 text-indigo-400 mb-4" />
            <h3 className="text-lg font-bold text-white font-['Outfit'] mb-2">Screenshot OCR</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Upload forwarded WhatsApp messages or social media images. Tesseract OCR extracts text cleanly before running analysis.
            </p>
          </div>

          <div className="glass-panel-interactive rounded-2xl p-6 border border-slate-800">
            <Search className="w-8 h-8 text-teal-400 mb-4" />
            <h3 className="text-lg font-bold text-white font-['Outfit'] mb-2">Evidence Verification</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Searches government portals, PIB, fact-checkers, and reputable news outlets to verify extracted factual claims.
            </p>
          </div>

          <div className="glass-panel-interactive rounded-2xl p-6 border border-slate-800">
            <Volume2 className="w-8 h-8 text-amber-400 mb-4" />
            <h3 className="text-lg font-bold text-white font-['Outfit'] mb-2">Voice Read Aloud</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Listen to the trust assessment and recommended action in your preferred language using browser text-to-speech.
            </p>
          </div>

        </div>
      </section>

      {/* PROJECT / TEAM INFO */}
      <section className="max-w-4xl mx-auto px-4 text-center">
        <div className="glass-panel rounded-2xl p-6 border border-slate-800 bg-slate-950/80">
          <div className="flex items-center justify-center gap-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <Award className="w-4 h-4 text-teal-400" /> Hackathon Project Submission
          </div>
          <h3 className="text-lg font-bold text-white font-['Outfit'] mb-2">Verity AI Engineering Team</h3>
          <p className="text-xs text-slate-400 max-w-xl mx-auto">
            Developed for the Digital Trust hackathon. Built using React, Vite, Tailwind CSS, Python FastAPI, Neon PostgreSQL & Tesseract OCR.
          </p>
        </div>
      </section>

    </div>
  );
}
