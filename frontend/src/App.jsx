import { useEffect, useState } from 'react'
import { getOverview, getRevenue, getProducts, getCustomers } from './api'
import axios from 'axios'
import KPICard from './components/KPICard'
import RevenueChart from './components/RevenueChart'
import ProductsTable from './components/ProductsTable'
import CustomerSegments from './components/CustomerSegments'
import CohortMatrix from './components/CohortMatrix'
import GrowthCard from './components/GrowthCard'

export default function App() {
  const [overview, setOverview] = useState(null)
  const [revenue, setRevenue] = useState([])
  const [products, setProducts] = useState([])
  const [customers, setCustomers] = useState([])
  const [cohort, setCohort] = useState([])
  const [growth, setGrowth] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      getOverview(), getRevenue(), getProducts(), getCustomers(),
      axios.get('/api/metrics/cohort/'),
      axios.get('/api/metrics/growth/'),
    ]).then(([o, r, p, c, co, g]) => {
      setOverview(o.data)
      setRevenue(r.data)
      setProducts(p.data)
      setCustomers(c.data)
      setCohort(co.data)
      setGrowth(g.data)
    }).finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="min-h-screen bg-[#0f1117] flex items-center justify-center">
      <div className="text-center">
        <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-slate-500 text-sm">Loading Meridian...</p>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-[#0f1117]">
      <header className="border-b border-[#2a2d3a] px-8 py-4 flex items-center justify-between bg-[#0f1117] sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 bg-indigo-600 rounded-lg flex items-center justify-center">
            <span className="text-white text-xs font-bold">M</span>
          </div>
          <div>
            <h1 className="text-sm font-bold text-white">Meridian</h1>
            <p className="text-xs text-slate-500">E-commerce Intelligence</p>
          </div>
        </div>
        {overview?.last_sync && (
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full" />
            <p className="text-xs text-slate-500">
              Synced {new Date(overview.last_sync).toLocaleString()}
            </p>
          </div>
        )}
      </header>

      <main className="px-8 py-6 max-w-7xl mx-auto space-y-5">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <KPICard title="Total Revenue" value={`$${Number(overview?.total_revenue || 0).toLocaleString()}`} delta={growth?.revenue_growth} />
          <KPICard title="Total Orders" value={overview?.total_orders || 0} delta={growth?.orders_growth} />
          <KPICard title="Avg Order Value" value={`$${Number(overview?.avg_aov || 0).toFixed(2)}`} />
          <KPICard title="Total Customers" value={overview?.total_customers || 0} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-2">
            <RevenueChart data={revenue} />
          </div>
          <GrowthCard growth={growth} />
        </div>

        <CohortMatrix data={cohort} />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <ProductsTable data={products} />
          <CustomerSegments data={customers} />
        </div>
      </main>
    </div>
  )
}
