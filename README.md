# 🛡️ Neuro Shield — AI Brain Health Diagnostics

**Neuro Shield** is an AI-powered diagnostic platform that combines deep learning and natural language processing to assist in understanding neurological conditions.

> ⚠️ **Disclaimer:** This project is for educational and research purposes only. It is **not** intended for clinical use. Always consult a qualified neurologist for medical decisions.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Alzheimer's MRI Detection** | CNN-based 4-class classifier (No Impairment, Very Mild, Mild, Moderate) with real confidence scores |
| ⚡ **EEG Seizure Detection** | EEG graph image → signal extraction → binary seizure/non-seizure classification |
| 📚 **Neurology Q&A Chatbot** | FAISS + Sentence Transformers RAG chatbot with 50+ expert neurology Q&As |
| 📄 **PDF Reports** | Branded PDF reports with diagnosis, confidence bar, measures & medication info |
| 🌐 **React Landing Page** | Modern dark-mode landing page with animations and premium design |

---

## 🚀 Getting Started

### Python Backend (Gradio App)

```bash
# 1. Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
# Opens at http://localhost:7860
```

### React Frontend (Landing Page)

```bash
# Requires Node.js ≥18
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# Opens at http://localhost:5173

# Build for production
npm run build
```

---

## 📁 Project Structure

```
Neuro-Shield/
├── app.py                    # Main Gradio application
├── ragbot.py                 # FAISS-based RAG chatbot engine
├── requirements.txt
│
├── src/
│   ├── model_utils.py        # MRI model loading + prediction (with confidence)
│   ├── eeg_utils.py          # EEG signal extraction + seizure prediction
│   ├── report_utils.py       # Branded PDF report generation
│   ├── train_alz_model.py    # Training script for Alzheimer's CNN
│   └── train_eeg_model.py    # Training script for EEG model
│
├── models/
│   ├── best_model.keras      # Trained Alzheimer's MRI CNN
│   └── eeg_model.h5          # Trained EEG seizure detector
│
├── data/
│   ├── neurology_faq.csv     # 50+ neurology Q&A pairs for RAG chatbot
│   ├── eeg.csv               # EEG dataset samples
│   └── train/ test/          # MRI image datasets for training
│
├── videos/
│   ├── alz_video.mp4         # Alzheimer's explainer
│   └── epilepsy_video.mp4    # Epilepsy explainer
│
└── frontend/                 # React (Vite) landing page
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── App.jsx
        ├── index.css          # Design system (CSS variables, animations)
        └── components/
            ├── Navbar.jsx     # Sticky nav with glass scroll effect
            ├── Hero.jsx       # Animated hero with parallax orbs
            ├── Features.jsx   # 3-card feature showcase
            ├── HowItWorks.jsx # 4-step process section
            ├── Stats.jsx      # Animated counter statistics
            ├── Testimonials.jsx
            ├── CTA.jsx
            └── Footer.jsx
```

---

## 🔬 Technical Stack

- **Deep Learning:** TensorFlow / Keras (CNN + Dense Networks)
- **Vector Search:** FAISS (IndexFlatIP with cosine similarity)
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **EEG Processing:** OpenCV (Canny edge detection → signal extraction)
- **PDF Reports:** FPDF2 with custom branded layout
- **UI:** Gradio Blocks + React (Vite) landing page
- **Datasets:**
  - Alzheimer's MRI Dataset (4-class)
  - CHB-MIT Scalp EEG Dataset / Epileptic Seizure Recognition Dataset
  - Custom neurology FAQ knowledge base (50+ pairs)

---

## 📊 Model Performance

| Model | Task | Accuracy |
|-------|------|----------|
| CNN (ResNet-style) | Alzheimer's MRI 4-class | ~98% (dataset) |
| Dense NN | EEG Seizure Detection | ~97% (dataset) |
| FAISS RAG | Neurology Q&A retrieval | Semantic similarity |

---

## 🛠️ Development Notes

- The RAG chatbot automatically loads `data/neurology_faq.csv` — add more rows to expand the knowledge base
- PDF confidence values are now **real model probabilities**, not hardcoded
- The EEG model is cached after first load (no reload per inference)
- The React landing page links to `http://localhost:7860` (Gradio) — update the `GRADIO_URL` in components for deployment
