import { useEffect, useState } from 'react'
import { getOverview, getRevenue, getProducts, getCustomers } from './api'
import KPICard from './components/KPICard'
import RevenueChart from './components/RevenueChart'
import ProductsTable from './components/ProductsTable'
import CustomerSegments from './components/CustomerSegments'

export default function App() {
  const [overview, setOverview] = useState(null)
  const [revenue, setRevenue] = useState([])
  const [products, setProducts] = useState([])
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getOverview(), getRevenue(), getProducts(), getCustomers()])
      .then(([o, r, p, c]) => {
        setOverview(o.data)
        setRevenue(r.data)
        setProducts(p.data)
        setCustomers(c.data)
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <p className="text-gray-400 text-sm">Loading Meridian...</p>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-8 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-900">Meridian</h1>
          <p className="text-xs text-gray-400">E-commerce Intelligence Platform</p>
        </div>
        {overview?.last_sync && (
          <p className="text-xs text-gray-400">
            Last sync: {new Date(overview.last_sync).toLocaleString()}
          </p>
        )}
      </header>

      <main className="px-8 py-6 max-w-7xl mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <KPICard title="Total Revenue" value={`$${Number(overview?.total_revenue || 0).toFixed(2)}`} color="blue" />
          <KPICard title="Total Orders" value={overview?.total_orders || 0} color="purple" />
          <KPICard title="Avg Order Value" value={`$${Number(overview?.avg_aov || 0).toFixed(2)}`} color="green" />
          <KPICard title="Total Customers" value={overview?.total_customers || 0} color="orange" />
        </div>

        <div className="mb-6">
          <RevenueChart data={revenue} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ProductsTable data={products} />
          <CustomerSegments data={customers} />
        </div>
      </main>
    </div>
  )
}
