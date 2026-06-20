import React, { useState, useEffect } from 'react';
import KPISummary from './components/KPISummary';
import PredictionPanel from './components/PredictionPanel';
import RevenueChart from './components/RevenueChart';
import { getAnalyticsSummary, getProducts } from './api/client';
import { Settings } from 'lucide-react';

function App() {
  const [summary, setSummary] = useState(null);
  const [products, setProducts] = useState([]);
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    // Fetch initial data
    const loadDashboard = async () => {
      try {
        const [summaryRes, productsRes] = await Promise.all([
          getAnalyticsSummary(),
          getProducts()
        ]);
        setSummary(summaryRes.data);
        setProducts(productsRes.data);
      } catch (error) {
        console.error("Failed to load dashboard data:", error);
      }
    };
    
    loadDashboard();
  }, []);

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Decorative background shapes */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary-200/50 blur-[120px] -z-10"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[30%] h-[30%] rounded-full bg-purple-200/50 blur-[100px] -z-10"></div>

      {/* Top Navbar */}
      <nav className="glass-panel sticky top-0 z-50 border-b border-gray-200/50 backdrop-blur-md px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-primary-600 p-2 rounded-lg">
              <Settings className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-extrabold tracking-tight text-gray-900">
              Supply<span className="text-primary-600">Optimizer</span>
            </h1>
          </div>
          <div className="flex items-center space-x-4 text-sm font-medium text-gray-500">
            <span>Powered by FastAPI & Scikit-Learn</span>
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <KPISummary summary={summary} />
        
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-4 h-full">
            <PredictionPanel 
              products={products} 
              onPredictionResult={setPrediction} 
            />
          </div>
          <div className="lg:col-span-8 h-full">
            <RevenueChart prediction={prediction} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
