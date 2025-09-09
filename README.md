
#PhishGuard, phishing awareness aoo– Sprint 1 Demo

Run:
```bash

#This gets you the proper package installer to ensure the correct packages are installed
python get-pip.py

#Make sure you are in the correct file path where the program is stored to execute properly
cd <file path>

#Download the 4 libraries needed
pip install fastapi uvicorn "jinja2" "pydantic<2"

#Start my FastAPI app using Uvicorn, watch for file change and restart if recognized, and make it available on port 8000
uvicorn main:app --reload --port 8000
```

Then open http://127.0.0.1:8000/

Endpoints:
- GET /api/lessons (list lessons)
- POST /api/users (create demo user)
- POST /api/report (save report)
- GET /api/healthz (check DB seeded)

Sprint 1 complete
