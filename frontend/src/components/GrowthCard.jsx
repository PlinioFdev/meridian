export default function GrowthCard({ growth }) {
  if (!growth) return null
  const fmt = (v) => v !== null ? `${v > 0 ? '+' : ''}${v}%` : 'N/A'
  const color = (v) => v === null ? 'text-slate-400' : v >= 0 ? 'text-emerald-400' : 'text-red-400'

  return (
    <div className="bg-[#1a1d27] border border-[#2a2d3a] rounded-xl p-5">
      <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">Month over Month</h2>
      <div className="space-y-4">
        <div>
          <p className="text-xs text-slate-500 mb-1">Revenue</p>
          <p className="text-2xl font-bold text-white">${Number(growth.this_month?.revenue || 0).toLocaleString()}</p>
          <p className={`text-xs font-semibold mt-1 ${color(growth.revenue_growth)}`}>{fmt(growth.revenue_growth)} vs last month</p>
        </div>
        <div className="border-t border-[#2a2d3a] pt-4">
          <p className="text-xs text-slate-500 mb-1">Orders</p>
          <p className="text-2xl font-bold text-white">{growth.this_month?.orders || 0}</p>
          <p className={`text-xs font-semibold mt-1 ${color(growth.orders_growth)}`}>{fmt(growth.orders_growth)} vs last month</p>
        </div>
      </div>
    </div>
  )
}
