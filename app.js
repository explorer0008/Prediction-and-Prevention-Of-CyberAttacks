// Simple client-side auth and small helpers for the demo frontend
// NOTE: This is purely for demonstration. Do NOT use client-side
// credentials in production. Replace with secure backend auth later.

const ADMIN_CREDENTIALS = { username: 'Divyanshu', password: '12345' };

function showMessage(el, msg, isError = false) {
  if (!el) return;
  el.textContent = msg;
  el.style.color = isError ? '#b91c1c' : ''; // red for error
}

function handleLogin(event) {
  event.preventDefault();
  const u = document.getElementById('username')?.value?.trim();
  const p = document.getElementById('password')?.value ?? '';
  const messageEl = document.getElementById('loginMessage');

  if (!u || !p) {
    showMessage(messageEl, 'Please enter username and password', true);
    return;
  }

  if (u === ADMIN_CREDENTIALS.username && p === ADMIN_CREDENTIALS.password) {
    // mark admin session locally
    localStorage.setItem('isAdmin', 'true');
    localStorage.setItem('adminUser', u);
    showMessage(messageEl, 'Login successful — redirecting...');
    // If a post-login demo flag is set, redirect to demo hub
    const wantsDemo = sessionStorage.getItem('postLoginDemo') === '1';
    setTimeout(() => {
      sessionStorage.removeItem('postLoginDemo');
      if (wantsDemo) window.location.href = 'demo.html';
      else window.location.href = 'dashboard.html';
    }, 600);
  } else {
    showMessage(messageEl, 'Invalid credentials', true);
  }
}

function checkAuth() {
  const isAdmin = localStorage.getItem('isAdmin') === 'true';
  if (!isAdmin) {
    // redirect to login (index)
    window.location.href = 'index.html';
  }
}

function logout() {
  localStorage.removeItem('isAdmin');
  localStorage.removeItem('adminUser');
  window.location.href = 'index.html';
}

function simulateAnalysis() {
  const el = document.getElementById('simResult');
  if (!el) return;
  el.textContent = 'Running simulated analysis...';
  setTimeout(() => {
    el.textContent = 'Demo result: Detected 3 suspicious flows. Accuracy estimate (simulated): 94.5%.';
  }, 1200);
}

// Notes saving/loading helpers (use localStorage)
function saveNote(id) {
  const ta = document.getElementById(id);
  if (!ta) return;
  localStorage.setItem(id, ta.value);
  const msg = document.getElementById(id + 'Msg');
  if (msg) { msg.textContent = 'Saved'; setTimeout(()=> msg.textContent = '', 1200); }
}

function clearNote(id) {
  const ta = document.getElementById(id);
  if (!ta) return;
  ta.value = '';
  localStorage.removeItem(id);
}

function loadNote(id) {
  const ta = document.getElementById(id);
  if (!ta) return;
  const v = localStorage.getItem(id);
  if (v) ta.value = v;
}

// Wire up form handler if present
window.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');
  if (loginForm) loginForm.addEventListener('submit', handleLogin);
  // If front page has a Show Demo link, wire it
  const showDemoLink = document.getElementById('showDemoLink');
    if (showDemoLink) {
    window.showDemo = function (ev) {
      if (ev) ev.preventDefault();
      const isAdmin = localStorage.getItem('isAdmin') === 'true';
      if (isAdmin) {
        // go to demo hub
        window.location.href = 'demo.html';
      } else {
        // remember intent and go to login (index)
        sessionStorage.setItem('postLoginDemo', '1');
        window.location.href = 'index.html';
      }
    };
  }
  // Load and wire note areas on prediction/prevention pages
  // Prediction notes
  if (document.getElementById('predictionNotes')) {
    loadNote('predictionNotes');
    const saveBtn = document.getElementById('savePredictionNotes');
    const clearBtn = document.getElementById('clearPredictionNotes');
    if (saveBtn) saveBtn.addEventListener('click', ()=> saveNote('predictionNotes'));
    if (clearBtn) clearBtn.addEventListener('click', ()=> clearNote('predictionNotes'));
  }
  // Prevention notes (removed pages) — keep code safe if future page added
  if (document.getElementById('preventionNotes')) {
    loadNote('preventionNotes');
    const saveBtn = document.getElementById('savePreventionNotes');
    const clearBtn = document.getElementById('clearPreventionNotes');
    if (saveBtn) saveBtn.addEventListener('click', ()=> saveNote('preventionNotes'));
    if (clearBtn) clearBtn.addEventListener('click', ()=> clearNote('preventionNotes'));
  }
});

// When dashboard loads, check hash and run demo if requested
function dashboardAutoDemo() {
  try {
    const isAdmin = localStorage.getItem('isAdmin') === 'true';
    if (!isAdmin) return; // checkAuth on dashboard will redirect if not admin
    if (window.location.hash === '#demo') {
      // small timeout to allow DOM to be ready
      setTimeout(() => {
        if (typeof simulateAnalysis === 'function') simulateAnalysis();
      }, 400);
    }
  } catch (e) { /* ignore */ }
}

// Try running auto demo on load too (useful when dashboard onload runs checkAuth())
window.addEventListener('load', dashboardAutoDemo);
