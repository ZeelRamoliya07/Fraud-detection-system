import React from 'react';

export default function Header() {
  return (
    <header className="border-b border-warm pb-6 mb-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-mono tracking-wider text-charcoal-muted uppercase mb-1">
            FRAUD DETECTION SYSTEM • v1.0
          </div>
          <h1 className="text-2xl sm:text-3xl font-serif text-charcoal-primary font-medium tracking-tight">
            Transaction Risk Analysis
          </h1>
          <p className="text-sm text-charcoal-secondary mt-1">
            Evaluate financial transactions using a leakage-free Random Forest pipeline with threshold-optimized decision scoring.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3 text-xs font-mono text-charcoal-secondary bg-warm-surface px-3 py-2 rounded border border-warm self-start sm:self-auto">
          <span>Model: <strong className="text-charcoal-primary font-semibold">Random Forest</strong></span>
          <span className="text-charcoal-muted">•</span>
          <span>Threshold: <strong className="text-charcoal-primary font-semibold">0.70</strong></span>
          <span className="text-charcoal-muted">•</span>
          <span className="inline-flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-600"></span>
            <span>API Ready</span>
          </span>
        </div>
      </div>
    </header>
  );
}
