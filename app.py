# app.py — Neuro Shield: FastAPI backend + custom HTML/CSS/JS frontend
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

import io
import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from PIL import Image
import uvicorn

from src.model_utils import load_model, predict_image
from src.eeg_utils import extract_signal_from_image, predict_from_signal
from src.report_utils import generate_pdf, RISK_LEVELS
from ragbot import EEGAlzheimersRAG

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Neuro Shield API")

# ── lazy singletons ──
_alz_model = None
_rag_bot = None


def get_alz_model():
    global _alz_model
    if _alz_model is None:
        _alz_model = load_model()
    return _alz_model


def get_rag_bot():
    global _rag_bot
    if _rag_bot is None:
        csv_path = BASE_DIR / "data" / "neurology_faq.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Could not find {csv_path}")
        _rag_bot = EEGAlzheimersRAG(str(csv_path), use_sentence_transformers=True)
    return _rag_bot


MEASURES = {
    "No Impairment": "Maintain a healthy diet and regular exercise. Stay mentally active. Keep a regular sleep schedule.",
    "Very Mild Impairment": "Adopt a brain-healthy diet. Engage in regular physical and cognitive exercise. Manage blood pressure and cholesterol.",
    "Mild Impairment": "Establish a structured daily routine. Use memory aids. Ensure home safety modifications. Arrange caregiver check-ins.",
    "Moderate Impairment": "Ensure supervision as needed. Remove home hazards. Simplify daily tasks. Coordinate with a care team.",
    "SEIZURE": "Avoid known seizure triggers. Keep a seizure diary. Ensure a safe environment. Wear a medical alert bracelet.",
    "NON-SEIZURE": "Continue routine health monitoring. Maintain regular sleep and stress management.",
}
MEDICINE = {
    "No Impairment": "No medication indicated. Continue preventive care.",
    "Very Mild Impairment": "Discuss cholinesterase inhibitor candidacy (e.g., Donepezil) with a neurologist.",
    "Mild Impairment": "Cholinesterase inhibitors or Memantine may be considered by a specialist.",
    "Moderate Impairment": "Combination therapy should be evaluated by a neurologist.",
    "SEIZURE": "Anti-epileptic drug therapy should be evaluated by a neurologist.",
    "NON-SEIZURE": "No anti-epileptic medication indicated.",
}


def _risk_payload(label, confidence):
    risk = RISK_LEVELS.get(label, {"level": "UNKNOWN", "color": (100, 116, 139), "description": "Consult your neurologist."})
    return {
        "label": label,
        "confidence": round(confidence * 100, 1),
        "risk_level": risk["level"],
        "color": list(risk["color"]),
        "note": risk.get("description", ""),
    }


@app.post("/api/mri/predict")
async def mri_predict(
    file: UploadFile = File(...),
    patient_name: str = Form(""),
    patient_age: str = Form(""),
    patient_gender: str = Form(""),
):
    tmp_path = None
    try:
        suffix = Path(file.filename).suffix or ".png"
        tmp_path = BASE_DIR / f"_tmp_mri_{uuid.uuid4().hex}{suffix}"
        contents = await file.read()
        tmp_path.write_bytes(contents)

        model = get_alz_model()
        label, confidence = predict_image(model, str(tmp_path))

        payload = _risk_payload(label, confidence)

        report_id = f"{uuid.uuid4().hex}.pdf"
        report_path = REPORTS_DIR / report_id
        generate_pdf(
            prediction=label, confidence=confidence,
            measures=MEASURES.get(label, "Consult your neurologist."),
            medicine=MEDICINE.get(label, "Consult your neurologist."),
            patient_name=patient_name or "Unknown",
            filename=str(report_path),
            report_type="Alzheimer's MRI",
            patient_age=patient_age or None,
            patient_gender=patient_gender or None,
        )
        payload["report_id"] = report_id
        return JSONResponse(payload)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()


@app.post("/api/eeg/predict")
async def eeg_predict(
    file: UploadFile = File(...),
    patient_name: str = Form(""),
    patient_age: str = Form(""),
    patient_gender: str = Form(""),
):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")

        signal = extract_signal_from_image(img)
        pred, confidence = predict_from_signal(signal)
        label = "SEIZURE" if pred == 1 else "NON-SEIZURE"

        payload = _risk_payload(label, confidence)

        report_id = f"{uuid.uuid4().hex}.pdf"
        report_path = REPORTS_DIR / report_id
        generate_pdf(
            prediction=label, confidence=confidence,
            measures=MEASURES.get(label, "Consult your neurologist."),
            medicine=MEDICINE.get(label, "Consult your neurologist."),
            patient_name=patient_name or "Unknown",
            filename=str(report_path),
            report_type="Epilepsy EEG",
            patient_age=patient_age or None,
            patient_gender=patient_gender or None,
        )
        payload["report_id"] = report_id
        return JSONResponse(payload)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/api/report/{report_id}")
async def get_report(report_id: str):
    safe_name = Path(report_id).name  # prevent path traversal
    report_path = REPORTS_DIR / safe_name
    if not report_path.exists():
        return JSONResponse({"error": "Report not found"}, status_code=404)
    return FileResponse(str(report_path), media_type="application/pdf", filename="neuroshield_report.pdf")


@app.post("/api/chat")
async def chat(payload: dict):
    message = (payload.get("message") or "").strip()
    if not message:
        return JSONResponse({"answer": "Please enter a question."})
    try:
        bot = get_rag_bot()
        answer = bot.answer_question(message)
    except Exception as e:
        answer = f"Chatbot unavailable: {e}"
    return JSONResponse({"answer": answer})


# Serve the static frontend LAST so it doesn't shadow the /api routes above
app.mount("/", StaticFiles(directory=str(BASE_DIR / "static"), html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7860)