import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Cell } from 'recharts';
import { BarChart3 } from 'lucide-react';

const RevenueChart = ({ prediction }) => {
  if (!prediction) {
    return (
      <div className="glass-panel p-6 rounded-2xl h-full shadow-sm flex flex-col items-center justify-center text-gray-400 min-h-[400px]">
        <BarChart3 className="w-16 h-16 mb-4 opacity-50" />
        <p>Run a simulation to see the projected demand & revenue.</p>
      </div>
    );
  }

  // Create visualization data from prediction response
  const data = [
    {
      name: 'Projected Demand',
      value: prediction.predicted_quantity,
      color: '#0ea5e9', // primary-500
      unit: ' units'
    },
    {
      name: 'Projected Revenue',
      value: prediction.predicted_revenue,
      color: '#10b981', // green-500
      unit: '$'
    }
  ];

  return (
    <div className="glass-panel p-6 rounded-2xl h-full shadow-sm flex flex-col min-h-[400px]">
      <div className="flex items-center mb-6">
        <BarChart3 className="text-primary-600 mr-2" />
        <h2 className="text-xl font-bold">Simulation Results: {prediction.stock_code}</h2>
      </div>
      
      <div className="flex-grow">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
            <XAxis dataKey="name" tick={{fill: '#4b5563', fontWeight: 500}} axisLine={false} tickLine={false} />
            <YAxis tick={{fill: '#4b5563'}} axisLine={false} tickLine={false} />
            <Tooltip 
              cursor={{fill: '#f3f4f6'}}
              contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }}
              formatter={(value, name, props) => {
                const isRevenue = props.payload.unit === '$';
                return [isRevenue ? `$${value.toLocaleString()}` : `${value.toLocaleString()} units`, ''];
              }}
            />
            <Bar dataKey="value" radius={[6, 6, 0, 0]} maxBarSize={100}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 p-4 bg-primary-50 rounded-xl text-primary-900 border border-primary-100">
        <p className="text-sm font-medium">
          <strong>Summary:</strong> Setting the price to <strong>${prediction.unit_price}</strong> on <strong>{new Date(prediction.target_date).toLocaleDateString()}</strong> is expected to generate <strong>{prediction.predicted_quantity.toLocaleString()} units</strong> in volume, resulting in a projected daily revenue of <strong>${prediction.predicted_revenue.toLocaleString()}</strong>.
        </p>
      </div>
    </div>
  );
};

export default RevenueChart;
