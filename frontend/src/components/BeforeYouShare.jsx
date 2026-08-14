import React from 'react';
import { ShieldAlert, CheckSquare } from 'lucide-react';
import { getTranslation } from '../services/localization';

export default function BeforeYouShare({ items: customItems, language = 'English' }) {
  const defaultItems = [
    {
      title: "Do I know the original source?",
      desc: "Check if the message originates from an official domain or reputable publisher rather than forwarded social media messages."
    },
    {
      title: "Is there reliable supporting evidence?",
      desc: "Cross-reference claims with official government portals (e.g., PIB, State circulars) or established fact-checking outlets."
    },
    {
      title: "Is the information current & timely?",
      desc: "Misinformation often recycles outdated news, old videos, or previous year circulars to trigger false panic."
    },
    {
      title: "Is the message pressuring immediate sharing?",
      desc: "Urgent call-to-actions ('Share with 10 groups immediately!') are a primary red flag of viral digital deception."
    }
  ];

  const items = customItems || defaultItems;

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-800 bg-slate-900/60 mt-8">
      <div className="flex items-center gap-3 mb-4 pb-3 border-b border-slate-800">
        <div className="w-9 h-9 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center">
          <ShieldAlert className="w-5 h-5 text-amber-400" />
        </div>
        <div>
          <h3 className="text-base font-bold text-white font-['Outfit'] flex items-center gap-2">
            {getTranslation(language, 'before_you_share_title')}
          </h3>
          <p className="text-xs text-slate-400">
            Digital Trust Checklist ({language})
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {items.map((item, index) => (
          <div key={index} className="flex items-start gap-3 p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <CheckSquare className="w-4 h-4 text-teal-400 mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="text-xs font-semibold text-slate-200 mb-1">{item.title}</h4>
              <p className="text-[11px] text-slate-400 leading-relaxed">{item.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
