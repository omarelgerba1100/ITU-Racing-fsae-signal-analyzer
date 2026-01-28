#!/bin/bash

echo "============================================"
echo " Advanced Engineering Analysis Tool"
echo " ITU Racing Team - Installation Script"
echo "============================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed."
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  macOS:  brew install python3"
    echo "  Ubuntu: sudo apt install python3 python3-pip python3-venv"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

echo "[OK] Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "[WARNING] Could not create virtual environment."
    echo "Installing packages globally..."
    pip3 install -r requirements.txt
    exit $?
fi

echo "[OK] Virtual environment created."
echo ""

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing required packages..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install some packages."
    echo "Please check your internet connection and try again."
    exit 1
fi

echo ""
echo "============================================"
echo " Installation Complete!"
echo "============================================"
echo ""
echo "To run the application:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Or simply run:"
echo "  ./run_app.sh"
echo ""

# Create run script
cat > run_app.sh << 'EOF'
#!/bin/bash
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 main.py
EOF

chmod +x run_app.sh
echo "[OK] Created run_app.sh script"
