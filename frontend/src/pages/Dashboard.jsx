import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';

export default function Dashboard() {
  const { user } = useAuth();
  
  // States for vehicles and filters
  const [vehicles, setVehicles] = useState([]);
  const [searchMake, setSearchMake] = useState('');
  const [searchModel, setSearchModel] = useState('');
  const [searchCategory, setSearchCategory] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [message, setMessage] = useState({ text: '', type: '' });

  // Admin form state
  const [newVehicle, setNewVehicle] = useState({
    make: '', model: '', year: new Date().getFullYear(),
    price: '', category: '', quantity: 1, status: 'available'
  });

  // Fetch all vehicles
  const fetchVehicles = async () => {
    try {
      const response = await API.get('/vehicles');
      setVehicles(response.data);
    } catch (err) {
      showMsg('Failed to fetch inventory', 'error');
    }
  };

  // Search/Filter Handler
  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const params = {};
      if (searchMake) params.make = searchMake;
      if (searchModel) params.model = searchModel;
      if (searchCategory) params.category = searchCategory;
      if (minPrice) params.min_price = parseFloat(minPrice);
      if (maxPrice) params.max_price = parseFloat(maxPrice);

      const response = await API.get('/vehicles/search', { params });
      setVehicles(response.data);
    } catch (err) {
      showMsg('Search failed', 'error');
    }
  };

  // Clear filters
  const clearFilters = () => {
    setSearchMake('');
    setSearchModel('');
    setSearchCategory('');
    setMinPrice('');
    setMaxPrice('');
    fetchVehicles();
  };

  // Customer Purchase Operation
  const handlePurchase = async (id) => {
    try {
      const response = await API.post(`/vehicles/${id}/purchase`);
      showMsg(response.data.message, 'success');
      fetchVehicles(); // Refresh list
    } catch (err) {
      showMsg(err.response?.data?.detail || 'Purchase failed', 'error');
    }
  };

  // Admin Operations: Add Vehicle
  const handleAddVehicle = async (e) => {
    e.preventDefault();
    try {
      await API.post('/vehicles', newVehicle);
      showMsg('Vehicle added successfully!', 'success');
      setNewVehicle({
        make: '', model: '', year: new Date().getFullYear(),
        price: '', category: '', quantity: 1, status: 'available'
      });
      fetchVehicles();
    } catch (err) {
      showMsg(err.response?.data?.detail || 'Failed to add vehicle', 'error');
    }
  };

  // Admin Operations: Restock
  const handleRestock = async (id) => {
    try {
      const response = await API.post(`/vehicles/${id}/restock?amount=5`);
      showMsg(response.data.message, 'success');
      fetchVehicles();
    } catch (err) {
      showMsg('Restock failed', 'error');
    }
  };

  // Admin Operations: Delete
  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this vehicle?')) return;
    try {
      const response = await API.delete(`/vehicles/${id}`);
      showMsg(response.data.message, 'success');
      fetchVehicles();
    } catch (err) {
      showMsg(err.response?.data?.detail || 'Delete failed', 'error');
    }
  };

  const showMsg = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: '', type: '' }), 4000);
  };

  useEffect(() => {
    fetchVehicles();
  }, []);

  return (
    <div className="space-y-8">
      {/* Notifications Alert Banner */}
      {message.text && (
        <div className={`p-4 rounded-xl text-sm border font-semibold ${
          message.type === 'success' 
            ? 'bg-green-900/30 border-green-800 text-green-400' 
            : 'bg-red-900/30 border-red-800 text-red-400'
        }`}>
          {message.text}
        </div>
      )}

      {/* 🛠️ ADMIN PANEL SECTION */}
      {user?.isAdmin && (
        <section className="bg-gray-900 p-6 rounded-2xl border border-blue-900/40 shadow-xl">
          <h2 className="text-xl font-bold text-blue-400 mb-4 flex items-center gap-2">
            <span>👑</span> Fleet Manager (Admin Console)
          </h2>
          <form onSubmit={handleAddVehicle} className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <input 
              type="text" placeholder="Make (e.g., Tesla)" required
              value={newVehicle.make} onChange={e => setNewVehicle({...newVehicle, make: e.target.value})}
              className="px-3 py-2 rounded-lg bg-gray-950 border border-gray-800 text-sm focus:outline-none focus:border-blue-500"
            />
            <input 
              type="text" placeholder="Model (e.g., Model S)" required
              value={newVehicle.model} onChange={e => setNewVehicle({...newVehicle, model: e.target.value})}
              className="px-3 py-2 rounded-lg bg-gray-950 border border-gray-800 text-sm focus:outline-none focus:border-blue-500"
            />
            <input 
              type="number" placeholder="Year" required
              value={newVehicle.year} onChange={e => setNewVehicle({...newVehicle, year: parseInt(e.target.value) || 2026})}
              className="px-3 py-2 rounded-lg bg-gray-950 border border-gray-800 text-sm focus:outline-none focus:border-blue-500"
            />
            <input 
              type="text" placeholder="Category (e.g., Sedan, SUV)" required
              value={newVehicle.category} onChange={e => setNewVehicle({...newVehicle, category: e.target.value})}
              className="px-3 py-2 rounded-lg bg-gray-950 border border-gray-800 text-sm focus:outline-none focus:border-blue-500"
            />
            <input 
              type="number" step="any" placeholder="Price ($)" required
              value={newVehicle.price} onChange={e => setNewVehicle({...newVehicle, price: parseFloat(e.target.value) || ''})}
              className="px-3 py-2 rounded-lg bg-gray-950 border border-gray-800 text-sm focus:outline-none focus:border-blue-500"
            />
            <input 
              type="number" placeholder="Stock Quantity" required
              value={newVehicle.quantity} onChange={e => setNewVehicle({...newVehicle, quantity: parseInt(e.target.value) || 0})}
              className="px-3 py-2 rounded-lg bg-gray-950 border border-gray-800 text-sm focus:outline-none focus:border-blue-500"
            />
            <button type="submit" className="col-span-2 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg text-sm transition-colors py-2">
              + Add Vehicle to Showroom
            </button>
          </form>
        </section>
      )}

      {/* 🔍 SEARCH AND FILTERS ENGINE */}
      <section className="bg-gray-900 p-6 rounded-2xl border border-gray-800 shadow-md">
        <h3 className="text-lg font-bold text-white mb-4">Search Catalog</h3>
        <form onSubmit={handleSearch} className="grid grid-cols-2 md:grid-cols-5 gap-3">
          <input 
            type="text" placeholder="Filter Make" 
            value={searchMake} onChange={e => setSearchMake(e.target.value)}
            className="px-3 py-2 rounded-lg bg-gray-950 border border-gray-800 text-xs focus:outline-none text-white"
          />
          <input 
            type="text" placeholder="Filter Model" 
            value={searchModel} onChange={e => setSearchModel(e.target.value)}
            className="px-3 py-2 rounded-lg bg-gray-950 border border-gray-800 text-xs focus:outline-none text-white"
          />
          <input 
            type="text" placeholder="Filter Category" 
            value={searchCategory} onChange={e => setSearchCategory(e.target.value)}
            className="px-3 py-2 rounded-lg bg-gray-950 border border-gray-800 text-xs focus:outline-none text-white"
          />
          <input 
            type="number" placeholder="Min Price" 
            value={minPrice} onChange={e => setMinPrice(e.target.value)}
            className="px-3 py-2 rounded-lg bg-gray-950 border border-gray-800 text-xs focus:outline-none text-white"
          />
          <input 
            type="number" placeholder="Max Price" 
            value={maxPrice} onChange={e => setMaxPrice(e.target.value)}
            className="px-3 py-2 rounded-lg bg-gray-950 border border-gray-800 text-xs focus:outline-none text-white"
          />
          <div className="col-span-2 md:col-span-5 flex justify-end space-x-3 mt-2">
            <button type="button" onClick={clearFilters} className="px-4 py-2 text-xs bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700">
              Clear All
            </button>
            <button type="submit" className="px-6 py-2 text-xs bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-500 shadow-md">
              Apply Filters
            </button>
          </div>
        </form>
      </section>

      {/* 🚘 SHOWROOM VEHICLE GRID LIST */}
      <section>
        <h3 className="text-xl font-extrabold tracking-tight mb-6">Current Inventory Available ({vehicles.length})</h3>
        {vehicles.length === 0 ? (
          <div className="text-center py-12 bg-gray-900 rounded-2xl border border-gray-800 text-gray-500 text-sm">
            No vehicles found matching criteria or showroom is empty.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {vehicles.map((car) => (
              <div key={car.id} className="bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden p-5 flex flex-col justify-between shadow-lg hover:border-gray-700 transition-all">
                <div>
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-xs font-bold uppercase tracking-wider text-blue-500 bg-blue-950/60 px-2.5 py-1 rounded-md border border-blue-900/30">
                      {car.category}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded font-medium border ${
                      car.quantity > 0 
                        ? 'bg-green-950/40 text-green-400 border-green-900/40' 
                        : 'bg-red-950/40 text-red-400 border-red-900/40'
                    }`}>
                      {car.quantity > 0 ? `${car.quantity} In Stock` : 'Out of Stock'}
                    </span>
                  </div>
                  <h4 className="text-lg font-black text-white mt-1">{car.make} <span className="font-normal text-gray-400">{car.model}</span></h4>
                  <p className="text-xs text-gray-500 mt-0.5">Manufacture Year: {car.year}</p>
                  <p className="text-2xl font-black text-white mt-4">${car.price.toLocaleString()}</p>
                </div>

                <div className="mt-6 pt-4 border-t border-gray-800/60 space-y-2">
                  {/* Customer Purchase Action */}
                  <button
                    onClick={() => handlePurchase(car.id)}
                    disabled={car.quantity <= 0}
                    className="w-full py-2.5 text-xs font-bold text-center rounded-xl bg-gray-100 text-gray-950 hover:bg-white disabled:bg-gray-800 disabled:text-gray-600 active:scale-[0.99] transition-all"
                  >
                    {car.quantity > 0 ? '⚡ Purchase Vehicle' : 'Sold Out'}
                  </button>

                  {/* Admin Controls Layout */}
                  {user?.isAdmin && (
                    <div className="grid grid-cols-2 gap-2 pt-1">
                      <button 
                        onClick={() => handleRestock(car.id)}
                        className="py-1.5 text-[11px] font-semibold bg-gray-800 hover:bg-gray-700 text-blue-400 rounded-lg border border-gray-700/60"
                      >
                        + Restock (5)
                      </button>
                      <button 
                        onClick={() => handleDelete(car.id)}
                        className="py-1.5 text-[11px] font-semibold bg-red-900/20 hover:bg-red-600 text-red-400 hover:text-white rounded-lg border border-red-900/40"
                      >
                        🗑️ Delete Fleet
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}