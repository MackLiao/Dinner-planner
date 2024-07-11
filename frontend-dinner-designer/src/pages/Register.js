import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate(); 

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); 
    try {
        const response = await fetch('http://127.0.0.1:5000/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
            });
        
        if (response.ok) { 
            // if registration is successful, alert user and redirect
            alert('Account created successfully!');
            navigate('/auth/login');
        } else {
            // if registration failed, show error message
            const errorData = await response.json();
            setErrorMessage(errorData.message || 'Registration failed. Please try again.');
            alert(errorMessage);
        }
    } catch (error) {
        // handle network errors
        setErrorMessage('Network error. Please try again.');
        console.error('Error:', error);
    }
    // Reset form fields
    setUsername('');
    setEmail('');
    setPassword('');
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;