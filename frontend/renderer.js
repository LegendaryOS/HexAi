const { ipcRenderer } = require('electron');
const promptInput = document.getElementById('prompt-input');
const sendBtn = document.getElementById('send-btn');
const clearBtn = document.getElementById('clear-btn');
const chatMessages = document.getElementById('chat-messages');
const blueModeBtn = document.getElementById('blue-mode');
const darkModeBtn = document.getElementById('dark-mode');
const codeModeBtn = document.getElementById('code-mode');
const imageModeBtn = document.getElementById('image-mode');
const searchModeBtn = document.getElementById('search-mode');
const historyModeBtn = document.getElementById('history-mode');
const statusEl = document.getElementById('status');

let currentMode = 'gemini';

function setMode(mode) {
  currentMode = mode;
  document.body.className = mode === 'grok' ? 'dark-mode' : '';
  [blueModeBtn, darkModeBtn, codeModeBtn, imageModeBtn, searchModeBtn, historyModeBtn].forEach(btn => {
    btn.classList.remove('active');
  });
  document.getElementById(`${mode === 'gemini' ? 'blue' : mode}-mode`).classList.add('active');
  
  if (mode === 'history') {
    loadHistory();
  } else {
    chatMessages.innerHTML = '';
  }
}

async function checkBackendStatus() {
  const isOnline = await ipcRenderer.invoke('check-backend');
  statusEl.textContent = isOnline ? 'Online' : 'Offline';
  statusEl.className = `status ${isOnline ? '' : 'offline'}`;
  return isOnline;
}

async function sendPrompt() {
  const prompt = promptInput.value.trim();
  if (!prompt) return;

  if (!(await checkBackendStatus())) {
    const aiMessage = document.createElement('div');
    aiMessage.className = 'message ai';
    aiMessage.textContent = 'Offline: Please check your internet connection or backend server.';
    chatMessages.appendChild(aiMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return;
  }

  const userMessage = document.createElement('div');
  userMessage.className = 'message user';
  userMessage.textContent = prompt;
  chatMessages.appendChild(userMessage);

  let endpoint = '';
  if (currentMode === 'gemini') endpoint = '/api/gemini';
  else if (currentMode === 'grok') endpoint = '/api/grok';
  else if (currentMode === 'image') endpoint = '/api/generate-image';
  else if (currentMode === 'search') endpoint = '/api/search';
  else if (currentMode === 'code') endpoint = '/api/gemini';

  try {
    const response = await fetch(`http://127.0.0.1:5000${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: currentMode === 'code' ? `Generate code for: ${prompt}` : prompt }),
    });
    const data = await response.json();

    const aiMessage = document.createElement('div');
    aiMessage.className = 'message ai';
    aiMessage.textContent = data.error || (currentMode === 'image' ? JSON.stringify(data) : data.response || JSON.stringify(data));
    chatMessages.appendChild(aiMessage);
  } catch (error) {
    const aiMessage = document.createElement('div');
    aiMessage.className = 'message ai';
    aiMessage.textContent = `Error: ${error.message}`;
    chatMessages.appendChild(aiMessage);
  }

  promptInput.value = '';
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function loadHistory() {
  chatMessages.innerHTML = '';
  try {
    const response = await fetch('http://127.0.0.1:5000/api/history');
    const history = await response.json();
    history.forEach(entry => {
      const userMessage = document.createElement('div');
      userMessage.className = 'message history';
      userMessage.textContent = `[${entry.timestamp}] ${entry.mode.toUpperCase()} Prompt: ${entry.prompt}`;
      chatMessages.appendChild(userMessage);

      const aiMessage = document.createElement('div');
      aiMessage.className = 'message history';
      aiMessage.textContent = `Response: ${entry.response}`;
      chatMessages.appendChild(aiMessage);
    });
  } catch (error) {
    const aiMessage = document.createElement('div');
    aiMessage.className = 'message ai';
    aiMessage.textContent = `Error loading history: ${error.message}`;
    chatMessages.appendChild(aiMessage);
  }
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

blueModeBtn.addEventListener('click', () => setMode('gemini'));
darkModeBtn.addEventListener('click', () => setMode('grok'));
codeModeBtn.addEventListener('click', () => setMode('code'));
imageModeBtn.addEventListener('click', () => setMode('image'));
searchModeBtn.addEventListener('click', () => setMode('search'));
historyModeBtn.addEventListener('click', () => setMode('history'));

sendBtn.addEventListener('click', sendPrompt);
clearBtn.addEventListener('click', () => chatMessages.innerHTML = '');
promptInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendPrompt();
  }
});

// Check backend status periodically
setInterval(checkBackendStatus, 5000);
checkBackendStatus();
