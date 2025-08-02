from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="excelsearchpro",
    version="1.0.0",
    author="ExcelSearchPro Team",
    author_email="contact@excelsearchpro.com",
    description="Fast Excel Database Search Tool with GUI and CLI interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ExcelSearchPro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
        "Topic :: Database",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "excelsearchpro=main:main",
            "excel-search-gui=excel_search_gui:main",
            "excel-search-cli=excel_search_cli:main",
        ],
    },
    keywords="excel search database csv gui cli pandas data-analysis spreadsheet office",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ExcelSearchPro/issues",
        "Source": "https://github.com/yourusername/ExcelSearchPro",
        "Documentation": "https://github.com/yourusername/ExcelSearchPro#readme",
    },
)
