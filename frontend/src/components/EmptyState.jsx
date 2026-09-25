import React from 'react';

export default function EmptyState() {
  return (
    <div className="bg-warm-surface border border-warm rounded-sm p-8 text-center space-y-3">
      <div className="text-xs font-mono tracking-wider text-charcoal-muted uppercase">
        03 • MODEL RESULT
      </div>
      <h3 className="text-lg font-serif text-charcoal-primary font-medium">
        No Transaction Analyzed Yet
      </h3>
      <p className="text-xs text-charcoal-secondary max-w-xs mx-auto leading-relaxed">
        Enter transaction details in the input panel on the left and click <strong className="text-charcoal-primary">Analyze Transaction</strong> to execute real-time model scoring.
      </p>
    </div>
  );
}
