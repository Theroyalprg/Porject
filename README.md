# Railway Infrastructure Intelligence — Minor Project-I

## Current starter features
- Streamlit dashboard
- Image upload and SQLite inspection record creation
- Manual review status tracking
- PDF text extraction with page-aware chunks and basic heading context
- Keyword search baseline over extracted manual passages

## Setup on macOS
```bash
cd railway_intelligence_starter
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If your default Python is incompatible, use Python 3.11 or 3.12 for the virtual environment.

## Important limitations
No railway-specific trained model is included. The app does not infer that an image is safe or defective. PDF heading detection is heuristic and must be validated against the source manual. This is not a safety-critical tool.

## Next steps
1. Verify dataset source, licence, annotations, and class balance.
2. Improve IRPWM parsing and validate chunks against source pages.
3. Add Sentence Transformers + FAISS for semantic retrieval.
4. Integrate a validated YOLO model and evaluate precision, recall, and mAP.
5. Add source-grounded explanations and traceability reports.

## Candidate official sources
- IRPWM: https://indianrailways.gov.in/railwayboard/uploads/directorate/prd/PR/IRPWM2020.pdf
- USFD Manual amendment: https://rdso.indianrailways.gov.in/uploads/2025-03-17-ACS%202%20of%20USFD%20Manual.pdf
