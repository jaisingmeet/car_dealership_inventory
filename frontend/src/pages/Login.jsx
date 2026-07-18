import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function Login({ navigateToRegister }) {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(username, password);
    setLoading(false);
    
    if (!result.success) {
      setError(result.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950 px-4">
      <div className="bg-gray-900 p-8 rounded-2xl w-full max-w-md shadow-2xl border border-gray-800">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-black text-white tracking-tight">Welcome Back</h2>
          <p className="text-sm text-gray-400 mt-2">Sign in to explore the dealership stock</p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-900/30 border border-red-800 text-red-400 text-xs font-medium">
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Username</label>
            <input 
              type="text" 
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g., admin_meet or guest_user"
              className="w-full px-4 py-3 rounded-xl bg-gray-950 border border-gray-800 text-white placeholder-gray-600 focus:outline-none focus:border-blue-500 transition-colors"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Password</label>
            <input 
              type="password" 
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-3 rounded-xl bg-gray-950 border border-gray-800 text-white placeholder-gray-600 focus:outline-none focus:border-blue-500 transition-colors"
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm shadow-lg shadow-blue-600/20 active:scale-[0.99] transition-all disabled:opacity-50"
          >
            {loading ? 'Authenticating...' : 'Sign In'}
          </button>
        </form>

        <div className="text-center mt-6 pt-6 border-t border-gray-800/60">
          <p className="text-xs text-gray-500">
            Don't have an account?{' '}
            <button onClick={navigateToRegister} className="text-blue-400 hover:underline font-medium">
              Register here
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}