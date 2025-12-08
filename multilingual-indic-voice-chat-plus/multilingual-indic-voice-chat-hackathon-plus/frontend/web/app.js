
const API = 'http://localhost:8000/api/v1';
const messagesDiv = document.getElementById('messages');
const input = document.getElementById('input');
const sendBtn = document.getElementById('send');
const speakBtn = document.getElementById('speak');
const micBtn = document.getElementById('micBtn');
const copyBtn = document.getElementById('copy');
const langSel = document.getElementById('lang');
const player = document.getElementById('player');

let lastBotText = '';
let mediaRecorder = null;
let chunks = [];

function addMessage(text, who, citations=[], confidence=null) {
  const div = document.createElement('div');
  div.className = `message ${who}`;
  div.innerHTML = text.replace(/
/g, '<br>');
  if (citations.length) {
    const cite = document.createElement('div');
    cite.className = 'cite';
    cite.textContent = 'Citations: ' + citations.join(', ');
    div.appendChild(cite);
  }
  if (confidence !== null) {
    const conf = document.createElement('div');
    conf.className = 'conf';
    conf.textContent = `Confidence: ${(confidence*100).toFixed(0)}%`;
    div.appendChild(conf);
  }
  messagesDiv.appendChild(div);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

sendBtn.onclick = async () => {
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  input.value = '';
  const lang = langSel.value;
  const res = await fetch(`${API}/chat`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, lang, channel: 'text' })
  });
  const data = await res.json();
  lastBotText = data.answer;
  addMessage(data.answer, 'bot', data.citations, data.confidence);
};

speakBtn.onclick = async () => {
  const text = lastBotText || 'Hello from Indic Voice Chat';
  const lang = langSel.value;
  const res = await fetch(`${API}/tts`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, lang })
  });
  const data = await res.json();
  player.src = 'data:audio/wav;base64,' + data.audio_base64;
  player.play();
};

copyBtn.onclick = async () => {
  if (!lastBotText) return;
  await navigator.clipboard.writeText(lastBotText);
  alert('Copied answer to clipboard');
};

micBtn.onclick = async () => {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert('Mic not supported in this browser.');
    return;
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    chunks = [];
    mediaRecorder.ondataavailable = e => chunks.push(e.data);
    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunks, { type: 'audio/webm' });
      const file = new File([blob], 'sample.webm', { type: 'audio/webm' });
      const form = new FormData();
      form.append('file', file);
      const res = await fetch(`${API}/asr`, { method: 'POST', body: form });
      const data = await res.json();
      addMessage('[ASR Transcript] ' + data.text, 'user');
    };
    mediaRecorder.start();
    setTimeout(() => mediaRecorder.stop(), 2000);
  } catch (err) {
    alert('Mic error: ' + err);
  }
};
