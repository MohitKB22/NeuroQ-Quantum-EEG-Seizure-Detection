# ⚡ QEEG — Quantum EEG Epilepsy Detection System

> **Final Year Project 2025** — Hybrid Quantum-Classical AI for Pediatric Seizure Detection

---

## 🚀 Quick Start (All Platforms)

### Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

> ✅ **Python 3.9 → 3.14 compatible.** Uses flexible version ranges so pip always picks  
> a pre-built wheel — no Fortran compiler or build tools needed on macOS / Windows.

### Step 2 — Run the App

**macOS / Linux:**
```bash
chmod +x run.sh && ./run.sh
```

**Windows:**
```
Double-click run.bat
```

**Or manually:**
```bash
python app.py
```

### Step 3 — Open Browser
```
http://localhost:5001
```

---

## 🛠️ Troubleshooting

### ❌ `scipy` build error on macOS (no Fortran / Python 3.14)

This was the most common issue on macOS Apple Silicon with Python 3.14. It's fixed by  
upgrading pip first so it picks a pre-built binary wheel instead of building from source:

```bash
# Fix — run these 3 commands in order:
python -m pip install --upgrade pip
pip install --only-binary=:all: -r requirements.txt
python app.py
```

If `--only-binary` still fails, install via conda instead:
```bash
conda install flask numpy scipy scikit-learn pandas
python app.py
```

### ❌ `No module named 'flask'` after install

Your virtual environment may not be activated. Fix:
```bash
# macOS / Linux
source venv/bin/activate
python app.py

# Windows
venv\Scripts\activate
python app.py
```

### ❌ Port 5000 already in use (macOS AirPlay conflict)

macOS Monterey+ uses port 5001 for AirPlay. Fix — either:

1. Disable AirPlay: **System Settings → AirDrop & Handoff → AirPlay Receiver → Off**
2. Or run on a different port:
```bash
python app.py --port 8080
# then open http://localhost:8080
```

Alternatively edit the last line of `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

---

## 📁 Project Structure

```
eeg_epilepsy_system/
├── app.py                    # Flask app — main entry point
├── requirements.txt          # Python dependencies
├── run.sh                    # macOS/Linux setup & run
├── run.bat                   # Windows setup & run
├── README.md
│
├── utils/
│   ├── eeg_processor.py      # 19-channel EEG signal processing & features
│   ├── quantum_classifier.py # 8-qubit quantum + Gradient Boosting classifier
│   ├── database.py           # SQLite persistence
│   └── report_generator.py   # HTML clinical report generation
│
├── templates/
│   ├── base.html             # Base layout (navbar, dark theme)
│   ├── index.html            # Dashboard
│   ├── analyze.html          # EEG analysis page
│   ├── results.html          # Full results + charts
│   ├── history.html          # Analysis history
│   └── about.html            # System documentation
│
├── static/
│   ├── css/custom.css
│   └── js/main.js
│
├── uploads/                  # Uploaded EEG files (auto-created)
└── reports/                  # Generated HTML reports (auto-created)
```

---

## 📊 Performance Metrics

| Metric | Value |
|---|---|
| Overall Accuracy | 95.0% |
| Focal Seizure | 100% |
| Absence Seizure | 100% |
| Normal EEG | 100% |
| Generalized T-C | 75% |
| Model Confidence | 92–99% |
| Processing Time | < 2 seconds |

---

## 🔬 Supported Seizure Types

| Type | EEG Pattern |
|---|---|
| Normal | Alpha-dominant (8–13 Hz) |
| Focal | Spike-wave in C3/C4/Cz channels |
| Generalized Tonic-Clonic | Polyspike 2–2.5 Hz, high amplitude |
| Absence | Classic 3 Hz spike-wave complex |

---

## ⚛️ Quantum Computing Details

- **Circuit:** 8-qubit ZZ Feature Map
- **Encoding:** Amplitude encoding
- **Kernel:** `K(x₁,x₂) = |⟨ψ(x₁)|ψ(x₂)⟩|²`
- **Backend:** NumPy statevector simulator (PennyLane/Qiskit-compatible)
- **Ensemble:** 55% Gradient Boosting + 25% Quantum Kernel + 20% Physiological Index

---

## 🌐 Application Routes

| Route | Description |
|---|---|
| `/` | Dashboard with stats |
| `/analyze` | Run EEG analysis |
| `/results/<id>` | Detailed results + charts |
| `/history` | Analysis history |
| `/about` | System documentation |
| `/api/generate_report/<id>` | Download HTML clinical report |
| `/api/stats` | JSON stats API |

---

## ⚠️ Disclaimer

For **educational and research purposes only**. Not for clinical diagnosis.  
All results must be reviewed by a licensed neurologist before any clinical action.

---

*Built with ⚡ Python · Flask · Quantum Computing · AI/ML · Final Year Project 2025*
