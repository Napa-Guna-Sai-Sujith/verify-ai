import React from 'react';
import { ShieldCheck, Languages, Lock, Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-800/80 bg-slate-950 mt-auto text-slate-400 text-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          
          <div className="space-y-3 md:col-span-2">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-teal-400" />
              <span className="font-bold text-white text-lg font-['Outfit']">VERITY AI</span>
            </div>
            <p className="text-slate-400 text-xs sm:text-sm max-w-md leading-relaxed">
              Verity AI is a multilingual Digital Trust platform designed to combat misinformation and misleading digital content, empowering users across regional Indian languages to verify facts before sharing.
            </p>
            <div className="flex flex-wrap items-center gap-2 pt-2">
              {['Kannada', 'Telugu', 'Tamil', 'Hindi', 'English'].map((lang) => (
                <span key={lang} className="text-xs px-2.5 py-1 rounded-md bg-slate-900 border border-slate-800 text-indigo-300 font-medium">
                  {lang}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-200 mb-3 flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-indigo-400" />
              Digital Trust Engine
            </h4>
            <ul className="space-y-2 text-xs">
              <li className="hover:text-slate-200 transition-colors">IDENTIFY claims</li>
              <li className="hover:text-slate-200 transition-colors">VERIFY official sources</li>
              <li className="hover:text-slate-200 transition-colors">UNDERSTAND explanations</li>
              <li className="hover:text-slate-200 transition-colors">RESPOND responsibly</li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-200 mb-3 flex items-center gap-1.5">
              <Languages className="w-3.5 h-3.5 text-teal-400" />
              Hackathon Project
            </h4>
            <p className="text-xs text-slate-400 leading-relaxed mb-2">
              Official Problem Statement: "How can technology help people identify, understand, and respond to misinformation and misleading content, especially in regional languages?"
            </p>
            <p className="text-xs text-slate-500">
              Built with React, Vite, Tailwind, Python FastAPI, Neon PostgreSQL & Tesseract OCR.
            </p>
          </div>

        </div>

        <div className="border-t border-slate-900 pt-6 flex flex-col sm:flex-row justify-between items-center text-xs text-slate-500 gap-4">
          <p>© {new Date().getFullYear()} Verity AI. All rights reserved. "Check before you trust."</p>
          <div className="flex items-center gap-1">
            <span>Built for Digital Trust & Safety</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
