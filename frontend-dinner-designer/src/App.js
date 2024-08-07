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

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate replace to="/auth/login" />} />
        <Route path="/auth/login" element={<SignInSide />} />
        <Route path="/auth/register" element={<SignUp />} />
        <Route path="/auth/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;