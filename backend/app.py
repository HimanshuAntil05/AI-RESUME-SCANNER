import os
import uuid
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from modules.resume_parser import extract_text, extract_sections, extract_contact
from modules.dna_fingerprint import generate_dna
from modules.lie_detector import score_credibility
from modules.skill_extractor import extract_skills, compute_job_fit, fetch_live_jobs
from modules.time_machine import get_time_machine
from modules.battle_mode import battle

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")

ALLOWED_EXT = {".pdf", ".docx"}


def _save_upload(file) -> str:
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        raise ValueError("Only PDF and DOCX files are supported.")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    file.save(tmp.name)
    return tmp.name


def _analyze(file_path: str) -> dict:
    text = extract_text(file_path)
    sections = extract_sections(text)
    contact = extract_contact(text)
    skills_data = extract_skills(text)
    dna = generate_dna(text)
    credibility = score_credibility(text, sections)
    job_fit = compute_job_fit(skills_data["skills"])
    time_machine = get_time_machine(list(skills_data["skills"].keys()))
    top_role = job_fit[0]["role"] if job_fit else "Software Engineer"
    live_jobs = fetch_live_jobs(top_role, list(skills_data["skills"].keys())[:5])

    return {
        "contact": contact,
        "skills": skills_data,
        "dna": dna,
        "credibility": credibility,
        "job_fit": job_fit,
        "time_machine": time_machine,
        "live_jobs": live_jobs,
    }


@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        path = _save_upload(request.files["resume"])
        result = _analyze(path)
        os.unlink(path)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


@app.route("/api/battle", methods=["POST"])
def battle_route():
    if "resume_a" not in request.files or "resume_b" not in request.files:
        return jsonify({"error": "Upload both resume_a and resume_b"}), 400
    path_a = path_b = None
    try:
        path_a = _save_upload(request.files["resume_a"])
        path_b = _save_upload(request.files["resume_b"])

        text_a = extract_text(path_a)
        text_b = extract_text(path_b)
        sections_a = extract_sections(text_a)
        sections_b = extract_sections(text_b)

        result = battle(text_a, sections_a, text_b, sections_b)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Battle failed: {str(e)}"}), 500
    finally:
        for p in [path_a, path_b]:
            if p and os.path.exists(p):
                os.unlink(p)


@app.route("/api/time-machine", methods=["POST"])
def time_machine_route():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        path = _save_upload(request.files["resume"])
        text = extract_text(path)
        os.unlink(path)
        skills_data = extract_skills(text)
        result = get_time_machine(list(skills_data["skills"].keys()))
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
