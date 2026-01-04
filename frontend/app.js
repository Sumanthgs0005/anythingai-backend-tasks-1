const API_BASE = "http://127.0.0.1:8000";
let accessToken = null;

function setStatus(message, isError = false) {
  const el = document.getElementById("status");
  el.textContent = message;
  el.className = isError ? "error" : "";
}

function updateTokenPreview() {
  const el = document.getElementById("token-preview");
  if (!accessToken) {
    el.textContent = "Not logged in";
  } else {
    el.textContent = accessToken.substring(0, 20) + "...";
  }
}

async function register() {
  const email = document.getElementById("reg-email").value;
  const password = document.getElementById("reg-password").value;
  const is_admin = document.getElementById("reg-admin").checked;

  setStatus("Registering user...");

  const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, is_admin }),
  });

  const data = await res.json();
  if (res.ok) {
    setStatus("Registration successful. You can now login.");
  } else {
    setStatus("Registration failed: " + (data.detail || JSON.stringify(data)), true);
  }
}

async function login() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  setStatus("Logging in...");

  const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();
  if (res.ok) {
    accessToken = data.access_token;
    updateTokenPreview();
    setStatus("Login successful. Token stored in memory.");
  } else {
    setStatus("Login failed: " + (data.detail || JSON.stringify(data)), true);
  }
}

async function createTask() {
  if (!accessToken) {
    setStatus("Please login first to create tasks.", true);
    return;
  }

  const title = document.getElementById("task-title").value;
  const description = document.getElementById("task-desc").value;

  setStatus("Creating task...");

  const res = await fetch(`${API_BASE}/api/v1/tasks/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + accessToken,
    },
    body: JSON.stringify({ title, description }),
  });

  const data = await res.json();
  if (res.ok) {
    setStatus("Task created successfully.");
    await loadMyTasks();
  } else {
    setStatus("Failed to create task: " + (data.detail || JSON.stringify(data)), true);
  }
}

async function loadMyTasks() {
  if (!accessToken) {
    setStatus("Please login first to view tasks.", true);
    return;
  }

  setStatus("Loading your tasks...");

  const res = await fetch(`${API_BASE}/api/v1/tasks/`, {
    headers: {
      Authorization: "Bearer " + accessToken,
    },
  });

  const data = await res.json();
  if (res.ok) {
    document.getElementById("tasks-output").innerText = JSON.stringify(data, null, 2);
    setStatus("Loaded your tasks.");
  } else {
    setStatus("Failed to load tasks: " + (data.detail || JSON.stringify(data)), true);
  }
}

async function loadAllTasks() {
  if (!accessToken) {
    setStatus("Login as admin to view all tasks.", true);
    return;
  }

  setStatus("Loading all tasks (admin)...");

  const res = await fetch(`${API_BASE}/api/v1/tasks/all`, {
    headers: {
      Authorization: "Bearer " + accessToken,
    },
  });

  const data = await res.json();
  if (res.ok) {
    document.getElementById("all-tasks-output").innerText = JSON.stringify(
      data,
      null,
      2
    );
    setStatus("Loaded all tasks (admin).");
  } else {
    setStatus("Failed to load all tasks: " + (data.detail || JSON.stringify(data)), true);
  }
}
