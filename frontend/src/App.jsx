import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

// Main App Controller wrapper jo state listen karega
const NavigationController = () => {
  const { user, logout } = useAuth();
  const [currentScreen, setCurrentScreen] = useState('dashboard'); // screens: dashboard, login, register

  // Unauthenticated users sirf login ya register dekh sakte hain
  if (!user) {
    if (currentScreen === 'register') {
      return <Register navigateToLogin={() => setCurrentScreen('login')} />;
    }
    return <Login navigateToRegister={() => setCurrentScreen('register')} />;
  }

  // Authenticated state: Show Dashboard layout
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 font-sans">
      {/* Dynamic Navbar */}
      <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex justify-between items-center shadow-md">
        <div className="flex items-center space-x-3">
          <span className="text-2xl font-black tracking-wider text-blue-500">DRIVE<span className="text-white">X</span></span>
          <span className="text-xs px-2 py-0.5 rounded bg-gray-800 text-gray-400 border border-gray-700">
            {user.isAdmin ? '👑 Admin Panel' : '👤 Customer'}
          </span>
        </div>
        <div className="flex items-center space-x-6">
          <span className="text-sm text-gray-400">Welcome, <strong className="text-gray-200">{user.username}</strong></span>
          <button 
            onClick={logout} 
            className="bg-red-900/40 hover:bg-red-600 text-red-200 hover:text-white text-xs font-semibold px-4 py-2 rounded-lg border border-red-800/60 transition-all duration-200"
          >
            Sign Out
          </button>
        </div>
      </nav>

      {/* Main Container View */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <Dashboard />
      </main>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <NavigationController />
    </AuthProvider>
  );
}

export default App;