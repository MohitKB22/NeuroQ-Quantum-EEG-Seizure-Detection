/**
 * QEEG System - Global JavaScript Utilities
 */

// Format numbers with commas
function formatNumber(n) {
    return n.toLocaleString();
}

// Animate counter from 0 to value
function animateCounter(element, target, duration = 1500) {
    const start = performance.now();
    const isDecimal = target % 1 !== 0;
    
    function update(timestamp) {
        const elapsed = timestamp - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = eased * target;
        
        element.textContent = isDecimal ? current.toFixed(1) : Math.round(current);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Animate all metric values on page load
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.metric-value[data-target]').forEach(el => {
        const target = parseFloat(el.dataset.target);
        if (!isNaN(target)) {
            animateCounter(el, target);
        }
    });
});

// Plotly default config
window.defaultPlotlyConfig = {
    responsive: true,
    displayModeBar: false,
    staticPlot: false
};

window.darkPlotlyLayout = {
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { color: '#8ba0c4', size: 11, family: 'DM Sans, sans-serif' },
    xaxis: {
        gridcolor: 'rgba(30,45,71,0.5)',
        color: '#4a6080',
        linecolor: '#1e2d47'
    },
    yaxis: {
        gridcolor: 'rgba(30,45,71,0.4)',
        color: '#4a6080',
        linecolor: '#1e2d47'
    },
    margin: { t: 15, r: 15, b: 40, l: 50 }
};
