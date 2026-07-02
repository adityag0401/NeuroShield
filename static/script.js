// ── Navigation ──
document.querySelectorAll('.nav-btn, .go-to').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.target;
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.getElementById(target).classList.add('active');
    document.querySelectorAll('.nav-btn').forEach(n => n.classList.toggle('active', n.dataset.target === target));
  });
});

// ── Image previews ──
function wirePreview(inputId, previewId) {
  const input = document.getElementById(inputId);
  const preview = document.getElementById(previewId);
  input.addEventListener('change', () => {
    if (input.files && input.files[0]) {
      preview.src = URL.createObjectURL(input.files[0]);
      preview.style.display = 'block';
    }
  });
}
wirePreview('mri-file', 'mri-preview');
wirePreview('eeg-file', 'eeg-preview');

// ── Result renderer ──
function renderResult(container, data) {
  if (data.error) {
    container.innerHTML = `<div class="placeholder-text">❌ ${data.error}</div>`;
    return;
  }
  const [r, g, b] = data.color;
  container.innerHTML = `
    <div class="result-top">
      <div class="result-label">${data.label}</div>
      <div class="risk-chip" style="background: rgba(${r},${g},${b},0.15); color: rgb(${r},${g},${b});">${data.risk_level} RISK</div>
    </div>
    <div class="conf-track"><div class="conf-fill" style="background: rgb(${r},${g},${b});"></div></div>
    <div class="conf-pct">${data.confidence}% model confidence</div>
    <div class="result-note">${data.note}</div>
    <a class="download-link" href="/api/report/${data.report_id}" target="_blank">📄 Download PDF Report</a>
  `;
  requestAnimationFrame(() => {
    container.querySelector('.conf-fill').style.width = data.confidence + '%';
  });
}

// ── MRI ──
document.getElementById('mri-btn').addEventListener('click', async () => {
  const fileInput = document.getElementById('mri-file');
  const resultBox = document.getElementById('mri-result');
  if (!fileInput.files[0]) { resultBox.innerHTML = '<div class="placeholder-text">⚠️ Please upload an MRI image first.</div>'; return; }

  const btn = document.getElementById('mri-btn');
  btn.disabled = true; btn.textContent = 'Analyzing...';
  resultBox.innerHTML = '<div class="placeholder-text">Analyzing MRI scan...</div>';

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('patient_name', document.getElementById('mri-name').value);
  formData.append('patient_age', document.getElementById('mri-age').value);
  formData.append('patient_gender', document.getElementById('mri-gender').value);

  try {
    const res = await fetch('/api/mri/predict', { method: 'POST', body: formData });
    const data = await res.json();
    renderResult(resultBox, data);
  } catch (e) {
    resultBox.innerHTML = `<div class="placeholder-text">❌ Request failed: ${e}</div>`;
  } finally {
    btn.disabled = false; btn.textContent = '🔍 Analyze MRI';
  }
});

// ── EEG ──
document.getElementById('eeg-btn').addEventListener('click', async () => {
  const fileInput = document.getElementById('eeg-file');
  const resultBox = document.getElementById('eeg-result');
  if (!fileInput.files[0]) { resultBox.innerHTML = '<div class="placeholder-text">⚠️ Please upload an EEG graph image first.</div>'; return; }

  const btn = document.getElementById('eeg-btn');
  btn.disabled = true; btn.textContent = 'Analyzing...';
  resultBox.innerHTML = '<div class="placeholder-text">Analyzing EEG signal...</div>';

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('patient_name', document.getElementById('eeg-name').value);
  formData.append('patient_age', document.getElementById('eeg-age').value);
  formData.append('patient_gender', document.getElementById('eeg-gender').value);

  try {
    const res = await fetch('/api/eeg/predict', { method: 'POST', body: formData });
    const data = await res.json();
    renderResult(resultBox, data);
  } catch (e) {
    resultBox.innerHTML = `<div class="placeholder-text">❌ Request failed: ${e}</div>`;
  } finally {
    btn.disabled = false; btn.textContent = '🔍 Analyze EEG';
  }
});

// ── Chatbot ──
const chatLog = document.getElementById('chat-log');
const chatInput = document.getElementById('chat-input');

function addBubble(text, who) {
  const div = document.createElement('div');
  div.className = `chat-bubble ${who}`;
  div.textContent = text;
  chatLog.appendChild(div);
  chatLog.scrollTop = chatLog.scrollHeight;
}

async function sendChat() {
  const msg = chatInput.value.trim();
  if (!msg) return;
  addBubble(msg, 'user');
  chatInput.value = '';
  addBubble('Thinking...', 'bot');
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg }),
    });
    const data = await res.json();
    chatLog.lastChild.remove();
    addBubble(data.answer, 'bot');
  } catch (e) {
    chatLog.lastChild.remove();
    addBubble('❌ Chatbot request failed: ' + e, 'bot');
  }
}

document.getElementById('chat-send').addEventListener('click', sendChat);
chatInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') sendChat(); });