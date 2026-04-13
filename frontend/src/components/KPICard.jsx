export default function KPICard({ title, value, subtitle, delta }) {
  const isPositive = delta > 0
  return (
    <div className="bg-[#1a1d27] border border-[#2a2d3a] rounded-xl p-5 hover:border-indigo-500/40 transition-colors">
      <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</p>
      <p className="text-3xl font-bold text-white mt-2">{value}</p>
      {delta !== undefined && (
        <p className={`text-xs mt-2 font-medium ${isPositive ? 'text-emerald-400' : 'text-red-400'}`}>
          {isPositive ? '▲' : '▼'} {Math.abs(delta)}% vs last month
        </p>
      )}
      {subtitle && <p className="text-xs mt-1 text-slate-500">{subtitle}</p>}
    </div>
  )
}
