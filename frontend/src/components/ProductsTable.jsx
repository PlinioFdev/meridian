export default function ProductsTable({ data }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <h2 className="text-sm font-semibold text-gray-500 mb-4">TOP PRODUCTS</h2>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-gray-400 border-b">
            <th className="pb-2">Product</th>
            <th className="pb-2 text-right">Units</th>
            <th className="pb-2 text-right">Revenue</th>
          </tr>
        </thead>
        <tbody>
          {data.map((p, i) => (
            <tr key={i} className="border-b last:border-0">
              <td className="py-2 text-gray-700">{p.title}</td>
              <td className="py-2 text-right text-gray-500">{p.units_sold}</td>
              <td className="py-2 text-right font-medium">${p.revenue}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
