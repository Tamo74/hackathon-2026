/* accessibility.js — TTS + save with error handling */

// ── Voice list ──────────────────────────────────────────────
let voices = [];
let selectedVoice = null;

function populateVoices() {
  voices = speechSynthesis.getVoices();
  const sel = document.getElementById('ttsVoice');
  if (!sel) return;

  sel.innerHTML = '';
  if (!voices.length) {
    sel.innerHTML = '<option value="">No voices available</option>';
    return;
  }

  voices.forEach((v, i) => {
    const opt = document.createElement('option');
    opt.value = i;
    opt.textContent = `${v.name} (${v.lang})`;
    // Pre-select a voice matching page language if possible
    const lang = document.getElementById('language')?.value || 'en';
    if (!selectedVoice && v.lang.startsWith(lang.slice(0, 2))) {
      opt.selected = true;
      selectedVoice = v;
    }
    sel.appendChild(opt);
  });
}

if (typeof speechSynthesis !== 'undefined') {
  speechSynthesis.onvoiceschanged = populateVoices;
  populateVoices();
}

function updateVoice(sel) {
  selectedVoice = voices[parseInt(sel.value)] || null;
}

// ── TTS preview section visibility ──────────────────────────
function toggleTTSSection(checkbox) {
  const section = document.getElementById('ttsOptions');
  if (section) section.classList.toggle('hidden', !checkbox.checked);
}

// ── Preview button ───────────────────────────────────────────
function previewTTS() {
  if (typeof speechSynthesis === 'undefined') {
    showToast('Text-to-speech is not supported in this browser.', 'error');
    return;
  }

  const btn   = document.getElementById('ttsPlayBtn');
  const waves = document.getElementById('ttsWaves');
  const txt   = document.getElementById('ttsPreviewText');

  if (speechSynthesis.speaking) {
    speechSynthesis.cancel();
    btn.classList.remove('speaking');
    if (waves) waves.classList.remove('active');
    if (txt)   txt.style.display = 'block';
    btn.querySelector('svg').innerHTML = '<path d="M5 3l14 9-14 9V3z"/>';
    return;
  }

  const previewText = txt?.textContent.trim() || 'Hello. Text to speech is working correctly.';
  const utterance   = new SpeechSynthesisUtterance(previewText);

  utterance.rate  = parseFloat(document.getElementById('ttsRate')?.value  || '1');
  utterance.pitch = parseFloat(document.getElementById('ttsPitch')?.value || '1');
  if (selectedVoice) utterance.voice = selectedVoice;

  utterance.onstart = () => {
    btn.classList.add('speaking');
    if (waves) waves.classList.add('active');
    if (txt)   txt.style.display = 'none';
    btn.querySelector('svg').innerHTML =
      '<rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>';
  };

  utterance.onend = utterance.onerror = () => {
    btn.classList.remove('speaking');
    if (waves) waves.classList.remove('active');
    if (txt)   txt.style.display = 'block';
    btn.querySelector('svg').innerHTML = '<path d="M5 3l14 9-14 9V3z"/>';
  };

  speechSynthesis.speak(utterance);
}

// ── Read an element aloud (used for TTS-on-focus/click) ──────
function speakElement(el) {
  const ttsEnabled = document.getElementById('tts')?.checked;
  if (!ttsEnabled || typeof speechSynthesis === 'undefined') return;
  if (speechSynthesis.speaking) speechSynthesis.cancel();

  const u = new SpeechSynthesisUtterance(el.textContent.trim());
  u.rate  = parseFloat(document.getElementById('ttsRate')?.value  || '1');
  u.pitch = parseFloat(document.getElementById('ttsPitch')?.value || '1');
  if (selectedVoice) u.voice = selectedVoice;
  speechSynthesis.speak(u);
}

// Attach TTS click handlers to all labels
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('label, .toggle-label strong').forEach(el => {
    el.addEventListener('click', () => speakElement(el));
  });
});

// ── Toast notification ────────────────────────────────────────
function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  const label = document.getElementById('toastMsg');
  if (!toast || !label) return;
  toast.className = `toast ${type}`;
  label.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3200);
}

// ── Save accessibility settings ───────────────────────────────
async function saveAccessibility() {
  const payload = {
    text_size:     parseInt(document.getElementById('textSize').value),
    icon_size:     parseInt(document.getElementById('iconSize').value),
    tts:           document.getElementById('tts').checked ? 1 : 0,
    autoscroll:    document.getElementById('autoscroll').checked ? 1 : 0,
    dark_mode:     document.getElementById('darkMode').checked ? 1 : 0,
    colour_filter: document.getElementById('colourFilter').value,
    language:      document.getElementById('language').value
  };

  try {
    const response = await fetch('/settings/accessibility/update', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status} ${response.statusText}`);
    }

    showToast('Settings saved!', 'success');
    setTimeout(() => location.reload(), 1200);

  } catch (error) {
    if (error instanceof TypeError) {
      console.error('Network error:', error);
      showToast('Network error — could not reach server.', 'error');
    } else {
      console.error('Save failed:', error);
      showToast(error.message || 'Could not save settings.', 'error');
    }
  }
}