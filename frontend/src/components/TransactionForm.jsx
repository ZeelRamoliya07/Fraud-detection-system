import React from 'react';

export default function TransactionForm({
  formData,
  onChange,
  onReset,
  onSubmit,
  onLoadPreset,
  isLoading,
  errors
}) {
  return (
    <form onSubmit={onSubmit} className="bg-warm-surface border border-warm rounded-sm p-5 space-y-6">
      <div className="flex items-center justify-between border-b border-warm pb-3">
        <span className="text-xs font-mono font-semibold tracking-wider text-charcoal-secondary uppercase">
          01 • TRANSACTION INPUTS
        </span>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => onLoadPreset('LEGIT')}
            disabled={isLoading}
            className="text-xs text-charcoal-secondary hover:text-charcoal-primary bg-warm-panel hover:bg-warm-canvas border border-warm px-2.5 py-1 rounded-sm transition-colors"
          >
            Sample Normal
          </button>
          <button
            type="button"
            onClick={() => onLoadPreset('FRAUD')}
            disabled={isLoading}
            className="text-xs text-accent-rust hover:text-red-700 bg-warm-panel hover:bg-warm-canvas border border-warm px-2.5 py-1 rounded-sm font-medium transition-colors"
          >
            Sample Fraud
          </button>
        </div>
      </div>

      {/* Transaction Info Section */}
      <div>
        <h3 className="text-xs font-mono font-medium text-charcoal-secondary uppercase mb-3">
          Transaction Overview
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label htmlFor="input-Time" className="block text-xs font-medium text-charcoal-primary mb-1">
              Time (Seconds since first transaction) <span className="text-red-600">*</span>
            </label>
            <input
              id="input-Time"
              type="number"
              step="any"
              name="Time"
              value={formData.Time}
              onChange={onChange}
              required
              min="0"
              disabled={isLoading}
              className={`w-full bg-warm-canvas border text-sm px-3 py-1.5 rounded-sm focus:outline-none focus:border-charcoal-primary ${
                errors.Time ? 'border-red-600' : 'border-warm-dark'
              }`}
              placeholder="e.g. 406.0"
            />
            {errors.Time && <span className="text-xs text-red-600 mt-1 block">{errors.Time}</span>}
          </div>

          <div>
            <label htmlFor="input-Amount" className="block text-xs font-medium text-charcoal-primary mb-1">
              Amount ($ USD) <span className="text-red-600">*</span>
            </label>
            <input
              id="input-Amount"
              type="number"
              step="any"
              name="Amount"
              value={formData.Amount}
              onChange={onChange}
              required
              min="0"
              disabled={isLoading}
              className={`w-full bg-warm-canvas border text-sm px-3 py-1.5 rounded-sm focus:outline-none focus:border-charcoal-primary ${
                errors.Amount ? 'border-red-600' : 'border-warm-dark'
              }`}
              placeholder="e.g. 100.0"
            />
            {errors.Amount && <span className="text-xs text-red-600 mt-1 block">{errors.Amount}</span>}
          </div>
        </div>
      </div>

      {/* Feature Grid Section */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-xs font-mono font-medium text-charcoal-secondary uppercase">
            02 • PCA Features (V1 – V28)
          </h3>
          <span className="text-xs text-charcoal-muted">Numeric continuous features</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          {Array.from({ length: 28 }, (_, i) => i + 1).map((num) => {
            const fieldName = `V${num}`;
            return (
              <div key={fieldName} className="bg-warm-canvas p-2 rounded-sm border border-warm">
                <label htmlFor={`input-${fieldName}`} className="block text-[11px] font-mono text-charcoal-secondary mb-0.5">
                  {fieldName}
                </label>
                <input
                  id={`input-${fieldName}`}
                  type="number"
                  step="any"
                  name={fieldName}
                  value={formData[fieldName]}
                  onChange={onChange}
                  required
                  disabled={isLoading}
                  className="w-full bg-transparent text-xs text-charcoal-primary font-mono focus:outline-none"
                />
              </div>
            );
          })}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center justify-end gap-3 pt-3 border-t border-warm">
        <button
          type="button"
          onClick={onReset}
          disabled={isLoading}
          className="text-xs text-charcoal-secondary hover:text-charcoal-primary px-4 py-2 border border-warm hover:border-warm-dark rounded-sm transition-colors"
        >
          Reset Form
        </button>

        <button
          type="submit"
          disabled={isLoading}
          className="text-xs font-semibold text-white bg-accent-rust hover:bg-amber-700 disabled:opacity-50 px-5 py-2 rounded-sm shadow-sm transition-colors"
        >
          {isLoading ? 'Analyzing...' : 'Analyze Transaction'}
        </button>
      </div>
    </form>
  );
}
