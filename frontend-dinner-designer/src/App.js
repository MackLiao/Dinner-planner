import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import SignInSide from './pages/SignInSide';
import SignUp from './pages/SignUp';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

function App() {
  const isAuthenticated = () => {
    return sessionStorage.getItem('token') !== null; // check if user is authenticated
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={isAuthenticated() ? <Dashboard /> : <Navigate replace to="/auth/login" />} />
        <Route path="/auth/login" element={<SignInSide />} />
        <Route path="/auth/register" element={<SignUp />} />
      </Routes>
    </Router>
  );
}

export default App;