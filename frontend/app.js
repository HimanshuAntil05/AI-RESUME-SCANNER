const API = 'http://127.0.0.1:5000/api';
let dnaChart = null, tmChart = null;

// ── Tab switching ──────────────────────────────────────────────
function showTab(name) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  event.currentTarget.classList.add('active');
}

// ── File label updates ─────────────────────────────────────────
document.getElementById('file-battle-a').addEventListener('change', e => {
  document.getElementById('name-a').textContent = e.target.files[0]?.name || 'No file chosen';
});
document.getElementById('file-battle-b').addEventListener('change', e => {
  document.getElementById('name-b').textContent = e.target.files[0]?.name || 'No file chosen';
});

// ── Drag & drop ────────────────────────────────────────────────
['drop-analyze', 'drop-tm'].forEach(id => {
  const el = document.getElementById(id);
  el.addEventListener('dragover', e => { e.preventDefault(); el.classList.add('dragover'); });
  el.addEventListener('dragleave', () => el.classList.remove('dragover'));
  el.addEventListener('drop', e => {
    e.preventDefault(); el.classList.remove('dragover');
    const input = el.querySelector('input[type=file]');
    if (e.dataTransfer.files[0]) {
      const dt = new DataTransfer();
      dt.items.add(e.dataTransfer.files[0]);
      input.files = dt.files;
    }
  });
});

// ── ANALYZE ────────────────────────────────────────────────────
async function analyzeResume() {
  const file = document.getElementById('file-analyze').files[0];
  if (!file) return alert('Please select a resume file first.');

  show('analyze-loader'); hide('analyze-results');
  clearError('analyze');

  const fd = new FormData();
  fd.append('resume', file);

  try {
    const data = await post(`${API}/analyze`, fd);
    renderAnalyze(data);
    hide('analyze-loader'); show('analyze-results');
  } catch (e) {
    hide('analyze-loader');
    showError('analyze', e.message);
  }
}

function renderAnalyze(d) {
  renderContact(d.contact);
  renderDNA(d.dna);
  renderCredibility(d.credibility);
  renderSkills(d.skills);
  renderJobFit(d.job_fit);
  renderLiveJobs(d.live_jobs);
}

function renderContact(c) {
  const el = document.getElementById('contact-info');
  const items = [
    c.email    && `📧 ${c.email}`,
    c.phone    && `📞 ${c.phone}`,
    c.linkedin && `🔗 ${c.linkedin}`,
    c.github   && `🐙 ${c.github}`,
  ].filter(Boolean);
  el.innerHTML = items.length
    ? items.map(i => `<div class="contact-item">${i}</div>`).join('')
    : '<p style="color:var(--muted)">No contact info detected</p>';
}

function renderDNA(dna) {
  if (!dna || !dna.radar) return;
  const labels = Object.keys(dna.radar);
  const values = Object.values(dna.radar);

  if (dnaChart) dnaChart.destroy();
  dnaChart = new Chart(document.getElementById('dna-radar'), {
    type: 'radar',
    data: {
      labels,
      datasets: [{
        label: 'DNA Profile',
        data: values,
        backgroundColor: 'rgba(108,99,255,.25)',
        borderColor: '#6c63ff',
        pointBackgroundColor: '#00d4aa',
        pointRadius: 4,
      }]
    },
    options: {
      scales: { r: { min: 0, max: 100, ticks: { display: false }, grid: { color: '#2a2f4a' }, pointLabels: { color: '#e8eaf6', font: { size: 11 } } } },
      plugins: { legend: { display: false } },
    }
  });

  document.getElementById('dna-meta').innerHTML = `
    <div class="dna-personality">${dna.personality_type || ''}</div>
    ${[
      ['Total Words',       dna.total_words],
      ['Unique Word Ratio', dna.unique_word_ratio + '%'],
      ['Avg Sentence Len',  dna.avg_sentence_length + ' words'],
      ['Buzzword Density',  dna.buzzword_density + '%'],
    ].map(([k,v]) => `<div class="dna-stat"><span>${k}</span><span>${v}</span></div>`).join('')}
  `;
}

function renderCredibility(c) {
  const score = c.credibility_score;
  const color = score >= 85 ? 'var(--accent2)' : score >= 65 ? 'var(--warn)' : 'var(--danger)';
  document.getElementById('cred-ring').style.borderColor = color;
  document.getElementById('cred-ring').style.color = color;
  document.getElementById('cred-ring').textContent = score;
  document.getElementById('cred-verdict').innerHTML = `<p style="font-size:1.05rem;font-weight:600">${c.verdict}</p><p style="color:var(--muted);margin-top:.4rem">${c.total_flags} flag(s) detected</p>`;

  document.getElementById('cred-flags').innerHTML = (c.flags || []).map(f => `
    <div class="flag-item ${f.severity}">
      <div class="flag-type">${severityIcon(f.severity)} ${f.type}</div>
      <div>${f.detail}</div>
    </div>`).join('') || '<p style="color:var(--accent2)">✅ No flags detected</p>';
}

function severityIcon(s) { return s === 'high' ? '🚨' : s === 'medium' ? '⚠️' : 'ℹ️'; }

function renderSkills(s) {
  const cats = s.by_category || {};
  const el = document.getElementById('skills-grid');
  if (!Object.keys(cats).length) { el.innerHTML = '<p style="color:var(--muted)">No skills detected</p>'; return; }
  el.innerHTML = `<div class="skills-grid">${
    Object.entries(cats).map(([cat, skills]) => `
      <div class="skill-category">
        <h4>${cat}</h4>
        ${skills.map(sk => `<span class="skill-tag">${sk}</span>`).join('')}
      </div>`).join('')
  }</div>`;
}

function renderJobFit(fits) {
  document.getElementById('job-fit-list').innerHTML = (fits || []).slice(0, 6).map(f => `
    <div class="fit-item">
      <div class="fit-header"><span>${f.role}</span><span>${f.score}%</span></div>
      <div class="fit-bar-bg"><div class="fit-bar" style="width:${f.score}%"></div></div>
      <div class="fit-verdict">${f.verdict}</div>
      ${f.missing.length ? `<div class="fit-missing">Missing: ${f.missing.join(', ')}</div>` : ''}
    </div>`).join('');
}

function renderLiveJobs(jobs) {
  document.getElementById('live-jobs').innerHTML = (jobs || []).map(j => `
    <div class="job-card">
      <div>
        <div class="job-title">${j.title}</div>
        <div class="job-meta">🏢 ${j.company} &nbsp;·&nbsp; 📍 ${j.location}</div>
      </div>
      <a href="${j.url}" target="_blank" class="job-link">Apply →</a>
    </div>`).join('') || '<p style="color:var(--muted)">No live jobs found</p>';
}

// ── BATTLE ─────────────────────────────────────────────────────
async function runBattle() {
  const fa = document.getElementById('file-battle-a').files[0];
  const fb = document.getElementById('file-battle-b').files[0];
  if (!fa || !fb) return alert('Upload both resumes first.');

  show('battle-loader'); hide('battle-results');

  const fd = new FormData();
  fd.append('resume_a', fa);
  fd.append('resume_b', fb);

  try {
    const data = await post(`${API}/battle`, fd);
    renderBattle(data);
    hide('battle-loader'); show('battle-results');
  } catch (e) {
    hide('battle-loader');
    alert('Battle failed: ' + e.message);
  }
}

function renderBattle(d) {
  const winnerColor = d.winner === 'Resume A' ? 'var(--accent)' : d.winner === 'Resume B' ? 'var(--accent2)' : 'var(--warn)';
  document.getElementById('winner-banner').innerHTML =
    `<div style="color:${winnerColor}">🏆 ${d.winner} Wins!</div>
     <div style="font-size:.95rem;color:var(--muted);margin-top:.4rem">Overall: A ${d.overall.a} vs B ${d.overall.b} · Margin: ${d.margin} pts</div>`;

  document.getElementById('battle-rounds').innerHTML = Object.entries(d.rounds).map(([name, r]) => `
    <div class="round-item">
      <div class="round-name">${name}</div>
      <div class="round-bars">
        <div class="round-bar-wrap">
          <div class="round-label">A — ${r.a}</div>
          <div class="round-bar-bg"><div class="round-bar-a" style="width:${r.a}%"></div></div>
        </div>
        <div class="round-bar-wrap">
          <div class="round-label">B — ${r.b}</div>
          <div class="round-bar-bg"><div class="round-bar-b" style="width:${r.b}%"></div></div>
        </div>
        <div class="round-winner-badge" style="color:${r.winner==='A'?'var(--accent)':'var(--accent2)'}">
          ${r.winner === 'Tie' ? '🤝' : r.winner + ' wins'}
        </div>
      </div>
    </div>`).join('');

  ['a','b'].forEach(side => {
    const r = d[`resume_${side}`];
    document.getElementById(`battle-card-${side}`).innerHTML = `
      <div class="battle-card-title" style="color:${side==='a'?'var(--accent)':'var(--accent2)'}">Resume ${side.toUpperCase()}</div>
      ${[
        ['Total Skills',    r.total_skills],
        ['Personality',     r.personality],
        ['Credibility',     r.credibility + '/100'],
        ['Best Role Fit',   r.top_role],
        ['Fit Score',       r.top_fit_score + '%'],
      ].map(([k,v]) => `<div class="battle-stat"><span>${k}</span><span>${v}</span></div>`).join('')}
    `;
  });
}

// ── TIME MACHINE ───────────────────────────────────────────────
async function runTimeMachine() {
  const file = document.getElementById('file-tm').files[0];
  if (!file) return alert('Please select a resume file first.');

  show('tm-loader'); hide('tm-results');

  const fd = new FormData();
  fd.append('resume', file);

  try {
    const data = await post(`${API}/time-machine`, fd);
    renderTimeMachine(data);
    hide('tm-loader'); show('tm-results');
  } catch (e) {
    hide('tm-loader');
    alert('Time machine failed: ' + e.message);
  }
}

function renderTimeMachine(d) {
  const timeline = d.timeline || {};
  const skills = Object.keys(timeline);
  if (!skills.length) {
    document.getElementById('tm-results').innerHTML = '<p style="color:var(--muted)">No trackable skills found in resume.</p>';
    return;
  }

  const colors = ['#6c63ff','#00d4aa','#ff4d6d','#ffb347','#a78bfa','#34d399','#f472b6','#60a5fa'];
  const datasets = skills.map((sk, i) => ({
    label: sk,
    data: timeline[sk].demand,
    borderColor: colors[i % colors.length],
    backgroundColor: 'transparent',
    tension: 0.4,
    pointRadius: 4,
  }));

  if (tmChart) tmChart.destroy();
  tmChart = new Chart(document.getElementById('tm-chart'), {
    type: 'line',
    data: { labels: d.years, datasets },
    options: {
      plugins: { legend: { labels: { color: '#e8eaf6', font: { size: 11 } } } },
      scales: {
        x: { ticks: { color: '#8892b0' }, grid: { color: '#2a2f4a' } },
        y: { min: 0, max: 100, ticks: { color: '#8892b0' }, grid: { color: '#2a2f4a' } }
      }
    }
  });

  const allTrends = [...(d.rising||[]), ...(d.falling||[]), ...(d.stable||[])];
  document.getElementById('tm-trends').innerHTML = allTrends.map(t => {
    const cls = (d.rising||[]).find(r=>r.skill===t.skill) ? 'rising' : (d.falling||[]).find(r=>r.skill===t.skill) ? 'falling' : 'stable';
    return `<div class="trend-card ${cls}">
      <div class="trend-skill">${t.skill}</div>
      <div class="trend-delta">${t.delta}</div>
      <div class="trend-label">${t.trend}</div>
    </div>`;
  }).join('');
}

// ── Helpers ────────────────────────────────────────────────────
async function post(url, formData) {
  const res = await fetch(url, { method: 'POST', body: formData });
  const json = await res.json();
  if (!res.ok) throw new Error(json.error || 'Server error');
  return json;
}

function show(id) { document.getElementById(id).classList.remove('hidden'); }
function hide(id) { document.getElementById(id).classList.add('hidden'); }

function showError(prefix, msg) {
  const existing = document.getElementById(`${prefix}-error`);
  if (existing) existing.remove();
  const div = document.createElement('div');
  div.id = `${prefix}-error`;
  div.className = 'error-msg';
  div.textContent = '❌ ' + msg;
  document.getElementById(`tab-${prefix}`).querySelector('.upload-card').after(div);
}

function clearError(prefix) {
  const el = document.getElementById(`${prefix}-error`);
  if (el) el.remove();
}
