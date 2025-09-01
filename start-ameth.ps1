cd "$env:USERPROFILE\OneDrive\Escritorio\ameth"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
