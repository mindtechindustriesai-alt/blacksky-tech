/**
 * BLACKSKY-TECH API Client
 * Backend: https://blacksky-backend.onrender.com
 * IBM Verified: Job ID d55p3jgnsj9s73b32lj0 · 98.4% Correlation · CHSH S=2.76
 */

// API Configuration
const API_BASE = "https://blacksky-backend.onrender.com";
// For local testing, uncomment below:
// const API_BASE = "http://localhost:8000";

// Timeout for fetch requests (milliseconds)
const REQUEST_TIMEOUT = 10000;

/**
 * Generic fetch wrapper with timeout and error handling
 */
async function fetchWithTimeout(url, options = {}, timeout = REQUEST_TIMEOUT) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('Request timeout - backend may be sleeping. Please try again.');
        }
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Get service root information
 * GET /
 */
async function getServiceInfo() {
    return fetchWithTimeout(`${API_BASE}/`);
}

/**
 * Get health check status
 * GET /health
 */
async function getHealth() {
    return fetchWithTimeout(`${API_BASE}/health`);
}

/**
 * Get IBM quantum verification status
 * GET /quantum/status
 */
async function getQuantumStatus() {
    return fetchWithTimeout(`${API_BASE}/quantum/status`);
}

/**
 * Get BlackSky module performance targets
 * GET /quantum/blacksky-targets
 */
async function getBlackSkyTargets() {
    return fetchWithTimeout(`${API_BASE}/quantum/blacksky-targets`);
}

/**
 * Get patent information
 * GET /quantum/patent
 */
async function getPatentInfo() {
    return fetchWithTimeout(`${API_BASE}/quantum/patent`);
}

/**
 * Get portfolio valuation estimate
 * GET /quantum/valuation
 */
async function getValuation() {
    return fetchWithTimeout(`${API_BASE}/quantum/valuation`);
}

/**
 * Generate a commercial license
 * POST /license/generate
 * @param {Object} licenseData - License parameters
 */
async function generateLicense(licenseData) {
    return fetchWithTimeout(`${API_BASE}/license/generate`, {
        method: 'POST',
        body: JSON.stringify(licenseData)
    });
}

/**
 * Format valuation for display (USD)
 */
function formatValuationUSD(valuation) {
    if (valuation >= 1e9) {
        return `$${(valuation / 1e9).toFixed(1)}B`;
    }
    if (valuation >= 1e6) {
        return `$${(valuation / 1e6).toFixed(0)}M`;
    }
    return `$${valuation.toLocaleString()}`;
}

/**
 * Format valuation for display (ZAR)
 */
function formatValuationZAR(valuation) {
    if (valuation >= 1e9) {
        return `R${(valuation / 1e9).toFixed(1)}B`;
    }
    if (valuation >= 1e6) {
        return `R${(valuation / 1e6).toFixed(0)}M`;
    }
    return `R${valuation.toLocaleString()}`;
}

/**
 * Update UI with IBM verification data
 */
async function updateQuantumBadge() {
    try {
        const status = await getQuantumStatus();
        const ibmBadge = document.getElementById('ibmBadge');
        if (ibmBadge) {
            ibmBadge.innerHTML = `
                <div class="ibm-verified">
                    <span class="ibm-icon">⚛️</span>
                    <span class="ibm-job">IBM Verified · Job: ${status.job_id}</span>
                    <span class="ibm-correlation">${(status.correlation * 100).toFixed(1)}% Correlation</span>
                    <span class="ibm-chsh">CHSH S=${status.chsh_score}</span>
                </div>
            `;
        }
    } catch (error) {
        console.error('Failed to load quantum badge:', error);
    }
}

/**
 * Update UI with BlackSky targets
 */
async function updateBlackSkyTargets() {
    try {
        const targets = await getBlackSkyTargets();
        
        // Update CRYO-OS display
        const cryoElement = document.getElementById('cryoPerformance');
        if (cryoElement) {
            cryoElement.textContent = targets['CRYO-OS'].blacksky_target + 'x';
        }
        
        // Update GATE-SMOOTH display
        const gateElement = document.getElementById('gatePerformance');
        if (gateElement) {
            gateElement.textContent = targets['GATE-SMOOTH'].blacksky_target + '%';
        }
        
        // Update NODE-LINK display
        const nodeElement = document.getElementById('nodePerformance');
        if (nodeElement) {
            nodeElement.textContent = targets['NODE-LINK'].blacksky_target + 'M/s';
        }
    } catch (error) {
        console.error('Failed to load BlackSky targets:', error);
    }
}

/**
 * Update UI with valuation data
 */
async function updateValuation() {
    try {
        const valuation = await getValuation();
        const valuationElement = document.getElementById('portfolioValuation');
        if (valuationElement) {
            valuationElement.innerHTML = `
                <div class="valuation-range">
                    <span>${formatValuationUSD(valuation.valuation_usd.low)} - ${formatValuationUSD(valuation.valuation_usd.high)} USD</span>
                    <span>${formatValuationZAR(valuation.valuation_zar.low)} - ${formatValuationZAR(valuation.valuation_zar.high)} ZAR</span>
                </div>
            `;
        }
    } catch (error) {
        console.error('Failed to load valuation:', error);
    }
}

/**
 * Handle license generation from form data
 */
async function handleLicenseGeneration(formData) {
    const licenseData = {
        licensee_name: formData.licenseeName || 'Licensee Company',
        license_type: formData.licenseType || 'Annual',
        modules: formData.modules || ['CRYO-OS', 'GATE-SMOOTH', 'NODE-LINK'],
        jurisdiction: formData.jurisdiction || 'South Africa',
        exclusivity: formData.exclusivity || 'Non-Exclusive'
    };
    
    try {
        const result = await generateLicense(licenseData);
        return result;
    } catch (error) {
        console.error('License generation failed:', error);
        throw error;
    }
}

// Export functions for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getServiceInfo,
        getHealth,
        getQuantumStatus,
        getBlackSkyTargets,
        getPatentInfo,
        getValuation,
        generateLicense,
        formatValuationUSD,
        formatValuationZAR,
        updateQuantumBadge,
        updateBlackSkyTargets,
        updateValuation,
        handleLicenseGeneration
    };
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('BLACKSKY API Client loaded');
    console.log(`API Base: ${API_BASE}`);
    console.log('IBM Verified: Job d55p3jgnsj9s73b32lj0 · 98.4% Correlation · CHSH S=2.76');
    
    // Initialize UI components if they exist
    updateQuantumBadge();
    updateBlackSkyTargets();
    updateValuation();
});
