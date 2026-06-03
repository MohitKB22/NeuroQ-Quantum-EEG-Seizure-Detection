"""
Medical Report Analyzer
Parses uploaded PDF/image medical reports and extracts EEG-relevant indicators.
Uses keyword analysis + heuristic scoring to flag potential epilepsy indicators.
"""

import re
import os
import json
from datetime import datetime


# ─── EEG / Epilepsy indicator keywords ────────────────────────────────────────

SEIZURE_KEYWORDS = [
    "seizure", "epilepsy", "epileptic", "convulsion", "ictal", "interictal",
    "postictal", "tonic", "clonic", "tonic-clonic", "absence", "myoclonic",
    "atonic", "focal", "generalized", "status epilepticus", "aura",
    "spike", "spike-wave", "polyspike", "sharp wave", "epileptiform",
    "paroxysmal", "discharge", "abnormal eeg", "eeg abnormality",
    "cortical dysplasia", "tuberous sclerosis", "lennox-gastaut",
    "west syndrome", "rolandic", "benign epilepsy",
]

EEG_KEYWORDS = [
    "eeg", "electroencephalogram", "electroencephalography",
    "brain wave", "brainwave", "delta wave", "theta wave", "alpha wave",
    "beta wave", "gamma wave", "slow wave", "fast wave",
    "background activity", "cortical activity", "neurological",
    "brain activity", "neural", "encephalopathy",
]

NORMAL_KEYWORDS = [
    "normal eeg", "no seizure", "no epilepsy", "no epileptiform",
    "within normal limits", "normal background", "unremarkable",
    "no abnormality", "no significant", "normal study",
    "benign variant", "age-appropriate",
]

MEDICATION_KEYWORDS = [
    "valproate", "valproic acid", "carbamazepine", "phenytoin", "lamotrigine",
    "levetiracetam", "keppra", "topiramate", "oxcarbazepine", "clonazepam",
    "phenobarbital", "ethosuximide", "gabapentin", "pregabalin",
    "anti-epileptic", "antiepileptic", "aed", "anticonvulsant",
]

BRAIN_REGION_KEYWORDS = [
    "temporal", "frontal", "occipital", "parietal", "central",
    "left hemisphere", "right hemisphere", "bilateral", "focal",
    "diffuse", "cortex", "hippocampus", "amygdala", "thalamus",
]


class MedicalReportAnalyzer:
    """Analyzes uploaded medical reports for EEG/epilepsy indicators."""

    def analyze_text(self, text: str, filename: str = "") -> dict:
        """
        Full analysis pipeline on extracted text.
        Returns structured findings dict.
        """
        text_lower = text.lower()
        words = text_lower.split()
        total_words = max(len(words), 1)

        # ── Keyword hits ──
        seizure_hits   = self._find_hits(text_lower, SEIZURE_KEYWORDS)
        eeg_hits       = self._find_hits(text_lower, EEG_KEYWORDS)
        normal_hits    = self._find_hits(text_lower, NORMAL_KEYWORDS)
        medication_hits= self._find_hits(text_lower, MEDICATION_KEYWORDS)
        region_hits    = self._find_hits(text_lower, BRAIN_REGION_KEYWORDS)

        # ── Extract patient info ──
        patient_info = self._extract_patient_info(text)

        # ── Risk scoring ──
        seizure_score  = min(len(seizure_hits) * 15, 60)
        eeg_score      = min(len(eeg_hits) * 8, 25)
        normal_penalty = len(normal_hits) * 20
        med_score      = min(len(medication_hits) * 10, 20)

        raw_score = seizure_score + eeg_score + med_score - normal_penalty
        eeg_probability = max(5, min(95, raw_score + 10))

        # ── Determine result ──
        has_eeg_mention = len(eeg_hits) > 0
        has_seizure_mention = len(seizure_hits) > 0
        is_explicitly_normal = any(
            phrase in text_lower for phrase in [
                "normal eeg", "no seizure activity", "no epileptiform",
                "within normal limits", "unremarkable eeg"
            ]
        )

        if is_explicitly_normal:
            verdict = "Normal"
            risk_level = "Minimal"
            eeg_probability = max(5, eeg_probability - 40)
        elif has_seizure_mention and len(seizure_hits) >= 3:
            verdict = "EEG Abnormality Indicated"
            risk_level = "High" if len(seizure_hits) >= 5 else "Medium"
        elif has_eeg_mention and has_seizure_mention:
            verdict = "Possible EEG Abnormality"
            risk_level = "Medium"
        elif has_eeg_mention or has_seizure_mention:
            verdict = "EEG Evaluation Recommended"
            risk_level = "Low"
        else:
            verdict = "No EEG Indicators Found"
            risk_level = "Minimal"
            eeg_probability = max(5, eeg_probability - 20)

        # ── Key sentences ──
        key_sentences = self._extract_key_sentences(text, seizure_hits + eeg_hits)

        # ── Summary ──
        summary = self._generate_summary(
            verdict, seizure_hits, eeg_hits, normal_hits,
            medication_hits, region_hits, patient_info
        )

        return {
            "filename": filename,
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "word_count": total_words,
            "verdict": verdict,
            "risk_level": risk_level,
            "eeg_probability": round(eeg_probability, 1),
            "has_eeg_content": has_eeg_mention,
            "is_explicitly_normal": is_explicitly_normal,
            "patient_info": patient_info,
            "keyword_hits": {
                "seizure_terms": seizure_hits[:10],
                "eeg_terms": eeg_hits[:8],
                "normal_terms": normal_hits[:5],
                "medications": medication_hits[:8],
                "brain_regions": region_hits[:6],
            },
            "hit_counts": {
                "seizure": len(seizure_hits),
                "eeg": len(eeg_hits),
                "normal": len(normal_hits),
                "medications": len(medication_hits),
                "regions": len(region_hits),
            },
            "key_sentences": key_sentences[:5],
            "summary": summary,
            "recommendations": self._generate_recommendations(verdict, risk_level, medication_hits),
        }

    def _find_hits(self, text_lower: str, keywords: list) -> list:
        hits = []
        for kw in keywords:
            if kw in text_lower:
                hits.append(kw)
        return hits

    def _extract_patient_info(self, text: str) -> dict:
        info = {}
        # Age
        age_match = re.search(
            r'\b(?:age[d]?\s*:?\s*|(\d+)\s*(?:year|yr)s?\s*old)\b(\d+)?',
            text, re.IGNORECASE
        )
        if age_match:
            age_str = age_match.group(1) or age_match.group(2)
            if age_str and age_str.isdigit():
                info["age"] = int(age_str)

        # Name (simple heuristic)
        name_match = re.search(
            r'(?:patient\s*(?:name)?\s*:?\s*)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            text
        )
        if name_match:
            info["name"] = name_match.group(1)

        # Date
        date_match = re.search(
            r'\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\d{4}-\d{2}-\d{2})\b', text
        )
        if date_match:
            info["report_date"] = date_match.group(1)

        return info

    def _extract_key_sentences(self, text: str, hit_keywords: list) -> list:
        sentences = re.split(r'[.!?]\s+', text)
        scored = []
        for sent in sentences:
            sent = sent.strip()
            if len(sent) < 20 or len(sent) > 400:
                continue
            score = sum(1 for kw in hit_keywords if kw in sent.lower())
            if score > 0:
                scored.append((score, sent))
        scored.sort(reverse=True)
        return [s[1] for s in scored[:5]]

    def _generate_summary(self, verdict, seizure_hits, eeg_hits,
                           normal_hits, medication_hits, region_hits, patient_info):
        parts = []

        if patient_info.get("name"):
            parts.append(f"Patient: {patient_info['name']}.")
        if patient_info.get("age"):
            parts.append(f"Age: {patient_info['age']} years.")

        if eeg_hits:
            parts.append(f"EEG-related terms found: {', '.join(eeg_hits[:4])}.")
        if seizure_hits:
            parts.append(f"Seizure/epilepsy terms detected: {', '.join(seizure_hits[:5])}.")
        if normal_hits:
            parts.append(f"Normal indicators: {', '.join(normal_hits[:3])}.")
        if medication_hits:
            parts.append(f"Anti-epileptic medications mentioned: {', '.join(medication_hits[:4])}.")
        if region_hits:
            parts.append(f"Brain regions referenced: {', '.join(region_hits[:4])}.")

        if not parts:
            parts.append("No significant EEG or neurological terms detected in this report.")

        parts.append(f"AI Assessment: {verdict}.")
        return " ".join(parts)

    def _generate_recommendations(self, verdict, risk_level, medication_hits):
        recs = []
        if risk_level in ("High", "Medium"):
            recs.append({"icon": "🧠", "priority": "URGENT",
                         "text": "Neurologist consultation strongly recommended"})
            recs.append({"icon": "📋", "priority": "HIGH",
                         "text": "Full EEG recording with video telemetry advised"})
        if medication_hits:
            recs.append({"icon": "💊", "priority": "HIGH",
                         "text": f"AED therapy noted — medication review recommended"})
        if risk_level == "Low":
            recs.append({"icon": "📅", "priority": "MEDIUM",
                         "text": "Routine EEG follow-up in 3–6 months"})
        recs.append({"icon": "⚕️", "priority": "INFO",
                     "text": "This AI analysis supplements but does not replace clinical judgment"})
        return recs


# ── Text extraction helpers (called from Flask routes) ────────────────────────

def extract_text_from_pdf(filepath: str) -> str:
    """Extract text from PDF using pdfplumber (best) or PyPDF2 fallback."""
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except Exception:
        pass

    try:
        import PyPDF2
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
    except Exception:
        pass

    return text


def extract_text_from_image(filepath: str) -> str:
    """Extract text from image using pytesseract OCR (if available)."""
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(filepath)
        return pytesseract.image_to_string(img)
    except ImportError:
        return ""
    except Exception:
        return ""


def extract_text_from_txt(filepath: str) -> str:
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            with open(filepath, encoding=enc) as f:
                return f.read()
        except Exception:
            continue
    return ""
