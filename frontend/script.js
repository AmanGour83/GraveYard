// frontend/script.js

const API_URL = "http://localhost:8000";

// Navigation Logic
function nav(sectionId) {
    document.querySelectorAll('.section').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    
    document.getElementById(sectionId).classList.add('active');
    
    const btn = document.getElementById(`btn-${sectionId}`);
    if(btn) btn.classList.add('active');

    // Reload data if going to showcase
    if(sectionId === 'showcase') fetchProjects();
}

// Fetch Projects from Backend
async function fetchProjects() {
    const grid = document.getElementById('project-grid');
    grid.innerHTML = '<p style="color: var(--text-muted)">Unearthing graves...</p>';
    
    try {
        const res = await fetch(`${API_URL}/projects/`);
        const projects = await res.json();
        
        if(projects.length === 0) {
            grid.innerHTML = '<p style="color: var(--text-muted)">No graves found.</p>';
            return;
        }

        grid.innerHTML = projects.map(p => `
            <div class="card" onclick="viewProject(${p.id})">
                <div class="card-img-placeholder">
                    ${p.docker_image}
                </div>
                <div class="card-meta">
                    <div class="avatar"></div>
                    <span>Unknown Student</span>
                </div>
                <div class="card-body">
                    <h3>${p.name}</h3>
                    <p>${p.description || "No epitaph written."}</p>
                </div>
            </div>
        `).join('');
    } catch(e) {
        console.error(e);
        grid.innerHTML = '<p style="color: var(--danger)">Error connecting to the Afterlife (Backend).</p>';
    }
}

// View Single Project Details
async function viewProject(id) {
    nav('details');
    const content = document.getElementById('detail-content');
    content.innerHTML = '<p style="color: var(--text-muted)">Summoning spirit...</p>';

    try {
        const res = await fetch(`${API_URL}/projects/${id}`);
        const p = await res.json();

        content.innerHTML = `
            <div class="hero-box">
                <div style="display:flex; justify-content:space-between; align-items: flex-start;">
                    <h1>${p.name}</h1>
                    <span style="background:var(--accent-green); color:white; padding:5px 10px; border-radius:4px;">${p.docker_image}</span>
                </div>
                <p style="font-size:1.1rem; color: var(--text-muted); margin: 20px 0;">${p.description || "No description provided."}</p>
                
                <div style="background:black; padding:20px; border-radius:8px; text-align:center; border:1px dashed var(--border);">
                    <h3 style="color:white;">Resurrection Chamber</h3>
                    <p style="color: var(--text-muted); margin-bottom: 15px;">Spin up a container to bring this project back to life.</p>
                    <div id="demo-area">
                        <button onclick="launchDemo(${p.id})" class="btn">⚡ Resurrect (Launch Demo)</button>
                    </div>
                </div>
            </div>
        `;
    } catch(e) { 
        content.innerHTML = "<p style='color: var(--danger)'>Error fetching details.</p>"; 
    }
}

// Launch Docker Container
async function launchDemo(id) {
    const area = document.getElementById('demo-area');
    area.innerHTML = '<span style="color:var(--accent-green)">Performing rituals... (Spinning up Docker)</span>';
    
    try {
        const res = await fetch(`${API_URL}/projects/${id}/launch`, { method: 'POST' });
        
        if (!res.ok) throw new Error("Launch failed");
        
        const data = await res.json();
        area.innerHTML = `
            <p style="color: var(--text-muted); margin-bottom: 10px;">It is alive!</p>
            <a href="${data.url}" target="_blank" class="btn">✨ Open Demo</a>
            <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 10px;">Expires in ${data.expires_in}</p>
        `;
    } catch(e) {
        area.innerHTML = `<span style="color: var(--danger)">Resurrection failed. Is Docker running?</span> <br><br> <button onclick="launchDemo(${id})" class="btn">Retry</button>`;
    }
}

// Submit New Project
async function submitProject() {
    const status = document.getElementById('upload-status');
    const btn = document.querySelector('#upload .btn');
    
    status.innerText = "Digging...";
    btn.disabled = true;
    
    const data = {
        name: document.getElementById('p-name').value,
        description: document.getElementById('p-desc').value,
        docker_image: document.getElementById('p-image').value,
        internal_port: parseInt(document.getElementById('p-port').value)
    };

    try {
        const res = await fetch(`${API_URL}/projects/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if(res.ok) {
            status.innerHTML = '<span style="color:var(--accent-green)">Grave Dug Successfully.</span>';
            // Clear inputs
            document.getElementById('p-name').value = '';
            document.getElementById('p-desc').value = '';
            document.getElementById('p-image').value = '';
        } else {
            const err = await res.json();
            status.innerText = "Error: " + (err.detail[0]?.msg || "Validation Failed");
        }
    } catch(e) { 
        status.innerText = "Connection Error."; 
    } finally {
        btn.disabled = false;
    }
}