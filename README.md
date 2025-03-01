# OCR Data Extraction From Receipt or Invoice

## Project Overview

This project demonstrates an end-to-end machine learning application for OCR data extraction from receipt or invoice. It uses Streamlit for an interactive frontend interface.

## Project Structure
```plaintext
ocr_app/
├── app/
│   ├── __init__.py
│   ├── ocr.py          # DonutOCR class (OCR processing)
│   └── api.py          # FastAPI API to receive files and return OCR results
├── utils/
│   ├── __init__.py
│   └── logger.py       # Logger configuration (as per the provided code)
├── streamlit_app.py    # Streamlit application for file upload UI
├── requirements.txt    # List of dependencies
└── Dockerfile          # Docker file for containerization
```

## Installation and Setup

### Prerequisites
- Python 3.9 or higher
- Docker and Docker Compose
- Git

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ocr_app.git
cd ocr_app
```

2. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows
.\venv\Scripts\activate
# For Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the applications:
```bash
streamlit run streamlit_app.py
```

### Docker Setup

#### Building Individual Images

1. FastAPI Image:
```bash
# Build Image Docker
docker build -t ocr_app .

```

2. Run Container:
```bash
# for FastAPI
docker run -d -p 8000:8000 ocr_app
```

```bash
# for Streamlit
docker run -d -p 8501:8501 ocr_app streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## Development Team
- - **Rein L Tobing** - Machine Learning Engineer
  - Email: reinltobing@gmail.com
  - LinkedIn: [Rein L Tobing](https://www.linkedin.com/in/rein-l-tobing/)
  - GitHub: [rein55](https://github.com/rein55)

## Acknowledgments
- NAVER Clova AI Research
- Hugging Face
- CORD Dataset Contributors
- Streamlit and FastAPI communities

---
📫 For support, email reinltobing@gmail.com or create an issue in the repository.

Built with ❤️ using Python, FastAPI, and Streamlit