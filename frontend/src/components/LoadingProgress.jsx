import React, { useState, useEffect } from 'react';
import { CheckCircle2, Loader2, Search, FileText, Globe, Brain } from 'lucide-react';

export default function LoadingProgress() {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    { label: 'Reading content & extracting text', icon: FileText },
    { label: 'Detecting language & regional script', icon: Globe },
    { label: 'Checking official evidence & web sources', icon: Search },
    { label: 'Preparing trust assessment & explanation', icon: Brain },
  ];

  useEffect(() => {
    const timer1 = setTimeout(() => setCurrentStep(1), 1200);
    const timer2 = setTimeout(() => setCurrentStep(2), 2600);
    const timer3 = setTimeout(() => setCurrentStep(3), 4200);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
    };
  }, []);

  return (
    <div className="glass-panel rounded-2xl p-8 max-w-xl mx-auto my-8 border border-indigo-500/20 shadow-glow-indigo text-center">
      <div className="relative w-16 h-16 mx-auto mb-6 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border-4 border-indigo-500/20 animate-ping"></div>
        <div className="w-16 h-16 rounded-full bg-indigo-600/20 border-2 border-indigo-500 flex items-center justify-center">
          <Loader2 className="w-8 h-8 text-indigo-400 animate-spin" />
        </div>
      </div>

      <h3 className="text-xl font-bold text-white mb-2 font-['Outfit']">
        Verity AI Analysis Engine
      </h3>
      <p className="text-sm text-slate-400 mb-8">
        Analyzing digital content, extracting claims, and cross-referencing reliable evidence...
      </p>

      <div className="space-y-4 text-left max-w-md mx-auto">
        {steps.map((step, idx) => {
          const IconComponent = step.icon;
          const isDone = idx < currentStep;
          const isCurrent = idx === currentStep;

          return (
            <div
              key={idx}
              className={`flex items-center gap-3.5 p-3 rounded-xl transition-all duration-300 ${
                isCurrent
                  ? 'bg-indigo-600/20 border border-indigo-500/40 text-white shadow-sm'
                  : isDone
                  ? 'bg-slate-900/60 text-slate-300 border border-slate-800/60'
                  : 'opacity-40 text-slate-500'
              }`}
            >
              <div className="flex-shrink-0">
                {isDone ? (
                  <CheckCircle2 className="w-5 h-5 text-teal-400" />
                ) : isCurrent ? (
                  <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />
                ) : (
                  <IconComponent className="w-5 h-5 text-slate-500" />
                )}
              </div>
              <span className="text-sm font-medium">{step.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
