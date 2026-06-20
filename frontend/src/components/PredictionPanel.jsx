import React, { useState } from 'react';
import { predictDemand } from '../api/client';
import { TrendingUp, Calendar, Tag, Search } from 'lucide-react';

const PredictionPanel = ({ products, onPredictionResult }) => {
  const [formData, setFormData] = useState({
    stock_code: '',
    unit_price: '',
    target_date: new Date().toISOString().split('T')[0]
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.stock_code || !formData.unit_price) return;
    
    setLoading(true);
    try {
      const response = await predictDemand({
        stock_code: formData.stock_code,
        unit_price: parseFloat(formData.unit_price),
        target_date: new Date(formData.target_date).toISOString()
      });
      onPredictionResult(response.data);
    } catch (error) {
      console.error("Prediction failed:", error);
      alert("Failed to fetch prediction.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel p-6 rounded-2xl h-full shadow-sm">
      <div className="flex items-center mb-6">
        <TrendingUp className="text-primary-600 mr-2" />
        <h2 className="text-xl font-bold">Dynamic Pricing Simulator</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Select Product</label>
          <div className="relative">
            <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <select
              required
              className="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all outline-none"
              value={formData.stock_code}
              onChange={e => setFormData({...formData, stock_code: e.target.value})}
            >
              <option value="">Search historical products...</option>
              {products.map(p => (
                <option key={p.StockCode} value={p.StockCode}>
                  {p.StockCode} - {p.Description} (${p.UnitPrice})
                </option>
              ))}
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Proposed Unit Price ($)</label>
          <div className="relative">
            <Tag className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <input
              type="number"
              step="0.01"
              min="0.01"
              required
              className="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all outline-none"
              placeholder="e.g. 2.99"
              value={formData.unit_price}
              onChange={e => setFormData({...formData, unit_price: e.target.value})}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Target Date</label>
          <div className="relative">
            <Calendar className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <input
              type="date"
              required
              className="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all outline-none"
              value={formData.target_date}
              onChange={e => setFormData({...formData, target_date: e.target.value})}
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full mt-4 bg-primary-600 hover:bg-primary-700 text-white font-bold py-3 px-4 rounded-xl transition-colors disabled:opacity-50"
        >
          {loading ? "Simulating..." : "Run ML Simulation"}
        </button>
      </form>
    </div>
  );
};

export default PredictionPanel;
