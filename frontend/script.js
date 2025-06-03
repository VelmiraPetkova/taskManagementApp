const API_URL = 'http://127.0.0.1:5000';

const registerForm = document.getElementById('register-form');
const loginForm = document.getElementById('login-form');


registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('reg-name').value;
  const email = document.getElementById('reg-email').value;
  const password = document.getElementById('reg-password').value;

  try {
    const res = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    });

    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('token', data.token);
      afterLogin();
    } else {
      alert('Registration error: ' + (data.message || 'Invalid data.'));
    }
  } catch (err) {
    alert('Request error:' + err.message);
  }
});

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  try {
    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('token', data.token);
      afterLogin();
    } else {
      alert('Login error: ' + (data.message || 'Invalid data.'));
    }
  } catch (err) {
    alert('Request error: ' + err.message);
  }
});

function afterLogin() {
  registerForm.style.display = 'none';
  loginForm.style.display = 'none';
  taskForm.style.display = 'block';
  loadTasks();
}

//add token
function getAuthHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  };
}

// TO DO:
async function loadTasks() {
  const res = await fetch(`${API_URL}/tasks`, {
    headers: getAuthHeaders()
  });
  const tasks = await res.json();
  taskList.innerHTML = '';
  tasks.forEach(task => {
    const li = document.createElement('li');
    li.innerHTML = `
      <strong>${task.title}</strong>: ${task.description} (${task.status})
      <button onclick="updateTask(${task.id})">✏️</button>
      <button onclick="deleteTask(${task.id})">🗑️</button>
    `;
    taskList.appendChild(li);
  });
}


taskForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  await fetch(`${API_URL}/tasks`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({
      title: titleInput.value,
      description: descInput.value
    })
  });
  titleInput.value = '';
  descInput.value = '';
  loadTasks();
});


async function deleteTask(id) {
  await fetch(`${API_URL}/tasks/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  });
  loadTasks();
}


async function updateTask(id) {
  const newTitle = prompt("Ново заглавие:");
  const newDescription = prompt("Ново описание:");
  const newStatus = prompt("Нов статус: OPEN, IN_PROGRESS, DONE");
  if (!newTitle || !newStatus) return;

  await fetch(`${API_URL}/tasks/${id}`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify({
      title: newTitle,
      description: newDescription,
      status: newStatus
    })
  });
  loadTasks();
}
