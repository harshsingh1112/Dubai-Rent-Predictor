'use client';

import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    ReferenceLine,
    Cell
} from 'recharts';

interface MarketData {
    range_start: number;
    range_end: number;
    count: number;
    label: string;
}

interface MarketChartProps {
    data: MarketData[];
    predictedPrice: number;
    location: string;
}

export default function MarketChart({ data, predictedPrice, location }: MarketChartProps) {
    return (
        <div className="w-full h-64 mt-6">
            <h4 className="text-white font-medium mb-4">Market Distribution in {location}</h4>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart
                    data={data}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                    <XAxis
                        dataKey="label"
                        stroke="#666"
                        tick={{ fontSize: 12 }}
                        tickLine={false}
                        axisLine={false}
                    />
                    <YAxis
                        stroke="#666"
                        tick={{ fontSize: 12 }}
                        tickLine={false}
                        axisLine={false}
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#111', border: '1px solid #333' }}
                        itemStyle={{ color: '#fff' }}
                        cursor={{ fill: 'rgba(255, 255, 255, 0.1)' }}
                    />
                    <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                        {data.map((entry, index) => {
                            // Highlight the bar that contains the predicted price
                            const isTarget = predictedPrice >= entry.range_start && predictedPrice < entry.range_end;
                            return (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={isTarget ? '#10B981' : '#3B82F6'}
                                    opacity={isTarget ? 1 : 0.6}
                                />
                            );
                        })}
                    </Bar>
                    <ReferenceLine x="label" stroke="red" label="Max" />
                </BarChart>
            </ResponsiveContainer>
            <div className="flex items-center justify-center gap-6 mt-2 text-xs text-gray-500">
                <div className="flex items-center gap-2">
                    <span className="w-3 h-3 bg-emerald-500 rounded-sm"></span>
                    <span>Your Range</span>
                </div>
                <div className="flex items-center gap-2">
                    <span className="w-3 h-3 bg-blue-500/60 rounded-sm"></span>
                    <span>Market</span>
                </div>
            </div>
        </div>
    );
}
