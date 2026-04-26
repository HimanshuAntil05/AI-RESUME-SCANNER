# ⚡ AI-Powered Resume Scanner

An advanced resume analysis web app that goes far beyond basic parsing — combining DNA fingerprinting, lie detection, job market fit, time machine skill trends, and head-to-head battle mode.

> Built with Python (Flask) + Vanilla JS. No paid AI API required to run.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🧬 **Resume DNA** | Radar chart showing Leadership, Achievement, Analytical, Formality scores + personality type |
| 🔍 **Lie Detector** | Credibility score out of 100 — flags vague language, skill inflation, employment gaps |
| 🎯 **Job Market Fit** | Scores your resume against 8 real job roles, shows matched & missing skills |
| 💼 **Live Job Matches** | Pulls real job listings matching your top role (requires free API key) |
| ⏳ **Time Machine** | Line chart showing how your skills' market demand changed from 2018 → 2024 |
| ⚔️ **Battle Mode** | Upload 2 resumes — 5-round head-to-head comparison with a winner |

---

## 🧱 Tech Stack

- **Backend:** Python, Flask, spaCy, pdfplumber, textstat
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **File Support:** PDF, DOCX

---

## 📁 Project Structure

```
resume-scanner/
├── backend/
│   ├── app.py                  # Flask API (3 endpoints)
│   └── modules/
│       ├── resume_parser.py    # PDF/DOCX text extraction
│       ├── dna_fingerprint.py  # Writing style analysis
│       ├── lie_detector.py     # Credibility scoring
│       ├── skill_extractor.py  # Skill detection + job fit
│       ├── time_machine.py     # Historical skill demand
│       └── battle_mode.py      # Head-to-head comparison
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── requirements.txt
└── .env.example
```

---

## ⚙️ Installation & Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/resume-scanner.git
cd resume-scanner
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Set up environment variables
```bash
cp .env.example backend/.env
```
Open `backend/.env` and add your keys:
```
FLASK_SECRET_KEY=any_random_string
JSEARCH_API_KEY=your_rapidapi_key   # optional — for live jobs
```
> Get a free JSearch API key at [rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)

### 4. Start the backend
```bash
cd backend
python app.py
```
Backend runs at `http://127.0.0.1:5000`

### 5. Open the frontend
Open `frontend/index.html` in your browser.
Or use VS Code **Live Server** extension for best experience.

---

## 🖥️ How to Use

### Analyze Tab
1. Upload a PDF or DOCX resume
2. Click **Analyze Resume**
3. View DNA radar, credibility score, skills, job fit, and live jobs

### Battle Tab
1. Upload Resume A and Resume B
2. Click **Start Battle**
3. See who wins across 5 dimensions

### Time Machine Tab
1. Upload a resume
2. Click **Run Time Machine**
3. See how your skills' demand has changed since 2018

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/analyze` | Full resume analysis |
| POST | `/api/battle` | Compare two resumes |
| POST | `/api/time-machine` | Skill demand history |
| GET | `/health` | Server health check |

---

## 🔮 Roadmap (Future Features)

- [ ] OpenAI integration for smart improvement tips
- [ ] User authentication + scan history
- [ ] Resume improvement suggestions
- [ ] Deploy to cloud (Render / AWS)
- [ ] Support for more file types (TXT, LinkedIn PDF)

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---

## 📄 License

MIT License — free to use and modify.
