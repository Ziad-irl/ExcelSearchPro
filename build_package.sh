#!/bin/bash
# ExcelSearchPro Package Builder Script

echo "🏗️  Building ExcelSearchPro Package..."
echo "======================================"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# Build source distribution
echo "📦 Building source distribution..."
python setup.py sdist

# Build wheel distribution
echo "🎯 Building wheel distribution..."
python setup.py bdist_wheel

# Check the package
echo "🔍 Checking package integrity..."
python -m twine check dist/*

echo ""
echo "✅ Package build complete!"
echo "📁 Files created in dist/ directory:"
ls -la dist/

echo ""
echo "🚀 To upload to PyPI:"
echo "   python -m twine upload dist/*"
