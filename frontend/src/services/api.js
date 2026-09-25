/**
 * API Service for Fraud Detection System backend communication.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

/**
 * Sends a transaction feature payload to the FastAPI prediction endpoint.
 * 
 * @param {Object} transactionData - Object containing 30 transaction features (Time, V1..V28, Amount).
 * @returns {Promise<Object>} Promise resolving to prediction response schema.
 */
export async function predictTransaction(transactionData) {
  const url = `${API_BASE_URL}/predict`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(transactionData),
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => null);
      const message = errorBody?.detail || `Server returned error status ${response.status}`;
      throw new Error(message);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error.message && (error.message.includes('fetch') || error.message.includes('Failed to fetch') || error.message.includes('NetworkError'))) {
      throw new Error("Unable to connect to prediction API. Please check that the backend server is running on " + API_BASE_URL);
    }
    throw error;
  }
}
