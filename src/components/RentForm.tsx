'use client';

import { useState } from 'react';

import MarketChart from './MarketChart';

const LOCATIONS = [
    'Al Nahda', 'Business Bay', 'Discovery Gardens', 'Downtown Dubai',
    'Dubai Marina', 'Dubai Silicon Oasis', 'Dubai Sports City',
    'International City', 'Jumeirah Beach Residence (JBR)',
    'Jumeirah Lake Towers (JLT)', 'Jumeirah Village Circle (JVC)',
    'Palm Jumeirah'
];

export default function RentForm() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<number | null>(null);
    const [marketData, setMarketData] = useState<any[]>([]);
    const [formData, setFormData] = useState({
        location: 'Dubai Marina',
        bedrooms: 1,
        bathrooms: 2,
        size_sqft: 800,
        furnishing: 'Furnished'
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);
        setMarketData([]);

        try {
            // In production (Vercel), this hits /api/predict
            // Locally, we might need a rewrites proxy or running the python server on a port
            const res = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            const data = await res.json();
            if (data.status === 'success') {
                setResult(data.predicted_price);
                if (data.market_data) {
                    setMarketData(data.market_data);
                }
            } else {
                alert('Error: ' + data.message);
            }
        } catch (error) {
            console.error(error);
            alert('Failed to fetch prediction.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto p-4 md:p-8 grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
            {/* Form Section */}
            <div className="bg-white/5 backdrop-blur-lg border border-white/10 p-6 md:p-8 rounded-3xl shadow-2xl">
                <h2 className="text-2xl font-bold text-white mb-6">Property Details</h2>
                <form onSubmit={handleSubmit} className="space-y-6">

                    {/* Location */}
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-gray-300">Location</label>
                        <select
                            className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                            value={formData.location}
                            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                        >
                            {LOCATIONS.map(loc => (
                                <option key={loc} value={loc} className="bg-gray-900">{loc}</option>
                            ))}
                        </select>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        {/* Bedrooms */}
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-300">Bedrooms</label>
                            <select
                                className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                                value={formData.bedrooms}
                                onChange={(e) => setFormData({ ...formData, bedrooms: parseInt(e.target.value) })}
                            >
                                {[0, 1, 2, 3, 4].map(b => (
                                    <option key={b} value={b} className="bg-gray-900">{b === 0 ? 'Studio' : b}</option>
                                ))}
                            </select>
                        </div>

                        {/* Bathrooms */}
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-300">Bathrooms</label>
                            <input
                                type="number"
                                min="1" max="6"
                                className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                                value={formData.bathrooms}
                                onChange={(e) => setFormData({ ...formData, bathrooms: parseFloat(e.target.value) })}
                            />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        {/* Size */}
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-300">Size (sq.ft)</label>
                            <input
                                type="number"
                                className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                                value={formData.size_sqft}
                                onChange={(e) => setFormData({ ...formData, size_sqft: parseFloat(e.target.value) })}
                            />
                        </div>

                        {/* Furnishing */}
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-300">Furnishing</label>
                            <select
                                className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                                value={formData.furnishing}
                                onChange={(e) => setFormData({ ...formData, furnishing: e.target.value })}
                            >
                                {['Unfurnished', 'Partly Furnished', 'Furnished'].map(f => (
                                    <option key={f} value={f} className="bg-gray-900">{f}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-white font-bold py-4 rounded-xl shadow-lg transform transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? 'Analyzing Market...' : 'Predict Fair Rent'}
                    </button>
                </form>
            </div>

            {/* Result Section */}
            <div className="space-y-6">
                <div className={`transition-all duration-500 transform ${result ? 'opacity-100 translate-y-0' : 'opacity-50 translate-y-4'}`}>
                    <div className="bg-gradient-to-br from-gray-900 to-black border border-white/10 p-8 rounded-3xl shadow-2xl relative overflow-hidden group">
                        <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl -mr-16 -mt-16 transition-all group-hover:bg-emerald-500/20"></div>

                        <h3 className="text-gray-400 text-lg font-medium mb-2">Estimated Fair Rent</h3>
                        <div className="flex items-baseline gap-2">
                            <span className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-200">
                                {result ? `AED ${result.toLocaleString()}` : '---'}
                            </span>
                            <span className="text-gray-500">/year</span>
                        </div>

                        <p className="mt-4 text-gray-400 text-sm leading-relaxed">
                            Based on AI analysis of similar properties in <strong>{formData.location}</strong>.
                        </p>
                    </div>
                </div>

                {/* Charts */}
                <div className="bg-white/5 border border-white/10 p-6 rounded-2xl">
                    {result && marketData.length > 0 ? (
                        <MarketChart
                            data={marketData}
                            predictedPrice={result}
                            location={formData.location}
                        />
                    ) : (
                        <div className="h-32 flex items-center justify-center border-2 border-dashed border-white/10 rounded-xl text-gray-500 text-sm">
                            {loading ? 'Crunching numbers...' : 'Market data will appear here'}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
