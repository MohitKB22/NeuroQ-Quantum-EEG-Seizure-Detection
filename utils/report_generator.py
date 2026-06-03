"""
Clinical Report Generator
Generates HTML/PDF clinical reports for EEG analyses
"""

import os
from datetime import datetime


class ReportGenerator:
    """Generates professional clinical EEG reports"""
    
    def generate_html_report(self, analysis):
        """Generate a comprehensive HTML clinical report"""
        
        analysis_id = analysis.get('analysis_id', 'N/A')
        patient_id = analysis.get('patient_id', 'N/A')
        patient_name = analysis.get('patient_name', 'Anonymous')
        patient_age = analysis.get('patient_age', 'N/A')
        timestamp = analysis.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        prediction = analysis.get('prediction', 'N/A')
        confidence = analysis.get('confidence', 0)
        seizure_prob = analysis.get('seizure_probability', 0)
        risk_level = analysis.get('risk_level', 'N/A')
        
        band_powers = analysis.get('band_powers', {})
        recommendations = analysis.get('recommendations', [])
        clinical_notes = analysis.get('clinical_notes', [])
        quantum_features = analysis.get('quantum_features', {})
        
        status_color = '#e74c3c' if prediction == 'Seizure' else '#27ae60'
        risk_colors = {'High': '#e74c3c', 'Medium': '#f39c12', 'Low': '#3498db', 'Minimal': '#27ae60'}
        risk_color = risk_colors.get(risk_level, '#95a5a6')
        
        rec_html = ''
        for rec in recommendations:
            p_colors = {'URGENT': '#e74c3c', 'HIGH': '#e67e22', 'MEDIUM': '#3498db', 'INFO': '#27ae60'}
            p_color = p_colors.get(rec.get('priority', 'INFO'), '#95a5a6')
            rec_html += f'''
            <div style="display:flex;align-items:center;gap:12px;padding:10px;border-left:4px solid {p_color};background:#f8f9fa;margin-bottom:8px;border-radius:4px;">
                <span style="font-size:1.5em;">{rec.get("icon","")}</span>
                <div>
                    <span style="color:{p_color};font-weight:bold;font-size:0.75em;">{rec.get("priority","")}</span>
                    <p style="margin:2px 0;color:#2c3e50;">{rec.get("action","")}</p>
                </div>
            </div>'''
        
        notes_html = ''.join(f'<li style="margin-bottom:6px;color:#555;">{note}</li>' for note in clinical_notes)
        
        band_rows = ''
        for band, power in band_powers.items():
            bar_width = min(int(float(power) * 400), 300)
            band_rows += f'''
            <tr>
                <td style="padding:8px;font-weight:bold;color:#2c3e50;">{band}</td>
                <td style="padding:8px;">{float(power):.4f}</td>
                <td style="padding:8px;">
                    <div style="background:#3498db;height:18px;width:{bar_width}px;border-radius:3px;min-width:4px;"></div>
                </td>
            </tr>'''
        
        q_rows = ''
        for k, v in quantum_features.items():
            q_rows += f'<tr><td style="padding:6px;color:#8e44ad;font-weight:bold;">{k}</td><td style="padding:6px;">{v}</td></tr>'
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>EEG Clinical Report - {analysis_id}</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; background: #f5f5f5; color: #2c3e50; }}
  .page {{ max-width: 900px; margin: 20px auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
  .header {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 30px 40px; }}
  .header h1 {{ margin: 0; font-size: 1.8em; letter-spacing: 2px; }}
  .header .subtitle {{ opacity: 0.7; margin-top: 5px; font-size: 0.9em; }}
  .section {{ padding: 25px 40px; border-bottom: 1px solid #eee; }}
  .section h2 {{ color: #1a1a2e; font-size: 1.1em; text-transform: uppercase; letter-spacing: 1px; border-left: 4px solid #3498db; padding-left: 10px; }}
  .status-badge {{ display: inline-block; padding: 8px 20px; border-radius: 20px; color: white; font-weight: bold; font-size: 1.2em; background: {status_color}; }}
  .risk-badge {{ display: inline-block; padding: 6px 16px; border-radius: 20px; color: white; font-weight: bold; background: {risk_color}; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
  .metric-card {{ background: #f8f9fa; border-radius: 8px; padding: 15px; text-align: center; }}
  .metric-card .value {{ font-size: 2em; font-weight: bold; color: #2c3e50; }}
  .metric-card .label {{ color: #7f8c8d; font-size: 0.85em; margin-top: 4px; }}
  table {{ width: 100%; border-collapse: collapse; }}
  .footer {{ background: #1a1a2e; color: rgba(255,255,255,0.6); padding: 20px 40px; font-size: 0.8em; text-align: center; }}
  @media print {{ body {{ background: white; }} .page {{ box-shadow: none; }} }}
</style>
</head>
<body>
<div class="page">
  <div class="header">
    <h1>⚡ EEG Epilepsy Analysis Report</h1>
    <div class="subtitle">Hybrid Quantum-Classical AI System | QEEG-Hybrid-v2.1</div>
    <div style="margin-top:15px;opacity:0.8;font-size:0.85em;">Report ID: {analysis_id} &nbsp;|&nbsp; Generated: {timestamp}</div>
  </div>
  
  <div class="section">
    <h2>Patient Information</h2>
    <div class="grid">
      <div><strong>Patient Name:</strong> {patient_name}</div>
      <div><strong>Patient ID:</strong> {patient_id}</div>
      <div><strong>Age:</strong> {patient_age} years</div>
      <div><strong>Analysis Date:</strong> {timestamp}</div>
    </div>
  </div>
  
  <div class="section">
    <h2>Diagnosis Result</h2>
    <div style="display:flex;align-items:center;gap:30px;flex-wrap:wrap;">
      <div>
        <div style="font-size:0.8em;color:#7f8c8d;margin-bottom:5px;">CLASSIFICATION</div>
        <span class="status-badge">{prediction.upper()}</span>
      </div>
      <div>
        <div style="font-size:0.8em;color:#7f8c8d;margin-bottom:5px;">RISK LEVEL</div>
        <span class="risk-badge">{risk_level}</span>
      </div>
      <div class="metric-card" style="min-width:120px;">
        <div class="value" style="color:{status_color};">{seizure_prob}%</div>
        <div class="label">Seizure Probability</div>
      </div>
      <div class="metric-card" style="min-width:120px;">
        <div class="value">{confidence}%</div>
        <div class="label">Model Confidence</div>
      </div>
    </div>
  </div>
  
  <div class="section">
    <h2>EEG Frequency Band Analysis</h2>
    <table>
      <thead><tr style="background:#f0f0f0;">
        <th style="padding:8px;text-align:left;">Band</th>
        <th style="padding:8px;text-align:left;">Power (μV²/Hz)</th>
        <th style="padding:8px;text-align:left;">Relative Activity</th>
      </tr></thead>
      <tbody>{band_rows}</tbody>
    </table>
  </div>
  
  <div class="section">
    <h2>Clinical Notes</h2>
    <ul style="padding-left:20px;margin:0;">{notes_html}</ul>
  </div>
  
  <div class="section">
    <h2>Clinical Recommendations</h2>
    {rec_html}
  </div>
  
  <div class="section">
    <h2>Quantum Computing Metrics</h2>
    <p style="color:#8e44ad;font-size:0.9em;">Analysis performed using 8-qubit ZZ Feature Map quantum circuit</p>
    <table>
      <thead><tr style="background:#f0f0f0;">
        <th style="padding:8px;text-align:left;">Quantum Parameter</th>
        <th style="padding:8px;text-align:left;">Value</th>
      </tr></thead>
      <tbody>{q_rows}</tbody>
    </table>
  </div>
  
  <div class="footer">
    <p>⚠️ DISCLAIMER: This report is generated by an AI-assisted system for research and educational purposes only. 
    It does not constitute medical advice and must be reviewed by a licensed neurologist before any clinical decisions.</p>
    <p>EEG Epilepsy Detection System © 2025 | Hybrid Quantum-Classical AI | Final Year Project</p>
  </div>
</div>
</body>
</html>'''
        
        report_path = os.path.join('reports', f'EEG_Report_{analysis_id}.html')
        with open(report_path, 'w') as f:
            f.write(html)
        
        return report_path
