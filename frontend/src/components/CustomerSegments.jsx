import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = { new: '#6366f1', returning: '#22c55e', at_risk: '#f59e0b', lost: '#ef4444' }

export default function CustomerSegments({ data }) {
  const counts = data.reduce((acc, c) => {
    acc[c.segment] = (acc[c.segment] || 0) + 1
    return acc
  }, {})
  const chartData = Object.entries(counts).map(([name, value]) => ({ name, value }))
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h2 className="text-sm font-semibold text-gray-500 mb-4">CUSTOMER SEGMENTS</h2>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
            {chartData.map((entry) => (
              <Cell key={entry.name} fill={COLORS[entry.name] || '#94a3b8'} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
