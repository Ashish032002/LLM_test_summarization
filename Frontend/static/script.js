// Frontend/static/js/script.js

// API Configuration
const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:8000',
    ENDPOINTS: {
        SUMMARIZE: '/summarize'
    }
};

// UI Elements
const elements = {
    textarea: document.getElementById('input-text'),
    summarizeBtn: document.getElementById('summarize-btn'),
    loading: document.getElementById('loading'),
    error: document.getElementById('error'),
    summary: document.getElementById('summary'),
    resultsCard: document.getElementById('results-card'),
    originalLength: document.getElementById('original-length'),
    summaryLength: document.getElementById('summary-length'),
    processingTime: document.getElementById('processing-time')
};

// Input validation
function validateInput(text) {
    if (!text) {
        throw new Error('Please enter some text to summarize.');
    }
    if (text.length < 100) {
        throw new Error('Please enter at least 100 characters for better results.');
    }
}

// Update UI state
function updateUIState(state) {
    elements.summarizeBtn.disabled = state === 'loading';
    elements.loading.style.display = state === 'loading' ? 'block' : 'none';
    elements.error.style.display = state === 'error' ? 'block' : 'none';
    elements.resultsCard.style.display = state === 'success' ? 'block' : 'none';
}

// Show error message
function showError(message) {
    elements.error.textContent = message;
    elements.error.style.display = 'block';
    setTimeout(() => {
        elements.error.style.display = 'none';
    }, 5000);
}

// Format numbers
function formatNumber(num) {
    return num.toLocaleString();
}

// Update statistics
function updateStats(originalText, summary, processingTime) {
    elements.originalLength.textContent = formatNumber(originalText.split(/\s+/).length);
    elements.summaryLength.textContent = formatNumber(summary.split(/\s+/).length);
    elements.processingTime.textContent = processingTime.toFixed(1);
}

// Main summarization function
async function summarizeText() {
    const inputText = elements.textarea.value.trim();

    try {
        // Validate input
        validateInput(inputText);

        // Update UI - Loading state
        updateUIState('loading');

        // Get parameters
        const maxLength = document.getElementById('max-length').value;
        const minLength = document.getElementById('min-length').value;
        const numBeams = document.getElementById('num-beams').value;

        // Make API request
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.SUMMARIZE}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                text: inputText,
                max_length: parseInt(maxLength),
                min_length: parseInt(minLength),
                num_beams: parseInt(numBeams)
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to get summary');
        }

        // Process response
        const data = await response.json();

        // Update UI - Success state
        elements.summary.textContent = data.summary;
        updateStats(inputText, data.summary, data.processing_time);
        updateUIState('success');

        // Smooth scroll to results
        elements.resultsCard.scrollIntoView({ behavior: 'smooth' });

    } catch (err) {
        // Update UI - Error state
        updateUIState('error');
        showError(err.message);
        console.error('Error:', err);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Character count validation
    elements.textarea.addEventListener('input', function() {
        const charCount = this.value.trim().length;
        elements.summarizeBtn.disabled = charCount < 100;
    });

    // Parameter validation
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('change', function() {
            const value = parseInt(this.value);
            const min = parseInt(this.min);
            const max = parseInt(this.max);

            if (value < min) this.value = min;
            if (value > max) this.value = max;
        });
    });
});