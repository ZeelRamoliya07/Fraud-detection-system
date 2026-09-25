import React from 'react';

export default function PredictionResult({ result }) {
  if (!result) return null;

  const { fraud_probability, is_fraud, risk_level, threshold } = result;

  // Format percentage to 2 decimal places
  const probaPct = (fraud_probability * 100).toFixed(2);
  const thresholdPct = (threshold * 100).toFixed(0);

  // Restrained risk badge styling
  let riskBadgeClass = "bg-risk-low-subtle text-risk-low border-risk-low";
  let statusColorClass = "text-emerald-800";
  let statusText = "LEGITIMATE TRANSACTION";

  if (risk_level === 'HIGH') {
    riskBadgeClass = "bg-risk-high-subtle text-risk-high border-risk-high";
    statusColorClass = "text-red-800";
    statusText = "FRAUD DETECTED";
  } else if (risk_level === 'MEDIUM') {
    riskBadgeClass = "bg-risk-medium-subtle text-risk-medium border-risk-medium";
    statusColorClass = "text-amber-800";
    statusText = "SUSPICIOUS ACTIVITY";
  }

  return (
    <div className="bg-warm-surface border border-warm rounded-sm p-6 space-y-6">
      <div className="flex items-center justify-between border-b border-warm pb-3">
        <span className="text-xs font-mono font-semibold tracking-wider text-charcoal-secondary uppercase">
          03 • MODEL RESULT
        </span>
        <span className={`text-xs font-mono font-bold px-2.5 py-0.5 border rounded-sm ${riskBadgeClass}`}>
          {risk_level} RISK
        </span>
      </div>

      {/* Probability Focus Block */}
      <div className="space-y-1">
        <div className="text-xs font-mono text-charcoal-secondary uppercase tracking-wide">
          Estimated Fraud Probability
        </div>
        <div className="text-4xl sm:text-5xl font-serif text-charcoal-primary font-normal tracking-tight">
          {probaPct}%
        </div>
      </div>

      {/* Decision Status Box */}
      <div className={`p-4 border rounded-sm ${is_fraud ? 'bg-risk-high-subtle' : 'bg-risk-low-subtle'}`}>
        <div className="text-xs font-mono text-charcoal-secondary uppercase mb-1">
          Classification Outcome
        </div>
        <div className={`text-base font-bold tracking-wide ${statusColorClass}`}>
          {statusText}
        </div>
        <p className="text-xs text-charcoal-secondary mt-1">
          {is_fraud
            ? `Estimated fraud probability (${probaPct}%) exceeds the ${thresholdPct}% decision threshold.`
            : `Estimated fraud probability (${probaPct}%) is below the ${thresholdPct}% decision threshold.`}
        </p>
      </div>

      {/* Model Metadata Grid */}
      <div className="grid grid-cols-2 gap-3 pt-2 text-xs font-mono border-t border-warm">
        <div className="bg-warm-canvas p-2.5 rounded-sm border border-warm">
          <div className="text-charcoal-muted uppercase text-[10px]">Operational Threshold</div>
          <div className="text-charcoal-primary font-bold mt-0.5">{thresholdPct}% (0.70)</div>
        </div>

        <div className="bg-warm-canvas p-2.5 rounded-sm border border-warm">
          <div className="text-charcoal-muted uppercase text-[10px]">Risk Tier Mapping</div>
          <div className="text-charcoal-primary font-bold mt-0.5">{risk_level} Risk</div>
        </div>
      </div>

      <div className="text-[11px] text-charcoal-muted leading-relaxed font-sans border-t border-warm pt-3">
        * Risk levels and binary decisions are evaluated at threshold {thresholdPct}% by the serialized Random Forest pipeline.
      </div>
    </div>
  );
}
