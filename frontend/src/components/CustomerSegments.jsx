import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'

const COLORS = { new: '#6366f1', returning: '#22c55e', at_risk: '#f59e0b', lost: '#ef4444' }
const LABELS = { new: 'New', returning: 'Returning', at_risk: 'At Risk', lost: 'Lost' }

export default function CustomerSegments({ data }) {
  const counts = data.reduce((acc, c) => {
    acc[c.segment] = (acc[c.segment] || 0) + 1
    return acc
  }, {})
  const chartData = Object.entries(counts).map(([name, value]) => ({ name, value }))
  return (
    <div className="bg-[#1a1d27] border border-[#2a2d3a] rounded-xl p-5">
      <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">Customer Segments</h2>
      <div className="flex items-center gap-4">
        <ResponsiveContainer width="50%" height={180}>
          <PieChart>
            <Pie data={chartData} dataKey="value" cx="50%" cy="50%" outerRadius={70} innerRadius={40}>
              {chartData.map((entry) => (
                <Cell key={entry.name} fill={COLORS[entry.name] || '#94a3b8'} />
              ))}
            </Pie>
            <Tooltip formatter={(v, n) => [v, LABELS[n] || n]} contentStyle={{ background: '#1a1d27', border: '1px solid #2a2d3a', borderRadius: 8, fontSize: 12 }} />
          </PieChart>
        </ResponsiveContainer>
        <div className="space-y-2">
          {chartData.map(entry => (
            <div key={entry.name} className="flex items-center gap-2 text-sm">
              <div className="w-2 h-2 rounded-full" style={{ background: COLORS[entry.name] }} />
              <span className="text-slate-400">{LABELS[entry.name] || entry.name}</span>
              <span className="text-white font-semibold ml-auto pl-4">{entry.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
