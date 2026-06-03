#!/bin/bash
# ============================================================
# QEEG Epilepsy Detection System - Setup & Run Script
# Supports: macOS (Intel + Apple Silicon), Linux, Windows WSL
# Python: 3.9 – 3.14
# ============================================================

echo ""
echo "  ⚡ QEEG — Quantum EEG Epilepsy Detection System"
echo "  ================================================="
echo ""

# Find python3
PYTHON=""
for cmd in python3.14 python3.13 python3.12 python3.11 python3.10 python3.9 python3 python; do
    if command -v "$cmd" &>/dev/null; then
        VER=$("$cmd" -c "import sys; print(sys.version_info[:2])" 2>/dev/null)
        MAJOR=$("$cmd" -c "import sys; print(sys.version_info[0])")
        MINOR=$("$cmd" -c "import sys; print(sys.version_info[1])")
        if [ "$MAJOR" -eq "3" ] && [ "$MINOR" -ge "9" ]; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "  ❌ Python 3.9+ not found. Please install from https://python.org"
    exit 1
fi

echo "  ✓ Using: $PYTHON ($($PYTHON --version))"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "  → Creating virtual environment..."
    $PYTHON -m venv venv
    if [ $? -ne 0 ]; then
        echo "  ❌ Failed to create venv. Try: $PYTHON -m pip install virtualenv"
        exit 1
    fi
fi

# Activate venv
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    source venv/Scripts/activate 2>/dev/null || true
fi
echo "  ✓ Virtual environment activated"

# Upgrade pip silently
echo "  → Upgrading pip..."
python -m pip install --upgrade pip -q

# Install dependencies
echo "  → Installing dependencies (this may take 1-2 minutes on first run)..."
pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo ""
    echo "  ❌ Dependency install failed. Trying with --only-binary=:all: ..."
    pip install --only-binary=:all: -r requirements.txt
fi

echo "  ✓ All dependencies installed"

# Create required directories
mkdir -p uploads reports
echo "  ✓ Directories ready"

echo ""
echo "  ✅ Setup complete! Starting server..."
echo ""
echo "  🌐 Dashboard:    http://localhost:5000"
echo "  🔬 Analyze EEG:  http://localhost:5000/analyze"
echo "  📋 History:      http://localhost:5000/history"
echo "  ℹ️  About:        http://localhost:5000/about"
echo ""
echo "  Press Ctrl+C to stop"
echo "  ================================================="
echo ""

python app.py
