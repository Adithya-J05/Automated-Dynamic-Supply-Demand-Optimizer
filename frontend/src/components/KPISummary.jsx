import React from 'react';
import { Activity, Package, DollarSign } from 'lucide-react';

const KPISummary = ({ summary }) => {
  if (!summary) return <div className="animate-pulse h-32 bg-gray-200 rounded-xl"></div>;

  const cards = [
    { title: "Total Revenue", value: `$${summary.total_revenue.toLocaleString()}`, icon: DollarSign, color: "text-green-600", bg: "bg-green-100" },
    { title: "Total Transactions", value: summary.total_transactions.toLocaleString(), icon: Activity, color: "text-primary-600", bg: "bg-primary-100" },
    { title: "Unique Products", value: summary.total_unique_products.toLocaleString(), icon: Package, color: "text-purple-600", bg: "bg-purple-100" },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {cards.map((card, idx) => (
        <div key={idx} className="glass-panel p-6 rounded-2xl hover-lift flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500 mb-1">{card.title}</p>
            <h3 className="text-3xl font-bold text-gray-900">{card.value}</h3>
          </div>
          <div className={`p-4 rounded-full ${card.bg}`}>
            <card.icon className={`w-8 h-8 ${card.color}`} />
          </div>
        </div>
      ))}
    </div>
  );
};

export default KPISummary;
