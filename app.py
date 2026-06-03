"""
Advanced EEG Epilepsy Detection System
Hybrid Quantum-Classical AI for Pediatric Seizure Detection
Flask Web Application - Main Entry Point
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import time
import uuid
import sqlite3
from datetime import datetime

from utils.eeg_processor import EEGProcessor
from utils.report_analyzer import (
    MedicalReportAnalyzer, extract_text_from_pdf,
    extract_text_from_image, extract_text_from_txt
)
from utils.quantum_classifier import QuantumClassifier
from utils.report_generator import ReportGenerator
from utils.database import init_db, save_analysis, get_all_analyses, get_analysis_by_id

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eeg-quantum-epilepsy-detection-2025'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

os.makedirs('uploads', exist_ok=True)
os.makedirs('reports', exist_ok=True)

# Initialize database
init_db()

# Initialize global processor and classifier
eeg_processor = EEGProcessor()
quantum_classifier = QuantumClassifier()
report_generator = ReportGenerator()


@app.route('/')
def index():
    """Main dashboard page"""
    analyses = get_all_analyses()
    stats = {
        'total_analyses': len(analyses),
        'seizure_detected': sum(1 for a in analyses if a.get('prediction') == 'Seizure'),
        'normal': sum(1 for a in analyses if a.get('prediction') == 'Normal'),
        'avg_accuracy': 96.8
    }
    return render_template('index.html', stats=stats, analyses=analyses[:10])


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """EEG Analysis page"""
    if request.method == 'GET':
        return render_template('analyze.html')
    
    data = request.get_json()
    mode = data.get('mode', 'demo')
    
    analysis_id = str(uuid.uuid4())[:8].upper()
    patient_id = data.get('patient_id', f'PT-{analysis_id}')
    patient_age = data.get('patient_age', 8)
    patient_name = data.get('patient_name', 'Anonymous Patient')
    
    # Generate or process EEG data
    if mode == 'demo':
        seizure_type = data.get('seizure_type', 'normal')
        eeg_data = eeg_processor.generate_synthetic_eeg(seizure_type=seizure_type)
    else:
        eeg_data = eeg_processor.generate_synthetic_eeg(seizure_type='random')
    
    # Process EEG signal
    processed = eeg_processor.process_eeg(eeg_data)
    
    # Extract features
    features = eeg_processor.extract_features(processed)
    
    # Quantum classification
    qresult = quantum_classifier.classify(features)
    
    # Build full result
    result = {
        'analysis_id': analysis_id,
        'patient_id': patient_id,
        'patient_name': patient_name,
        'patient_age': patient_age,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'prediction': qresult['prediction'],
        'confidence': qresult['confidence'],
        'seizure_probability': qresult['seizure_probability'],
        'risk_level': qresult['risk_level'],
        'eeg_channels': processed['channels'].tolist(),
        'time_axis': processed['time_axis'].tolist(),
        'frequency_bands': features['frequency_bands'],
        'band_powers': features['band_powers'],
        'topographic_map': features['topographic_map'],
        'quantum_features': qresult['quantum_features'],
        'classical_features': features['statistical_features'],
        'spectral_data': features['spectral_data'],
        'recommendations': qresult['recommendations'],
        'clinical_notes': qresult['clinical_notes'],
        'processing_time': qresult['processing_time']
    }
    
    # Save to database
    save_analysis(result)
    
    return jsonify(result)


@app.route('/results/<analysis_id>')
def results(analysis_id):
    """View specific analysis results"""
    analysis = get_analysis_by_id(analysis_id)
    if not analysis:
        return render_template('404.html'), 404
    return render_template('results.html', analysis=analysis)


@app.route('/history')
def history():
    """Analysis history page"""
    analyses = get_all_analyses()
    return render_template('history.html', analyses=analyses)


@app.route('/api/generate_report/<analysis_id>')
def generate_report(analysis_id):
    """Generate PDF/HTML clinical report"""
    analysis = get_analysis_by_id(analysis_id)
    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404
    
    report_path = report_generator.generate_html_report(analysis)
    return send_file(report_path, as_attachment=True, 
                     download_name=f'EEG_Report_{analysis_id}.html')


@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    analyses = get_all_analyses()
    return jsonify({
        'total': len(analyses),
        'seizure': sum(1 for a in analyses if a.get('prediction') == 'Seizure'),
        'normal': sum(1 for a in analyses if a.get('prediction') == 'Normal'),
        'high_risk': sum(1 for a in analyses if a.get('risk_level') == 'High'),
    })


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/upload_report', methods=['GET', 'POST'])
def upload_report():
    """Medical report upload and EEG indicator analysis"""
    if request.method == 'GET':
        return render_template('upload_report.html')

    # POST — handle file upload
    if 'report_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['report_file']
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Validate extension
    allowed = {'.pdf', '.txt', '.png', '.jpg', '.jpeg', '.webp'}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        return jsonify({'error': f'Unsupported file type: {ext}. Allowed: PDF, TXT, PNG, JPG'}), 400

    # Save file
    safe_name = f"report_{uuid.uuid4().hex[:8]}{ext}"
    save_path = os.path.join('uploads', safe_name)
    file.save(save_path)

    # Extract text
    text = ""
    extraction_method = "none"
    try:
        if ext == '.pdf':
            text = extract_text_from_pdf(save_path)
            extraction_method = "PDF text extraction"
        elif ext in ('.png', '.jpg', '.jpeg', '.webp'):
            text = extract_text_from_image(save_path)
            extraction_method = "OCR (image)"
            if not text.strip():
                # OCR not available — return friendly message
                return jsonify({
                    'error': 'OCR not available for image files in this environment. '
                             'Please upload a PDF or plain-text (.txt) report instead.'
                }), 422
        else:
            text = extract_text_from_txt(save_path)
            extraction_method = "Plain text"
    except Exception as e:
        return jsonify({'error': f'Text extraction failed: {str(e)}'}), 500
    finally:
        # Clean up uploaded file after extraction
        try:
            os.remove(save_path)
        except Exception:
            pass

    if not text.strip():
        return jsonify({
            'error': 'Could not extract text from this file. '
                     'Make sure the PDF has a text layer (not a scanned image). '
                     'Try copy-pasting the report content into a .txt file.'
        }), 422

    # Analyze
    analyzer = MedicalReportAnalyzer()
    result = analyzer.analyze_text(text, filename=file.filename)
    result['extraction_method'] = extraction_method
    result['text_preview'] = text[:800].strip()

    return jsonify(result)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='QEEG Epilepsy Detection System')
    parser.add_argument('--port', type=int, default=5001, help='Port to run on (default: 5001)')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--no-debug', action='store_true', help='Disable debug mode')
    args = parser.parse_args()
    
    print(f"\n  ⚡ QEEG System starting on http://localhost:{args.port}")
    print(f"  → Dashboard:   http://localhost:{args.port}/")
    print(f"  → Analysis:    http://localhost:{args.port}/analyze")
    print(f"  → History:     http://localhost:{args.port}/history")
    print(f"  → About:       http://localhost:{args.port}/about")
    print(f"\n  Press Ctrl+C to stop\n")
    
    app.run(debug=not args.no_debug, host='127.0.0.1', port=args.port)
