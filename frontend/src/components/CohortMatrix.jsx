export default function CohortMatrix({ data }) {
  if (!data || data.length === 0) return null
  const months = ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6']

  const getStyle = (rate) => {
    if (!rate) return { background: '#1a1d27', color: '#374151' }
    const opacity = Math.min(rate / 100, 1)
    return {
      background: `rgba(99, 102, 241, ${0.15 + opacity * 0.75})`,
      color: opacity > 0.5 ? '#fff' : '#a5b4fc'
    }
  }

  return (
    <div className="bg-[#1a1d27] border border-[#2a2d3a] rounded-xl p-5">
      <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Cohort Retention</h2>
      <p className="text-xs text-slate-600 mb-4">% of customers who returned each month after acquisition</p>
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr>
              <th className="text-left pb-2 text-slate-500 font-medium pr-4">Cohort</th>
              <th className="text-left pb-2 text-slate-500 font-medium pr-4">Size</th>
              {months.map(m => (
                <th key={m} className="text-center pb-2 text-slate-500 font-medium px-1 w-14">{m}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row) => (
              <tr key={row.cohort}>
                <td className="pr-4 py-1 font-medium text-slate-300">{row.cohort}</td>
                <td className="pr-4 py-1 text-slate-500">{row.cohort_size}</td>
                {months.map((m) => {
                  const key = m.toLowerCase()
                  const cell = row.retention[key]
                  return (
                    <td key={m} className="px-1 py-1">
                      <div
                        className="rounded text-center py-1 px-1 font-semibold"
                        style={getStyle(cell?.rate)}
                      >
                        {cell?.rate > 0 ? `${cell.rate}%` : '—'}
                      </div>
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
