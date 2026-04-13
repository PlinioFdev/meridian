export default function ProductsTable({ data }) {
  const max = Math.max(...data.map(p => Number(p.revenue)))
  return (
    <div className="bg-[#1a1d27] border border-[#2a2d3a] rounded-xl p-5">
      <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">Top Products</h2>
      <div className="space-y-3">
        {data.map((p, i) => (
          <div key={i}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-slate-300 truncate pr-4">{p.title}</span>
              <span className="text-white font-semibold whitespace-nowrap">${Number(p.revenue).toLocaleString()}</span>
            </div>
            <div className="h-1 bg-[#2a2d3a] rounded-full">
              <div
                className="h-1 bg-indigo-500 rounded-full"
                style={{ width: `${(Number(p.revenue) / max) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
