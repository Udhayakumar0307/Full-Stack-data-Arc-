import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [mode, setMode] = useState('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const [users, setUsers] = useState([]);
  const [viewPage, setViewPage] = useState('home');
  const [uploadUsername, setUploadUsername] = useState('');

  useEffect(() => {
    if (loggedIn || viewPage === 'upload') {
      fetchUsers(); // Only fetch users for upload dropdown, not for users page
    }
  }, [loggedIn, viewPage]);

  const handleAuth = async () => {
    const endpoint = mode === 'register' ? 'register' : 'login';
    const body = mode === 'register'
      ? { username, password, email }
      : { username, password };

    const res = await fetch(`http://localhost:5000/${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const data = await res.json();
    setStatus(data.message || data.error);

    if (res.ok) {
      if (mode === 'login') {
        setLoggedIn(true);
        setViewPage('upload');
      } else if (mode === 'register') {
        setUsername('');
        setPassword('');
        setEmail('');
        setMode('login'); // Stay on login, no auto-fill
      }
    }
  };

  const handleUpload = async () => {
    if (!uploadUsername) return alert('Select a username to upload file');
    if (!file) return alert('Choose a file');
    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch(`http://localhost:5000/upload/${uploadUsername}`, {
      method: 'POST',
      body: formData,
    });

    const data = await res.json();
    setStatus(data.message || data.error);
  };

  const fetchUsers = async () => {
    try {
      const res = await fetch('http://localhost:5000/users');
      const data = await res.json();
      setUsers(data);
    } catch (err) {
      setStatus('Failed to load users');
      console.error('Error fetching users:', err);
    }
  };

  const handleViewUsers = async () => {
    await fetchUsers();
    setViewPage('users'); // Now safe to switch view after fetching
  };

  const deleteUser = async (userToDelete) => {
    await fetch(`http://localhost:5000/delete/${userToDelete}`, {
      method: 'DELETE',
    });
    fetchUsers(); // Refresh after deletion
  };

  return (
    <div className="container">
      {viewPage === 'users' ? (
        <>
          <h2>All Users & Projects</h2>
          <ul>
            {users.map((u, i) => (
              <li key={i}>
                <div>
                  <strong>{u.username}</strong><br />
                  <span>{u.email}</span><br />
                  {u.file && (
                    <a
                      href={`http://localhost:5000/uploads/${u.file}`}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      View File
                    </a>
                  )}
                </div>
                <button className="delete-btn" onClick={() => deleteUser(u.username)}>Delete</button>
              </li>
            ))}
          </ul>
          <button onClick={() => setViewPage('home')}>Go to Home</button>
        </>
      ) : viewPage === 'upload' ? (
        <>
          <h2>Upload a Project</h2>
          <label>Select Username:</label>
          <select value={uploadUsername} onChange={(e) => setUploadUsername(e.target.value)}>
            <option value="">-- Select User --</option>
            {users.map((u, i) => (
              <option key={i} value={u.username}>
                {u.username}
              </option>
            ))}
          </select>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button onClick={handleUpload}>Upload File</button>
          <p>{status}</p>
          <button onClick={handleViewUsers}>View All Users</button>
          <button onClick={() => setViewPage('home')}>Go Back Home</button>
        </>
      ) : (
        <>
          <h2>{mode === 'login' ? 'Login' : 'Register'}</h2>
          <input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {mode === 'register' && (
            <input
              placeholder="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          )}
          <button onClick={handleAuth}>
            {mode === 'login' ? 'Login' : 'Register'}
          </button>
          <p>{status}</p>
          <button
            className="switch-btn"
            onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
          >
            Switch to {mode === 'login' ? 'Register' : 'Login'}
          </button>
        </>
      )}
    </div>
  );
}

export default App;


