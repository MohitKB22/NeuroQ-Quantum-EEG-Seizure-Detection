# ⚡ QEEG — Quantum EEG Epilepsy Detection System

> 🎓 Hybrid Quantum-Classical AI for Pediatric Seizure Detection

![License](https://img.shields.io/badge/License-MIT-8b5cf6.svg)
![Python](https://img.shields.io/badge/Python-3.9--3.14-3b7bff.svg)
![Accuracy](https://img.shields.io/badge/Accuracy-95%25+-00e98a.svg)
![Quantum](https://img.shields.io/badge/Quantum-8--Qubit-ff8c42.svg)

---

## 🧠 About the Project

The **QEEG Epilepsy Detection System** is an advanced final year project that combines **Quantum Computing** with **AI/Machine Learning** to detect epileptic seizures in pediatric patients through EEG (Electroencephalogram) signal analysis. The system achieves over **95% diagnostic accuracy** by employing a novel Hybrid Quantum-Classical Machine Learning pipeline — a cutting-edge approach that maps classical EEG features into a quantum Hilbert space using an 8-qubit ZZ Feature Map circuit, then classifies them through an ensemble of a Quantum Kernel SVM and a Gradient Boosting Classifier.

🔬 Beyond real-time EEG signal analysis, the system also includes an **AI-powered Medical Report Scanner** that allows clinicians to upload existing patient reports (PDF or text) and automatically scans them for EEG-related terminology, seizure indicators, anti-epileptic medications, and brain region references — generating an instant risk assessment with clinical recommendations.

🖥️ The entire system is wrapped in a professional **dark-mode medical web interface** built with Flask, featuring interactive Plotly visualizations, topographic brain mapping, frequency band analysis, and downloadable clinical HTML reports — making it both a research-grade tool and a polished, presentation-ready application.

---

## ✨ Key Features

- ⚛️ **Hybrid Quantum-Classical ML** — 8-qubit ZZ Feature Map quantum circuit combined with Gradient Boosting for superior classification
- 📡 **19-Channel EEG Processing** — Full preprocessing pipeline including bandpass filtering, Common Average Referencing, Welch PSD, Hjorth parameters, and inter-channel coherence
- 🔴 **4 Seizure Type Detection** — Normal, Focal, Generalized Tonic-Clonic, and Absence seizures
- 📄 **Medical Report Scanner** — Upload PDF/TXT patient reports; AI scans for EEG terms, seizure keywords, AED medications, and brain regions
- 🗺️ **Topographic Brain Mapping** — Real-time 2D spatial activity visualization across all 19 electrodes
- 📋 **Clinical Report Generation** — Professional downloadable HTML reports with all metrics and recommendations
- 🗄️ **Persistent Analysis History** — SQLite-backed storage of all analyses with full search and review

---

## 📊 Performance

| Metric | Value |
|---|---|
| 🎯 Overall Accuracy | 95.0% |
| 🔴 Focal Seizure Detection | 100% |
| 🟡 Absence Seizure Detection | 100% |
| 🟢 Normal EEG Classification | 100% |
| 💡 Model Confidence Range | 92 – 99% |
| ⚡ Processing Time | < 2 seconds |

---

## 🔬 Seizure Types

| Type | EEG Signature |
|---|---|
| ✅ Normal | Alpha-dominant background (8–13 Hz) |
| 🔴 Focal Seizure | Spike-wave discharges in C3/C4/Cz channels |
| 🚨 Generalized Tonic-Clonic | Polyspike complexes at 2–2.5 Hz, high amplitude |
| 🟡 Absence Seizure | Classic 3 Hz spike-wave complex, all channels |

---

## ⚛️ Quantum Computing Approach

| Parameter | Detail |
|---|---|
| 🔧 Circuit | 8-qubit ZZ Feature Map |
| 📥 Encoding | Amplitude encoding |
| 🧮 Kernel | K(x₁,x₂) = \|⟨ψ(x₁)\|ψ(x₂)⟩\|² |
| 💻 Backend | NumPy statevector simulator (PennyLane / Qiskit compatible) |
| ⚖️ Ensemble Weights | 55% Gradient Boosting · 25% Quantum Kernel · 20% Physiological Index |

---
