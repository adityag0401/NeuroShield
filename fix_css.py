"""
Smart repair: replace CUSTOM_CSS block using a known unique anchor after it.
The CUSTOM_CSS string ends right before the blank line + next Python definition.
We'll find it by looking for the pattern: gap-4 ... """ which is the end of CSS.
"""

NEW_CSS_BLOCK = '''CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box !important; }

/* Root background */
body, .gradio-container {
    background: linear-gradient(160deg, #f0fdf4 0%, #dcfce7 40%, #f0fdf4 100%) !important;
    background-attachment: fixed !important;
    min-height: 100vh !important;
}

.gradio-container::before {
    content: '';
    position: fixed;
    top: -200px; left: -200px;
    width: 600px; height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(22,163,74,0.08) 0%, transparent 70%);
    pointer-events: none; z-index: 0;
}

/* Tabs */
.tabs > .tab-nav {
    background: #ffffff !important;
    border-radius: 14px !important; padding: 6px !important;
    margin-bottom: 24px !important;
    border: 1px solid rgba(22,163,74,0.25) !important;
    box-shadow: 0 2px 12px rgba(22,163,74,0.1) !important;
}
.tabs > .tab-nav button {
    color: #4b7a55 !important; border-radius: 10px !important;
    font-weight: 500 !important; font-size: 0.9rem !important;
    padding: 10px 18px !important; transition: all 0.25s ease !important;
}
.tabs > .tab-nav button:hover {
    background: rgba(22,163,74,0.08) !important; color: #15803d !important;
}
.tabs > .tab-nav button.selected {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(22,163,74,0.35) !important;
    font-weight: 600 !important;
}

/* Cards */
.block, .form {
    background: #ffffff !important;
    border: 1px solid rgba(22,163,74,0.18) !important;
    border-radius: 20px !important;
    box-shadow: 0 2px 12px rgba(22,163,74,0.06) !important;
    padding: 20px !important; margin-bottom: 16px !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}
.block:hover { border-color: rgba(22,163,74,0.35) !important; box-shadow: 0 4px 20px rgba(22,163,74,0.12) !important; }

/* Labels */
label, .label-wrap span {
    color: #1f4e2e !important; font-weight: 600 !important;
    font-size: 0.85rem !important; text-transform: uppercase !important;
    letter-spacing: 0.5px !important; margin-bottom: 6px !important;
}

/* Inputs */
textarea, input[type="text"], input {
    background: #f8fffe !important; color: #1a2e1f !important;
    border: 1.5px solid rgba(22,163,74,0.25) !important;
    border-radius: 12px !important; padding: 12px 16px !important;
    font-size: 0.95rem !important; transition: border-color 0.25s !important;
}
textarea:focus, input:focus {
    border-color: #16a34a !important;
    box-shadow: 0 0 0 3px rgba(22,163,74,0.12) !important;
}

/* Primary button */
button.primary, .gr-button-primary {
    background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 600 !important;
    font-size: 1rem !important; padding: 12px 28px !important;
    box-shadow: 0 4px 16px rgba(22,163,74,0.3) !important;
    transition: all 0.25s ease !important;
}
button.primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(22,163,74,0.45) !important;
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
}
button.primary:active { transform: translateY(0) !important; }

/* Secondary button */
button.secondary {
    background: rgba(22,163,74,0.07) !important;
    border: 1.5px solid rgba(22,163,74,0.3) !important;
    color: #15803d !important; border-radius: 12px !important;
    font-weight: 500 !important; transition: all 0.2s !important;
}
button.secondary:hover {
    background: rgba(22,163,74,0.14) !important;
    border-color: rgba(22,163,74,0.55) !important;
}

/* Small buttons */
button.sm {
    background: rgba(22,163,74,0.07) !important;
    border: 1px solid rgba(22,163,74,0.2) !important;
    color: #166534 !important; border-radius: 8px !important;
    font-size: 0.82rem !important; transition: all 0.2s !important;
}
button.sm:hover { background: rgba(22,163,74,0.16) !important; color: #14532d !important; }

/* Markdown */
.markdown-text, .output-markdown, .md-content { color: #1a2e1f !important; line-height: 1.7 !important; }
.prose h1, .prose h2, .prose h3 { color: #15803d !important; }
.prose strong { color: #166534 !important; }
.prose a { color: #16a34a !important; }

/* Chatbot */
.chatbot { background: transparent !important; }
.chatbot .message.bot { background: #f0fdf4 !important; border: 1px solid rgba(22,163,74,0.22) !important; border-radius: 16px !important; color: #1a2e1f !important; }
.chatbot .message.user { background: linear-gradient(135deg, #16a34a, #15803d) !important; border-radius: 16px !important; color: white !important; }

/* File upload */
.upload-container, .upload-btn-wrapper {
    border: 2px dashed rgba(22,163,74,0.3) !important;
    border-radius: 16px !important; background: #f0fdf4 !important;
    transition: all 0.25s !important;
}
.upload-container:hover { border-color: rgba(22,163,74,0.6) !important; background: #dcfce7 !important; }

.image-container img { border-radius: 14px !important; border: 1px solid rgba(22,163,74,0.2) !important; }
.file { background: #f0fdf4 !important; border: 1px solid rgba(22,163,74,0.25) !important; border-radius: 12px !important; color: #15803d !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f0fdf4; }
::-webkit-scrollbar-thumb { background: rgba(22,163,74,0.35); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(22,163,74,0.6); }

/* Misc */
input[type="range"] { accent-color: #16a34a !important; }
video { border-radius: 16px !important; border: 1px solid rgba(22,163,74,0.2) !important; }
.ns-info-card { background: #f0fdf4; border: 1px solid rgba(22,163,74,0.2); border-radius: 14px; padding: 14px 18px; margin: 12px 0; display: flex; align-items: flex-start; gap: 12px; font-size: 0.88rem; color: #1f4e2e; line-height: 1.5; }
.ns-info-card .ns-icon { font-size: 1.5rem; flex-shrink: 0; margin-top: 2px; }
.ns-stat { display: inline-flex; align-items: center; gap: 6px; background: rgba(22,163,74,0.1); border: 1px solid rgba(22,163,74,0.28); border-radius: 20px; padding: 4px 12px; font-size: 0.82rem; font-weight: 600; color: #15803d; }
hr { border-color: rgba(22,163,74,0.15) !important; margin: 20px 0 !important; }
.gap-4 { gap: 16px !important; }
"""

'''

# The unique anchor right after CUSTOM_CSS in the original file
ANCHOR_AFTER_CSS = '\n# ───────────────────────────────────────────────\n# Load Models'

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Verify anchor exists
if ANCHOR_AFTER_CSS not in content:
    print("ERROR: anchor not found in app.py. Contents may be too corrupted.")
    print("First 500 chars:", content[:500])
else:
    anchor_pos = content.index(ANCHOR_AFTER_CSS)
    css_start = content.index('CUSTOM_CSS = ')
    print(f"CUSTOM_CSS starts at: {css_start}")
    print(f"Anchor (Load Models comment) at: {anchor_pos}")
    print(f"Replacing chars {css_start}..{anchor_pos}")
    
    content = content[:css_start] + NEW_CSS_BLOCK + content[anchor_pos:]
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("app.py fully repaired.")
