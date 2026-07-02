from fpdf import FPDF
from datetime import datetime
import os

# ─── Unicode → Latin-1 safe text sanitizer ──────────────────────────────────
def _safe_text(text: str) -> str:
    """Replace common Unicode chars that FPDF's built-in fonts can't encode."""
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        '\u2014': '--',   # em dash
        '\u2013': '-',    # en dash
        '\u2018': "'",    # left single quote
        '\u2019': "'",    # right single quote
        '\u201c': '"',    # left double quote
        '\u201d': '"',    # right double quote
        '\u2022': '-',    # bullet
        '\u2026': '...',  # ellipsis
        '\u00b7': '.',    # middle dot
        '\u2032': "'",    # prime
        '\u2033': '"',    # double prime
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    # Strip any remaining non-Latin-1 characters
    return text.encode('latin-1', errors='replace').decode('latin-1')


# ─── Brand Color Palette ─────────────────────────────────────────────────────
BRAND_COLORS = {
    "primary": (99, 102, 241),       # Indigo
    "primary_dark": (67, 56, 202),   # Dark Indigo
    "dark": (30, 27, 75),            # Dark Navy
    "accent": (34, 197, 94),         # Emerald
    "text": (55, 65, 81),            # Gray-700
    "text_light": (107, 114, 128),   # Gray-500
    "light_bg": (243, 244, 246),     # Gray-100
    "white": (255, 255, 255),
    "warning_bg": (255, 243, 205),   # Amber-50
    "warning_border": (250, 204, 21),# Amber-400
    "warning_text": (120, 90, 0),    # Amber-900
}

# ─── Risk Level Definitions ──────────────────────────────────────────────────
RISK_LEVELS = {
    "No Impairment": {
        "level": "LOW",
        "color": (34, 197, 94),
        "bg": (220, 252, 231),
        "description": "No significant cognitive decline detected. Brain patterns appear within normal range.",
    },
    "Very Mild Impairment": {
        "level": "MILD",
        "color": (234, 179, 8),
        "bg": (254, 249, 195),
        "description": "Very mild cognitive changes detected. Early monitoring and lifestyle adjustments recommended.",
    },
    "Mild Impairment": {
        "level": "MODERATE",
        "color": (249, 115, 22),
        "bg": (255, 237, 213),
        "description": "Mild cognitive impairment identified. Clinical follow-up and intervention strategies recommended.",
    },
    "Moderate Impairment": {
        "level": "HIGH",
        "color": (239, 68, 68),
        "bg": (254, 226, 226),
        "description": "Significant cognitive decline detected. Immediate specialist consultation recommended.",
    },
    "SEIZURE": {
        "level": "HIGH",
        "color": (239, 68, 68),
        "bg": (254, 226, 226),
        "description": "Seizure activity detected in EEG signal. Neurological evaluation strongly recommended.",
    },
    "NON-SEIZURE": {
        "level": "LOW",
        "color": (34, 197, 94),
        "bg": (220, 252, 231),
        "description": "No seizure activity detected. EEG waveform appears within normal parameters.",
    },
}

# ─── Follow-up Recommendations ───────────────────────────────────────────────
FOLLOWUP_RECS = {
    "No Impairment": [
        "Annual cognitive screening recommended",
        "Continue healthy lifestyle practices",
        "Monitor for any new cognitive symptoms",
    ],
    "Very Mild Impairment": [
        "Schedule follow-up assessment in 6 months",
        "Begin cognitive stimulation activities",
        "Consult with a neurologist for baseline evaluation",
        "Consider neuropsychological testing",
    ],
    "Mild Impairment": [
        "Urgent neurologist consultation recommended",
        "Comprehensive neuropsychological evaluation",
        "Discuss medication options with specialist",
        "Engage occupational therapy for daily task support",
        "Family/caregiver education and planning",
    ],
    "Moderate Impairment": [
        "Immediate specialist referral required",
        "Full care-plan development with multidisciplinary team",
        "Home safety assessment and modifications",
        "Caregiver support and respite care planning",
        "Legal and financial planning discussions",
    ],
    "SEIZURE": [
        "Urgent neurological consultation required",
        "Comprehensive EEG monitoring recommended",
        "Anti-epileptic medication evaluation",
        "Driving and activity restrictions review",
        "Seizure action plan development",
    ],
    "NON-SEIZURE": [
        "Routine follow-up in 12 months",
        "Continue current management plan",
        "Monitor for any new neurological symptoms",
    ],
}


class NeuroShieldPDF(FPDF):
    """Custom PDF class with branded header and footer."""

    def header(self):
        # ── Navy gradient header bar ──
        self.set_fill_color(*BRAND_COLORS["dark"])
        self.rect(0, 0, 210, 28, 'F')

        # Accent strip
        self.set_fill_color(*BRAND_COLORS["primary"])
        self.rect(0, 28, 210, 1.5, 'F')

        # Brand name
        self.set_font("Arial", 'B', 18)
        self.set_text_color(255, 255, 255)
        self.set_xy(12, 4)
        self.cell(100, 10, "NEURO SHIELD", ln=False)

        # Tagline
        self.set_font("Arial", '', 8)
        self.set_text_color(180, 180, 220)
        self.set_xy(12, 14)
        self.cell(100, 6, "AI-Powered Brain Health Diagnostics Platform", ln=False)

        # Report badge
        self.set_fill_color(*BRAND_COLORS["primary"])
        self.set_xy(140, 7)
        self.set_font("Arial", 'B', 9)
        self.set_text_color(255, 255, 255)
        self.cell(58, 14, "CLINICAL REPORT", align='C', fill=True)

        self.ln(34)

    def footer(self):
        self.set_y(-22)
        self.set_fill_color(*BRAND_COLORS["dark"])
        self.rect(0, self.get_y(), 210, 30, 'F')

        # Accent line above footer
        self.set_fill_color(*BRAND_COLORS["primary"])
        self.rect(0, self.get_y(), 210, 0.8, 'F')

        self.set_y(-18)
        self.set_font("Arial", 'I', 7)
        self.set_text_color(160, 160, 200)
        self.cell(0, 5,
                  "DISCLAIMER: This report is AI-generated for educational/research purposes only.",
                  ln=True, align='C')
        self.cell(0, 5,
                  "Professional medical consultation is required for clinical decisions. Do not use as a sole diagnostic tool.",
                  ln=True, align='C')
        self.cell(0, 5,
                  f"Generated by Neuro Shield v2.0  |  Page {self.page_no()}",
                  ln=True, align='C')

    def section_header(self, title, icon=""):
        """Draw a styled section header with colored bar."""
        self.set_fill_color(*BRAND_COLORS["primary"])
        self.rect(10, self.get_y(), 190, 10, 'F')
        # Small accent on left
        self.set_fill_color(*BRAND_COLORS["primary_dark"])
        self.rect(10, self.get_y(), 4, 10, 'F')
        self.set_font("Arial", 'B', 11)
        self.set_text_color(255, 255, 255)
        self.set_x(18)
        label = f"{icon}  {title}" if icon else title
        self.cell(178, 10, label, ln=True, align='L')
        self.ln(4)

    def info_row(self, label, value, x=15, width=85):
        """Draw a label-value pair."""
        self.set_x(x)
        self.set_font("Arial", 'B', 9)
        self.set_text_color(*BRAND_COLORS["text_light"])
        self.cell(30, 7, _safe_text(label), ln=False)
        self.set_font("Arial", '', 10)
        self.set_text_color(*BRAND_COLORS["dark"])
        self.cell(width - 30, 7, _safe_text(str(value)), ln=False)


def generate_pdf(prediction, confidence, measures, medicine, patient_name="Unknown",
                 filename="report.pdf", report_type="Alzheimer's MRI", patient_id=None,
                 patient_age=None, patient_gender=None):
    """
    Generate a branded Neuro Shield PDF report.

    Args:
        prediction: Diagnostic prediction label
        confidence: Confidence score (0.0-1.0)
        measures: Precautionary measures text
        medicine: Suggested medication text
        patient_name: Patient's full name
        filename: Output filename
        report_type: Type of diagnosis ('Alzheimer's MRI' or 'Epilepsy EEG')
        patient_id: Optional patient ID (auto-generated if None)
        patient_age: Optional patient age
        patient_gender: Optional patient gender
    """
    if patient_id is None:
        patient_id = f"NS-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    risk_info = RISK_LEVELS.get(prediction, {
        "level": "UNKNOWN",
        "color": BRAND_COLORS["primary"],
        "bg": BRAND_COLORS["light_bg"],
        "description": "Unable to determine risk level.",
    })
    followup = FOLLOWUP_RECS.get(prediction, ["Consult your neurologist for follow-up guidance."])

    pdf = NeuroShieldPDF()
    pdf.set_auto_page_break(auto=True, margin=28)
    pdf.add_page()

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 1: Patient Demographics
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.set_fill_color(*BRAND_COLORS["light_bg"])
    pdf.set_draw_color(220, 220, 230)

    # Calculate box height based on content
    box_y = pdf.get_y()
    pdf.rect(10, box_y, 190, 38, 'FD')

    # Row 1
    pdf.set_y(box_y + 4)
    pdf.info_row("Patient:", patient_name, x=15, width=85)
    pdf.info_row("Patient ID:", patient_id, x=110, width=85)
    pdf.ln(8)

    # Row 2
    age_str = str(patient_age) + " years" if patient_age else "Not specified"
    gender_str = patient_gender if patient_gender else "Not specified"
    pdf.info_row("Age:", age_str, x=15, width=85)
    pdf.info_row("Gender:", gender_str, x=110, width=85)
    pdf.ln(8)

    # Row 3
    pdf.info_row("Date:", datetime.now().strftime('%B %d, %Y  %H:%M'), x=15, width=85)
    pdf.info_row("Report Type:", report_type, x=110, width=85)

    pdf.set_y(box_y + 42)

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 2: Risk Level Assessment
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.section_header("RISK LEVEL ASSESSMENT")

    risk_y = pdf.get_y()
    pdf.set_fill_color(*risk_info["bg"])
    pdf.set_draw_color(*risk_info["color"])
    pdf.rect(15, risk_y, 180, 22, 'FD')

    # Risk badge
    pdf.set_xy(20, risk_y + 3)
    pdf.set_fill_color(*risk_info["color"])
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(255, 255, 255)
    badge_w = pdf.get_string_width(f"  {risk_info['level']}  ") + 6
    pdf.cell(badge_w, 8, f"  {risk_info['level']}  ", fill=True)

    # Risk type label
    pdf.set_x(20 + badge_w + 4)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(*BRAND_COLORS["dark"])
    pdf.cell(60, 8, "Risk Level", ln=True)

    # Risk description
    pdf.set_xy(20, risk_y + 13)
    pdf.set_font("Arial", '', 9)
    pdf.set_text_color(*BRAND_COLORS["text"])
    pdf.cell(170, 6, _safe_text(risk_info["description"]), ln=True)

    pdf.set_y(risk_y + 28)

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 3: Diagnostic Result
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.section_header("DIAGNOSTIC RESULT")

    confidence_pct = confidence * 100

    # Severity color based on prediction
    severity_colors = {
        "No Impairment": (34, 197, 94),
        "No": (34, 197, 94),
        "Very Mild Impairment": (250, 204, 21),
        "Very Mild": (250, 204, 21),
        "VeryMild": (250, 204, 21),
        "Mild Impairment": (251, 146, 60),
        "Mild": (251, 146, 60),
        "Moderate Impairment": (239, 68, 68),
        "Moderate": (239, 68, 68),
        "Severe": (127, 29, 29),
        "NON-SEIZURE": (34, 197, 94),
        "SEIZURE": (239, 68, 68),
    }
    diag_color = severity_colors.get(prediction, BRAND_COLORS["primary"])

    # Prediction label
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(*diag_color)
    pdf.set_x(15)
    pdf.cell(180, 12, _safe_text(f"Diagnosis: {prediction}"), ln=True)
    pdf.ln(2)

    # Confidence bar with label
    pdf.set_font("Arial", 'B', 9)
    pdf.set_text_color(*BRAND_COLORS["text_light"])
    pdf.set_x(15)
    pdf.cell(40, 7, "CONFIDENCE SCORE", ln=True)

    bar_x = 15
    bar_y = pdf.get_y()
    bar_width = 140

    # Bar background
    pdf.set_fill_color(230, 230, 235)
    pdf.rect(bar_x, bar_y, bar_width, 7, 'F')

    # Filled bar
    filled = (confidence_pct / 100) * bar_width
    pdf.set_fill_color(*diag_color)
    pdf.rect(bar_x, bar_y, filled, 7, 'F')

    # Confidence percentage
    pdf.set_xy(bar_x + bar_width + 4, bar_y - 1)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(*diag_color)
    pdf.cell(30, 9, f"{confidence_pct:.1f}%", ln=True)
    pdf.ln(6)

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 4: Clinical Summary
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.section_header("CLINICAL SUMMARY")

    age_text = f", age {patient_age}" if patient_age else ""
    gender_text = f" ({patient_gender})" if patient_gender else ""

    if report_type == "Alzheimer's MRI":
        summary = (
            f"Patient {patient_name}{age_text}{gender_text} underwent AI-assisted MRI brain scan analysis "
            f"using a Convolutional Neural Network (CNN) model. The analysis classified the scan as "
            f"\"{prediction}\" with a confidence score of {confidence_pct:.1f}%. "
            f"Risk level has been assessed as {risk_info['level']}. "
            f"This result should be correlated with clinical findings and further diagnostic workup."
        )
    else:
        summary = (
            f"Patient {patient_name}{age_text}{gender_text} underwent AI-assisted EEG signal analysis "
            f"using a dense neural network model with edge-detection preprocessing. The analysis "
            f"classified the EEG pattern as \"{prediction}\" with a confidence score of {confidence_pct:.1f}%. "
            f"Risk level has been assessed as {risk_info['level']}. "
            f"Clinical correlation with patient history and additional EEG monitoring is advised."
        )

    pdf.set_fill_color(248, 250, 252)
    summary_y = pdf.get_y()
    pdf.set_x(15)
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(*BRAND_COLORS["text"])
    pdf.multi_cell(180, 6, _safe_text(summary))
    pdf.ln(6)

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 5: Precautionary Measures
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.section_header("PRECAUTIONARY MEASURES")

    pdf.set_x(15)
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(*BRAND_COLORS["text"])

    # Split measures into bullet points if they contain periods
    measure_items = [m.strip() for m in _safe_text(measures).replace(". ", ".\n").split("\n") if m.strip()]
    for item in measure_items:
        pdf.set_x(18)
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(*BRAND_COLORS["primary"])
        pdf.cell(5, 6, "-", ln=False)  # Latin-1 safe bullet
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(*BRAND_COLORS["text"])
        pdf.set_x(25)
        pdf.multi_cell(170, 6, item)
        pdf.ln(1)
    pdf.ln(3)

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 6: Suggested Medications
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.section_header("SUGGESTED MEDICATIONS")

    pdf.set_x(15)
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(*BRAND_COLORS["text"])

    med_items = [m.strip() for m in _safe_text(medicine).replace(". ", ".\n").split("\n") if m.strip()]
    for item in med_items:
        pdf.set_x(18)
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(*BRAND_COLORS["primary"])
        pdf.cell(5, 6, "-", ln=False)  # Latin-1 safe bullet
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(*BRAND_COLORS["text"])
        pdf.set_x(25)
        pdf.multi_cell(170, 6, item)
        pdf.ln(1)
    pdf.ln(3)

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 7: Follow-up Recommendations
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.section_header("FOLLOW-UP RECOMMENDATIONS")

    pdf.set_fill_color(240, 242, 255)
    rec_start = pdf.get_y()

    for i, rec in enumerate(followup, 1):
        pdf.set_x(18)
        # Number badge
        pdf.set_fill_color(*BRAND_COLORS["primary"])
        pdf.set_font("Arial", 'B', 8)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(6, 6, str(i), fill=True, align='C')

        pdf.set_x(27)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(*BRAND_COLORS["text"])
        pdf.cell(168, 6, _safe_text(rec), ln=True)
        pdf.ln(2)
    pdf.ln(3)

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 8: Important Notice / Disclaimer
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.set_fill_color(*BRAND_COLORS["warning_bg"])
    pdf.set_draw_color(*BRAND_COLORS["warning_border"])
    notice_y = pdf.get_y()
    pdf.rect(10, notice_y, 190, 24, 'FD')

    # Warning icon + title
    pdf.set_xy(15, notice_y + 2)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(*BRAND_COLORS["warning_text"])
    pdf.cell(180, 7, "Important Notice", ln=True)

    pdf.set_x(15)
    pdf.set_font("Arial", '', 8)
    pdf.set_text_color(100, 75, 0)
    pdf.multi_cell(180, 5,
                   "This AI-generated report is for educational and research purposes only. "
                   "It should not replace professional medical diagnosis. Always consult a qualified "
                   "neurologist or physician for clinical interpretation, treatment decisions, and care management.")

    pdf.output(filename)
    return filename
