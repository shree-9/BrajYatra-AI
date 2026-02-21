/* ═══════════════════════════════════════════════════════
   BrajYatra AI — Sacred Spiritual Frontend
   Krishna-inspired · Bansuri melody · Warm particles
   ═══════════════════════════════════════════════════════ */

const API_BASE = window.location.origin;

// ─── State ───
let chatHistory = [];
let currentSessionId = null;
let audioPlaying = false;

// ─── DOM ───
const landing = document.getElementById('landing');
const chatApp = document.getElementById('chatApp');
const startBtn = document.getElementById('startBtn');
const chatArea = document.getElementById('chatArea');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const canvas = document.getElementById('particleCanvas');
const audioToggle = document.getElementById('audioToggle');


/* ═══════════════════════════════════════════════════════
   KRISHNA BANSURI SYNTHESIZER
   Realistic pentatonic flute melody using Web Audio API
   Raga Yaman-inspired scale with natural vibrato
   ═══════════════════════════════════════════════════════ */

class BansuriPlayer {
    constructor() {
        this.ctx = null;
        this.masterGain = null;
        this.playing = false;
        this.loopTimer = null;

        // Raga Yaman / Bhairavi notes (Hz) — deeply spiritual
        this.scales = {
            yaman: [261.63, 293.66, 329.63, 369.99, 392.00, 440.00, 493.88, 523.25],
            bhairavi: [261.63, 277.18, 311.13, 329.63, 392.00, 415.30, 466.16, 523.25]
        };

        // Slow, meditative Krishna melody patterns
        this.melodies = [
            [4, -1, 5, 4, 3, 2, -1, 3, 4, 5, 7, -1, 5, 4, 3, -1, 2, 3, 2, 0],
            [0, 2, 3, 4, -1, 5, 4, 3, 2, 0, -1, 2, 4, 5, 7, 5, -1, 4, 3, 2],
            [5, 4, 5, 7, -1, 5, 4, 3, 4, 2, -1, 0, 2, 3, 4, -1, 3, 2, 0, -1],
        ];
        this.currentMelody = 0;
    }

    start() {
        if (this.playing) return;
        try {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();

            // Master gain
            this.masterGain = this.ctx.createGain();
            this.masterGain.gain.value = 0;
            this.masterGain.gain.linearRampToValueAtTime(0.28, this.ctx.currentTime + 2);

            // Reverb (convolution-like using delay)
            const delay = this.ctx.createDelay();
            delay.delayTime.value = 0.12;
            const feedback = this.ctx.createGain();
            feedback.gain.value = 0.25;
            const reverbFilter = this.ctx.createBiquadFilter();
            reverbFilter.type = 'lowpass';
            reverbFilter.frequency.value = 2500;

            this.masterGain.connect(this.ctx.destination);
            this.masterGain.connect(delay);
            delay.connect(feedback);
            feedback.connect(reverbFilter);
            reverbFilter.connect(delay);
            reverbFilter.connect(this.ctx.destination);

            this.playing = true;
            this._playLoop();
        } catch (e) {
            console.warn('Bansuri init failed:', e);
        }
    }

    _playNote(freq, startTime, duration) {
        if (!this.ctx || !this.playing) return;

        // Primary tone (sine — flute body)
        const osc1 = this.ctx.createOscillator();
        osc1.type = 'sine';
        osc1.frequency.value = freq;

        // Breathy overtone (triangle, octave up, quiet)
        const osc2 = this.ctx.createOscillator();
        osc2.type = 'triangle';
        osc2.frequency.value = freq * 2.002;

        // Soft sub tone
        const osc3 = this.ctx.createOscillator();
        osc3.type = 'sine';
        osc3.frequency.value = freq * 0.999;

        // Natural vibrato (slower, gentler)
        const vibrato = this.ctx.createOscillator();
        vibrato.type = 'sine';
        vibrato.frequency.value = 4.5 + Math.random() * 1.5;
        const vibGain = this.ctx.createGain();
        vibGain.gain.value = 2.5 + Math.random();
        vibrato.connect(vibGain);
        vibGain.connect(osc1.frequency);
        vibGain.connect(osc3.frequency);

        // Breath noise
        const bufferSize = this.ctx.sampleRate * duration;
        const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const noise = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            noise[i] = (Math.random() * 2 - 1) * 0.015;
        }
        const noiseSrc = this.ctx.createBufferSource();
        noiseSrc.buffer = noiseBuffer;
        const noiseFilter = this.ctx.createBiquadFilter();
        noiseFilter.type = 'bandpass';
        noiseFilter.frequency.value = freq * 2;
        noiseFilter.Q.value = 2;
        noiseSrc.connect(noiseFilter);

        // Main envelope — slow breath attack/release
        const env = this.ctx.createGain();
        const attack = 0.25 + Math.random() * 0.12;
        env.gain.setValueAtTime(0, startTime);
        env.gain.linearRampToValueAtTime(0.75, startTime + attack);
        env.gain.setValueAtTime(0.75, startTime + duration * 0.5);
        env.gain.linearRampToValueAtTime(0.3, startTime + duration * 0.8);
        env.gain.exponentialRampToValueAtTime(0.001, startTime + duration);

        // Sub/overtone levels
        const subGain = this.ctx.createGain();
        subGain.gain.value = 0.3;
        const overGain = this.ctx.createGain();
        overGain.gain.value = 0.06;

        // Connect
        osc1.connect(env);
        osc3.connect(subGain);
        subGain.connect(env);
        osc2.connect(overGain);
        overGain.connect(env);
        noiseFilter.connect(env);
        env.connect(this.masterGain);

        // Start & stop
        const end = startTime + duration + 0.05;
        [osc1, osc2, osc3, vibrato, noiseSrc].forEach(s => {
            s.start(startTime);
            s.stop(end);
        });
    }

    _playLoop() {
        if (!this.playing || !this.ctx) return;

        const notes = this.scales.yaman;
        const melody = this.melodies[this.currentMelody];
        this.currentMelody = (this.currentMelody + 1) % this.melodies.length;

        const now = this.ctx.currentTime + 0.2;
        let time = now;

        for (const idx of melody) {
            if (idx === -1) {
                // Rest / silence
                time += 1.2 + Math.random() * 0.6;
            } else {
                const dur = 1.6 + Math.random() * 1.0;
                this._playNote(notes[idx], time, dur);
                time += dur + 0.1 + Math.random() * 0.2;
            }
        }

        const loopDuration = (time - now + 2.5) * 1000;
        this.loopTimer = setTimeout(() => this._playLoop(), loopDuration);
    }

    stop() {
        this.playing = false;
        if (this.loopTimer) clearTimeout(this.loopTimer);
        if (this.masterGain && this.ctx) {
            this.masterGain.gain.linearRampToValueAtTime(0, this.ctx.currentTime + 1);
        }
        setTimeout(() => {
            if (this.ctx) {
                this.ctx.close().catch(() => { });
                this.ctx = null;
            }
        }, 1200);
    }

    toggle() {
        if (this.playing) { this.stop(); return false; }
        else { this.start(); return true; }
    }
}

const bansuri = new BansuriPlayer();

audioToggle.addEventListener('click', () => {
    const isPlaying = bansuri.toggle();
    audioToggle.classList.toggle('muted', !isPlaying);
    audioToggle.textContent = isPlaying ? '🎵' : '🔇';
    audioPlaying = isPlaying;
});


/* ═══════════════════════════════════════════════════════
   SACRED PARTICLE SYSTEM
   Warm diya-like glowing particles with golden connections
   ═══════════════════════════════════════════════════════ */

class SacredParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: -1000, y: -1000 };
        this.running = true;
        this.frame = 0;

        this.resize();
        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });

        this.init();
        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    init() {
        const count = Math.min(80, Math.floor((window.innerWidth * window.innerHeight) / 14000));
        this.particles = [];

        for (let i = 0; i < count; i++) {
            const type = Math.random();
            let hue, sat, light, glow;

            if (type < 0.35) {
                // Diya flame gold
                hue = 38 + Math.random() * 8;
                sat = 90 + Math.random() * 10;
                light = 55 + Math.random() * 10;
                glow = true;
            } else if (type < 0.6) {
                // Deep saffron
                hue = 20 + Math.random() * 12;
                sat = 95 + Math.random() * 5;
                light = 50 + Math.random() * 10;
                glow = Math.random() > 0.5;
            } else if (type < 0.8) {
                // Warm turmeric
                hue = 45 + Math.random() * 8;
                sat = 80 + Math.random() * 15;
                light = 58 + Math.random() * 10;
                glow = false;
            } else {
                // Temple vermillion
                hue = 5 + Math.random() * 10;
                sat = 75 + Math.random() * 20;
                light = 55 + Math.random() * 8;
                glow = Math.random() > 0.6;
            }

            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.3,
                vy: (Math.random() - 0.5) * 0.3 - 0.1, // slight upward drift (like flame)
                radius: Math.random() * 2.2 + 0.8,
                baseOpacity: Math.random() * 0.35 + 0.15,
                opacity: 0,
                hue, sat, light, glow,
                flicker: Math.random() * Math.PI * 2
            });
        }
    }

    animate() {
        if (!this.running) return;
        this.frame++;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.update();
        this.draw();
        requestAnimationFrame(() => this.animate());
    }

    update() {
        for (const p of this.particles) {
            // Mouse repulsion
            const dx = this.mouse.x - p.x;
            const dy = this.mouse.y - p.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 150) {
                p.vx += dx * 0.00008;
                p.vy += dy * 0.00008;
            }

            p.x += p.vx;
            p.y += p.vy;
            p.vx *= 0.998;
            p.vy *= 0.998;

            // Flickering opacity (like diya flame)
            p.flicker += 0.03 + Math.random() * 0.01;
            p.opacity = p.baseOpacity + Math.sin(p.flicker) * 0.08;

            // Wrap around
            if (p.x < -10) p.x = this.canvas.width + 10;
            if (p.x > this.canvas.width + 10) p.x = -10;
            if (p.y < -10) p.y = this.canvas.height + 10;
            if (p.y > this.canvas.height + 10) p.y = -10;
        }
    }

    draw() {
        // Golden connection threads
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const a = this.particles[i], b = this.particles[j];
                const dx = a.x - b.x, dy = a.y - b.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 100) {
                    const alpha = (1 - dist / 100) * 0.06;
                    this.ctx.strokeStyle = `hsla(38, 85%, 55%, ${alpha})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.beginPath();
                    this.ctx.moveTo(a.x, a.y);
                    this.ctx.lineTo(b.x, b.y);
                    this.ctx.stroke();
                }
            }
        }

        // Particles with glow
        for (const p of this.particles) {
            if (p.glow) {
                // Soft glow aura
                const gradient = this.ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.radius * 6);
                gradient.addColorStop(0, `hsla(${p.hue}, ${p.sat}%, ${p.light}%, ${p.opacity * 0.3})`);
                gradient.addColorStop(1, `hsla(${p.hue}, ${p.sat}%, ${p.light}%, 0)`);
                this.ctx.fillStyle = gradient;
                this.ctx.beginPath();
                this.ctx.arc(p.x, p.y, p.radius * 6, 0, Math.PI * 2);
                this.ctx.fill();
            }

            // Core dot
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = `hsla(${p.hue}, ${p.sat}%, ${p.light}%, ${p.opacity})`;
            this.ctx.fill();
        }
    }

    stop() { this.running = false; }
}

let particleSystem;


/* ═══════════════════════════════════════════════════════
   LANDING → CHAT TRANSITION
   ═══════════════════════════════════════════════════════ */

startBtn.addEventListener('click', () => {
    // Start bansuri on first gesture (browser policy)
    if (!audioPlaying) {
        bansuri.start();
        audioPlaying = true;
        audioToggle.textContent = '🎵';
        audioToggle.classList.remove('muted');
    }

    landing.classList.add('fade-out');
    setTimeout(() => {
        landing.classList.add('gone');
        if (particleSystem) particleSystem.stop();
        chatApp.classList.remove('hidden');
        chatApp.classList.add('visible');
        showWelcome();
        chatInput.focus();
    }, 900);
});


/* ═══════════════════════════════════════════════════════
   WELCOME SCREEN
   ═══════════════════════════════════════════════════════ */

function showWelcome() {
    chatArea.innerHTML = `
        <div class="welcome-block">
            <div class="welcome-om">🙏</div>
            <h2 class="welcome-title">Namaste! I'm BrajYatra AI</h2>
            <div class="welcome-mantra">॥ राधे राधे · हरे कृष्ण ॥</div>
            <p class="welcome-sub">
                I'm your AI guide for the sacred Braj region — home of Lord Krishna.
                Plan pilgrimages, check darshan times, explore temples, and immerse yourself in devotion.
            </p>
            <div class="suggestion-grid">
                <div class="suggestion-card" onclick="useSuggestion(this)">
                    <div class="sg-title">🛕 Spiritual Yatra</div>
                    Plan a 3-day spiritual pilgrimage to Mathura and Vrindavan
                </div>
                <div class="suggestion-card" onclick="useSuggestion(this)">
                    <div class="sg-title">🏰 Heritage Explorer</div>
                    2-day heritage tour of Agra and Mathura on a budget
                </div>
                <div class="suggestion-card" onclick="useSuggestion(this)">
                    <div class="sg-title">👨‍👩‍👧‍👦 Family Yatra</div>
                    Plan a family-friendly 4-day trip to all Braj cities
                </div>
                <div class="suggestion-card" onclick="useSuggestion(this)">
                    <div class="sg-title">🌤️ Check Weather</div>
                    What's the weather like in Vrindavan today?
                </div>
            </div>
        </div>
    `;
}

function useSuggestion(el) {
    const title = el.querySelector('.sg-title');
    const text = el.textContent.replace(title.textContent, '').trim();
    chatInput.value = text;
    chatInput.dispatchEvent(new Event('input'));
    sendMessage();
}


/* ═══════════════════════════════════════════════════════
   CHAT INPUT
   ═══════════════════════════════════════════════════════ */

chatInput.addEventListener('input', () => {
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 150) + 'px';
    sendBtn.disabled = !chatInput.value.trim();
});

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (chatInput.value.trim()) sendMessage();
    }
});

sendBtn.addEventListener('click', () => {
    if (chatInput.value.trim()) sendMessage();
});

clearBtn.addEventListener('click', () => {
    chatHistory = [];
    currentSessionId = null;
    showWelcome();
});


/* ═══════════════════════════════════════════════════════
   COMMAND DETECTION
   ═══════════════════════════════════════════════════════ */

function detectCommand(text) {
    const t = text.toLowerCase().trim();

    if (/^weather\b/.test(t) || t.split(' ').slice(0, 5).includes('weather')) {
        const city = t.replace(/weather/i, '').replace(/\bin\b/g, '').trim() || 'Mathura';
        return { type: 'weather', city: capitalize(city) };
    }

    const planKeywords = [
        'plan', 'itinerary', 'trip', 'travel', 'visit', 'tour', 'yatra',
        'suggest', 'recommend', 'take me', 'show me', 'pilgrimage',
        'create', 'make', 'generate', 'day', 'days', 'schedule', 'darshan'
    ];
    if (planKeywords.some(w => t.includes(w))) return { type: 'plan', query: text };

    const placeKeywords = ['mathura', 'vrindavan', 'agra', 'gokul', 'barsana', 'govardhan'];
    const themeKeywords = ['temple', 'spiritual', 'heritage', 'food', 'nature', 'shopping',
        'krishna', 'radha', 'explore', 'sacred', 'religious'];
    if ([...placeKeywords, ...themeKeywords].some(w => t.includes(w))) {
        return { type: 'plan', query: text };
    }

    return { type: 'chat', message: text };
}

function capitalize(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
}


/* ═══════════════════════════════════════════════════════
   SEND MESSAGE
   ═══════════════════════════════════════════════════════ */

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    const welcome = chatArea.querySelector('.welcome-block');
    if (welcome) welcome.remove();

    appendMessage('user', text);
    chatInput.value = '';
    chatInput.style.height = 'auto';
    sendBtn.disabled = true;

    const thinkingEl = showThinking();
    const command = detectCommand(text);

    try {
        let response;
        if (command.type === 'plan') {
            response = await callPlan(command.query);
        } else if (command.type === 'weather') {
            response = await callWeather(command.city);
        } else {
            response = await callChat(text);
        }
        removeThinking(thinkingEl);
        renderResponse(command.type, response);
    } catch (err) {
        removeThinking(thinkingEl);
        appendAIMessage(`🙏 Kshama karein (sorry) — ${err.message}. Please ensure the backend is running.`);
    }

    scrollToBottom();
}


/* ═══════════════════════════════════════════════════════
   API CALLS
   ═══════════════════════════════════════════════════════ */

async function callPlan(query) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    try {
        const res = await fetch(`${API_BASE}/plan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, weather_city: 'Mathura' }),
            signal: controller.signal,
        });
        clearTimeout(timeout);
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || `Plan failed (${res.status})`);
        }
        const data = await res.json();
        currentSessionId = data.session_id;
        return data;
    } catch (e) {
        clearTimeout(timeout);
        if (e.name === 'AbortError') throw new Error('Request timed out — AI models may still be loading. Try again in a moment.');
        throw e;
    }
}

async function callWeather(city) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    try {
        const res = await fetch(`${API_BASE}/weather/${encodeURIComponent(city)}`, { signal: controller.signal });
        clearTimeout(timeout);
        if (!res.ok) throw new Error(`Weather failed (${res.status})`);
        return await res.json();
    } catch (e) {
        clearTimeout(timeout);
        if (e.name === 'AbortError') throw new Error('Weather request timed out.');
        throw e;
    }
}

async function callChat(message) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, history: chatHistory }),
            signal: controller.signal,
        });
        clearTimeout(timeout);
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || `Chat failed (${res.status})`);
        }
        const data = await res.json();
        chatHistory = data.history;
        return data;
    } catch (e) {
        clearTimeout(timeout);
        if (e.name === 'AbortError') throw new Error('Request timed out — AI models may still be loading. Try again in a moment.');
        throw e;
    }
}


/* ═══════════════════════════════════════════════════════
   RENDER RESPONSES
   ═══════════════════════════════════════════════════════ */

function renderResponse(type, data) {
    if (type === 'plan') renderPlanResponse(data);
    else if (type === 'weather') renderWeatherResponse(data);
    else appendAIMessage(data.response || 'Hari Om 🙏 No response received.');
}

function renderPlanResponse(data) {
    let html = '';
    if (data.explanation) {
        html += `<div class="explanation-card">
            <div class="label">🙏 About Your Yatra</div>
            ${escapeHtml(data.explanation)}
        </div>`;
    }
    if (data.itinerary) html += renderItinerary(data.itinerary);
    if (data.weather) html += renderWeatherCard(data.weather);
    if (data.budget) html += renderBudgetCard(data.budget);

    if (!html) html = '🙏 Your yatra has been planned! Check the details above.';
    appendAIMessage(html, true);
}

function renderItinerary(itinerary) {
    let days = '';
    for (const [day, activities] of Object.entries(itinerary)) {
        let items = '';
        for (const act of activities) {
            const cat = act.category || '';
            const city = act.city || '';
            let emoji = '📍';
            if (/food|restaurant/i.test(cat)) emoji = '🍽️';
            else if (/temple|spiritual|mandir/i.test(cat)) emoji = '🛕';
            else if (/heritage|fort|monument/i.test(cat)) emoji = '🏰';
            else if (/garden|park|nature/i.test(cat)) emoji = '🌳';
            else if (/market|shop/i.test(cat)) emoji = '🛍️';
            else if (/ghat|river/i.test(cat)) emoji = '🏞️';
            else if (/hotel|stay/i.test(cat)) emoji = '🏨';

            items += `
                <div class="place-item">
                    <div class="place-time">${escapeHtml(act.start || '')} – ${escapeHtml(act.end || '')}</div>
                    <div class="place-info">
                        <div class="place-name">${emoji} ${escapeHtml(act.place || '')}</div>
                        <div class="place-meta">
                            ${cat ? `<span>${escapeHtml(cat)}</span>` : ''}
                            ${city ? `<span>${escapeHtml(city)}</span>` : ''}
                            ${act.duration_minutes ? `<span>${act.duration_minutes} min</span>` : ''}
                        </div>
                    </div>
                </div>
            `;
        }
        days += `
            <div class="day-section">
                <div class="day-label">📅 ${escapeHtml(day)}</div>
                ${items}
            </div>
        `;
    }

    return `
        <div class="itinerary-card">
            <div class="itinerary-header">
                <span>🗺️</span>
                <h3>Your Braj Yatra Itinerary</h3>
            </div>
            ${days}
        </div>
    `;
}

function renderWeatherResponse(data) {
    appendAIMessage(renderWeatherCard(data), true);
}

function renderWeatherCard(w) {
    const cond = (w.condition || '').toLowerCase();
    let emoji = '☀️';
    if (cond.includes('rain')) emoji = '🌧️';
    else if (cond.includes('cloud')) emoji = '☁️';
    else if (cond.includes('thunder')) emoji = '⛈️';
    else if (cond.includes('mist') || cond.includes('fog')) emoji = '🌫️';

    return `
        <div class="weather-card">
            <div class="weather-icon">${emoji}</div>
            <div class="weather-info">
                <h4>Weather in ${escapeHtml(w.city || '')}</h4>
                <p>
                    ${escapeHtml(capitalize(w.description || ''))}
                    · ${w.temperature || '--'}°C (feels ${w.feels_like || '--'}°C)
                    · 💧 ${w.humidity || '--'}%
                    · 💨 ${w.wind_speed || '--'} m/s
                </p>
            </div>
        </div>
    `;
}

function renderBudgetCard(b) {
    if (!b) return '';
    if (b.summary) {
        return `
            <div class="budget-card">
                <h4>💰 Budget Estimate (${escapeHtml(b.summary.budget_type || 'moderate')})</h4>
                <div class="budget-row"><span>Accommodation</span><span>₹${fmtN(b.breakdown?.accommodation?.cost_min || 0)} – ₹${fmtN(b.breakdown?.accommodation?.cost_max || 0)}</span></div>
                <div class="budget-row"><span>Food</span><span>₹${fmtN(b.breakdown?.food?.cost_total || 0)}</span></div>
                <div class="budget-row"><span>Sightseeing</span><span>₹${fmtN(b.breakdown?.sightseeing?.cost_total || 0)}</span></div>
                <div class="budget-total"><span>Estimated Total</span><span>₹${fmtN(b.summary.grand_total_min || 0)} – ₹${fmtN(b.summary.grand_total_max || 0)}</span></div>
            </div>
        `;
    }
    if (b.total_estimated) {
        return `
            <div class="budget-card">
                <h4>💰 Budget Estimate</h4>
                <div class="budget-row"><span>Entry Fees</span><span>₹${fmtN(b.entry_fees || 0)}</span></div>
                <div class="budget-total"><span>Estimated Total</span><span>₹${fmtN(b.total_estimated)}</span></div>
            </div>
        `;
    }
    return '';
}


/* ═══════════════════════════════════════════════════════
   MESSAGE RENDERING
   ═══════════════════════════════════════════════════════ */

function appendMessage(role, text) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    if (role === 'user') {
        div.innerHTML = `<div class="message-content">${escapeHtml(text)}</div>`;
    }
    chatArea.appendChild(div);
    scrollToBottom();
}

function appendAIMessage(content, isHTML = false) {
    const div = document.createElement('div');
    div.className = 'message ai';
    div.innerHTML = `
        <div class="ai-avatar">🙏</div>
        <div class="message-content">${isHTML ? content : escapeHtml(content)}</div>
    `;
    chatArea.appendChild(div);
    scrollToBottom();
}

function showThinking() {
    const div = document.createElement('div');
    div.className = 'message ai';
    div.innerHTML = `
        <div class="ai-avatar">🙏</div>
        <div class="message-content">
            <div class="thinking-indicator"><span></span><span></span><span></span></div>
        </div>
    `;
    chatArea.appendChild(div);
    scrollToBottom();
    return div;
}

function removeThinking(el) {
    if (el && el.parentNode) el.parentNode.removeChild(el);
}


/* ═══════════════════════════════════════════════════════
   UTILITIES
   ═══════════════════════════════════════════════════════ */

function escapeHtml(str) {
    if (!str) return '';
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
}

function fmtN(n) {
    return Number(n).toLocaleString('en-IN');
}

function scrollToBottom() {
    requestAnimationFrame(() => {
        chatArea.scrollTop = chatArea.scrollHeight;
    });
}


/* ═══════════════════════════════════════════════════════
   INITIALIZE
   ═══════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    particleSystem = new SacredParticleSystem(canvas);
});
