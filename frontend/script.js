const API_URL = 'http://127.0.0.1:5000';

const registerForm = document.getElementById('register-form');
const loginForm = document.getElementById('login-form');
const taskForm = document.getElementById('task-form');
const titleInput = document.getElementById('title');
const descInput = document.getElementById('description');
const taskList = document.getElementById('task-list');
const createTaskTitle = document.getElementById('create-task-title');

let taskStatuses = [];

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
  createTaskTitle.style.display = 'block';
  loadStatusesAndTasks();
}

function getAuthHeaders() {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${localStorage.getItem('token')}`
  };
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

async function loadStatusesAndTasks() {
  try {
    const res = await fetch(`${API_URL}/task-statuses`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Неуспешно зареждане на статусите.');
    taskStatuses = await res.json(); // [{key:"notStarted", value:"Not Started"}, ...]

    loadTasks();
  } catch (err) {
    alert('Грешка при зареждане на статусите: ' + err.message);
  }
}

async function loadTasks() {
  const res = await fetch(`${API_URL}/tasks`, {
    headers: getAuthHeaders()
  });

  if (!res.ok) {
    alert('Error loading tasks.');
    return;
  }

  const tasks = await res.json();
  taskList.innerHTML = '';

  tasks.forEach((task) => {
    const card = document.createElement('div');
    card.className = 'task-card';

    const title = document.createElement('h3');
    title.textContent = task.title;

    const desc = document.createElement('p');
    desc.textContent = task.description;

    const assignedTo = document.createElement('p');
    assignedTo.textContent = task.user_id
      ? `Assigned to user_id: ${task.user_id}`
      : 'Assigned to: nobody';

    // Показваме updated_on красиво
    const updatedOn = document.createElement('p');
    if (task.updated_on) {
      const date = new Date(task.updated_on);
      updatedOn.textContent = `Updated on: ${date.toLocaleString()}`;
    } else {
      updatedOn.textContent = 'Updated on: N/A';
    }

    const statusLabel = document.createElement('p');
    statusLabel.textContent = `Status:`;

    const statusSelect = document.createElement('select');

    // Създаваме опциите - value = key, text = value
    // защото бекенд-а приема key (enum name) при ъпдейт, а показваме човеко-разбираемо value
    taskStatuses.forEach((state) => {
      const option = document.createElement('option');
      option.value = state.key; // ключ (enum name)
      option.text = state.value; // човекочитаема стойност

      // Селектираме според task.status, който е стойност (пример "Not Started")
      if (task.status === state.key) {
        option.selected = true;
      }

      statusSelect.appendChild(option);
    });

    statusSelect.addEventListener('change', async () => {
      try {
        const res = await fetch(`${API_URL}/tasks/${task.id}/status`, {
          method: 'PUT',
          headers: getAuthHeaders(),
          body: JSON.stringify({ status: statusSelect.value }) // изпращаме ключа (enum name)
        });

        const result = await res.json();

        if (!res.ok) {
          alert('Грешка при промяна на статуса: ' + (result.message || 'Неизвестна грешка'));
        } else {
          loadTasks();
        }
      } catch (err) {
        alert('Грешка при изпращане на заявката: ' + err.message);
      }
    });

    const editBtn = document.createElement('button');
    editBtn.textContent = '✏️  Redact';
    editBtn.onclick = async () => {
      const newTitle = prompt('New title:', task.title);
      const newDesc = prompt('New description:', task.description);
      if (!newTitle || !newDesc) return;

      await fetch(`${API_URL}/tasks/${task.id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({ title: newTitle, description: newDesc })
      });
      loadTasks();
    };

    const assignBtn = document.createElement('button');
    assignBtn.textContent = '👤 Assign';
    assignBtn.onclick = async () => {
      const userId = prompt('Enter the user_id of the user who will receive the task:');
      if (!userId) return;

      const res = await fetch(`${API_URL}/tasks/${task.id}/assign`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({ user_id: userId })
      });

      if (res.ok) {
        loadTasks();
      } else {
        const err = await res.json();
        alert('Error: ' + (err.message || 'Unknown error'));
      }
    };

    card.appendChild(title);
    card.appendChild(desc);
    card.appendChild(assignedTo);
    card.appendChild(updatedOn);
    card.appendChild(statusLabel);
    card.appendChild(statusSelect);
    card.appendChild(editBtn);
    card.appendChild(assignBtn);

    taskList.appendChild(card);
  });
}
