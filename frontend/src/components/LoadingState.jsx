import React from 'react';

export default function LoadingState() {
  return (
    <div className="bg-warm-surface border border-warm rounded-sm p-8 text-center space-y-4">
      <div className="text-xs font-mono tracking-wider text-charcoal-muted uppercase">
        MODEL INFERENCE IN PROGRESS
      </div>
      <div className="inline-block w-6 h-6 border-2 border-charcoal-muted border-t-accent-rust rounded-full animate-spin"></div>
      <p className="text-xs text-charcoal-secondary font-mono">
        Transforming features & scoring Random Forest pipeline...
      </p>
    </div>
  );
}
