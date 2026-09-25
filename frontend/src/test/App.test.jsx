import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import App from '../App';

describe('Fraud Detection System Frontend Component Tests', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders header, transaction form, and initial empty state', () => {
    render(<App />);

    expect(screen.getByText(/Transaction Risk Analysis/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Time/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Amount/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Analyze Transaction/i })).toBeInTheDocument();
    expect(screen.getByText(/No Transaction Analyzed Yet/i)).toBeInTheDocument();
  });

  it('populates sample fraud transaction when Sample Fraud button is clicked', () => {
    render(<App />);

    const sampleFraudBtn = screen.getByRole('button', { name: /Sample Fraud/i });
    fireEvent.click(sampleFraudBtn);

    const timeInput = screen.getByLabelText(/Time/i);
    expect(timeInput.value).toBe('406');
  });

  it('sends POST /predict request and renders prediction result on submit', async () => {
    const mockPrediction = {
      fraud_probability: 0.83,
      is_fraud: true,
      risk_level: 'HIGH',
      threshold: 0.70
    };

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockPrediction
    });

    render(<App />);

    const submitBtn = screen.getByRole('button', { name: /Analyze Transaction/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(1);
      expect(screen.getByText('83.00%')).toBeInTheDocument();
      expect(screen.getByText('FRAUD DETECTED')).toBeInTheDocument();
      expect(screen.getByText('HIGH RISK')).toBeInTheDocument();
      expect(screen.getByText('70% (0.70)')).toBeInTheDocument();
    });
  });

  it('renders user-friendly error message when API fetch fails', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('TypeError: Failed to fetch'));

    render(<App />);

    const submitBtn = screen.getByRole('button', { name: /Analyze Transaction/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByText(/Prediction Unavailable/i)).toBeInTheDocument();
      expect(screen.getByText(/Unable to connect to prediction API/i)).toBeInTheDocument();
    });
  });

  it('resets form and clears result when Reset button is clicked', async () => {
    const mockPrediction = {
      fraud_probability: 0.10,
      is_fraud: false,
      risk_level: 'LOW',
      threshold: 0.70
    };

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockPrediction
    });

    render(<App />);

    fireEvent.click(screen.getByRole('button', { name: /Analyze Transaction/i }));

    await waitFor(() => {
      expect(screen.getByText('10.00%')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /Reset Form/i }));

    expect(screen.getByText(/No Transaction Analyzed Yet/i)).toBeInTheDocument();
  });
});
