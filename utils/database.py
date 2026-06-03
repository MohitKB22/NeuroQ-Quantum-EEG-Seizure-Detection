"""
Database Module - SQLite storage for EEG analyses
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = 'eeg_analyses.db'


def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id TEXT UNIQUE NOT NULL,
            patient_id TEXT,
            patient_name TEXT,
            patient_age INTEGER,
            timestamp TEXT,
            prediction TEXT,
            confidence REAL,
            seizure_probability REAL,
            risk_level TEXT,
            data_json TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def save_analysis(result):
    """Save analysis result to database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT OR REPLACE INTO analyses 
            (analysis_id, patient_id, patient_name, patient_age, timestamp, 
             prediction, confidence, seizure_probability, risk_level, data_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result['analysis_id'],
            result.get('patient_id', ''),
            result.get('patient_name', ''),
            result.get('patient_age', 0),
            result.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            result.get('prediction', ''),
            result.get('confidence', 0),
            result.get('seizure_probability', 0),
            result.get('risk_level', ''),
            json.dumps(result)
        ))
        conn.commit()
    except Exception as e:
        print(f"DB save error: {e}")
    finally:
        conn.close()


def get_all_analyses():
    """Get all analyses from database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('''
        SELECT analysis_id, patient_id, patient_name, patient_age, 
               timestamp, prediction, confidence, seizure_probability, risk_level
        FROM analyses ORDER BY created_at DESC
    ''')
    
    rows = c.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_analysis_by_id(analysis_id):
    """Get specific analysis by ID"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT data_json FROM analyses WHERE analysis_id = ?', (analysis_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return json.loads(row[0])
    return None
