import React, { useState } from 'react';
import Header from './components/Header';
import TransactionForm from './components/TransactionForm';
import PredictionResult from './components/PredictionResult';
import EmptyState from './components/EmptyState';
import LoadingState from './components/LoadingState';
import { predictTransaction } from './services/api';
import { SAMPLE_LEGIT, SAMPLE_FRAUD } from './services/sampleData';

const INITIAL_FORM_STATE = { ...SAMPLE_LEGIT };

export default function App() {
  const [formData, setFormData] = useState(INITIAL_FORM_STATE);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [validationErrors, setValidationErrors] = useState({});

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value === '' ? '' : parseFloat(value)
    }));

    if (validationErrors[name]) {
      setValidationErrors((prev) => ({ ...prev, [name]: null }));
    }
  };

  const handleLoadPreset = (type) => {
    if (type === 'FRAUD') {
      setFormData({ ...SAMPLE_FRAUD });
    } else {
      setFormData({ ...SAMPLE_LEGIT });
    }
    setValidationErrors({});
  };

  const handleReset = () => {
    setFormData({ ...SAMPLE_LEGIT });
    setResult(null);
    setError(null);
    setValidationErrors({});
  };

  const validateForm = () => {
    const errs = {};
    if (formData.Time === '' || isNaN(formData.Time) || formData.Time < 0) {
      errs.Time = 'Time must be a non-negative number';
    }
    if (formData.Amount === '' || isNaN(formData.Amount) || formData.Amount < 0) {
      errs.Amount = 'Amount must be a non-negative number';
    }
    for (let i = 1; i <= 28; i++) {
      const field = `V${i}`;
      if (formData[field] === '' || isNaN(formData[field])) {
        errs[field] = 'Must be a valid number';
      }
    }
    setValidationErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsLoading(true);
    setError(null);

    try {
      // Build clean float payload
      const payload = {};
      Object.keys(formData).forEach((key) => {
        payload[key] = parseFloat(formData[key]);
      });

      const prediction = await predictTransaction(payload);
      setResult(prediction);
    } catch (err) {
      setError(err.message || 'Unable to execute fraud prediction.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-warm-canvas text-charcoal-primary p-4 sm:p-8">
      <div className="max-w-6xl mx-auto">
        <Header />

        <main className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Transaction Input Form */}
          <div className="lg:col-span-7">
            <TransactionForm
              formData={formData}
              onChange={handleInputChange}
              onReset={handleReset}
              onSubmit={handleSubmit}
              onLoadPreset={handleLoadPreset}
              isLoading={isLoading}
              errors={validationErrors}
            />
          </div>

          {/* Right Column: Prediction Result / Status */}
          <div className="lg:col-span-5 space-y-4">
            {isLoading ? (
              <LoadingState />
            ) : error ? (
              <div className="bg-risk-high-subtle border border-risk-high rounded-sm p-6 space-y-3">
                <div className="text-xs font-mono font-bold text-risk-high uppercase">
                  API ERROR
                </div>
                <h3 className="text-sm font-semibold text-charcoal-primary">
                  Prediction Unavailable
                </h3>
                <p className="text-xs text-charcoal-secondary leading-relaxed">
                  {error}
                </p>
                <button
                  onClick={handleSubmit}
                  className="text-xs font-medium text-accent-rust hover:underline"
                >
                  Retry request
                </button>
              </div>
            ) : result ? (
              <PredictionResult result={result} />
            ) : (
              <EmptyState />
            )}
          </div>
        </main>

        <footer className="mt-12 pt-6 border-t border-warm text-center text-xs font-mono text-charcoal-muted">
          Random Forest fraud classification • Threshold optimized to 0.70 on evaluation set
        </footer>
      </div>
    </div>
  );
}
