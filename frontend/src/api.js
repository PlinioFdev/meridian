import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getOverview = () => api.get('/metrics/overview/')
export const getRevenue = () => api.get('/metrics/revenue/')
export const getProducts = () => api.get('/metrics/products/')
export const getCustomers = () => api.get('/metrics/customers/')
export const getSyncStatus = () => api.get('/sync/status/')
