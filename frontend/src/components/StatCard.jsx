import React from 'react';

export default function StatCard({ title, value, icon: Icon, colorClass, badgeText, subtitle }) {
  return (
    <div className="glass-panel-interactive rounded-2xl p-5 border border-slate-800/80 relative overflow-hidden group">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          {title}
        </span>
        <div className={`p-2.5 rounded-xl ${colorClass}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>

      <div className="flex items-baseline gap-2">
        <span className="text-3xl font-extrabold text-white font-['Outfit'] tracking-tight">
          {value}
        </span>
        {badgeText && (
          <span className="text-[11px] font-medium text-slate-400 bg-slate-900 px-2 py-0.5 rounded-md border border-slate-800">
            {badgeText}
          </span>
        )}
      </div>

      {subtitle && (
        <p className="text-xs text-slate-500 mt-2 font-medium">{subtitle}</p>
      )}
    </div>
  );
}
