import api from './client'

export function getDashboard() {
  return api.get('/provider/dashboard').then((r) => r.data)
}

export function toggleServiceStatus(serviceId) {
  return api.patch(`/provider/dashboard/services/${serviceId}/toggle-status`).then((r) => r.data)
}

export function getBookings(statusFilter) {
  return api
    .get('/provider/dashboard/bookings', { params: statusFilter ? { status_filter: statusFilter } : {} })
    .then((r) => r.data)
}

export function updateBookingStatus(bookingId, status) {
  return api
    .patch(`/provider/dashboard/bookings/${bookingId}/status`, { status })
    .then((r) => r.data)
}

export function listServices() {
  return api.get('/provider/services').then((r) => r.data)
}

export function createService(payload) {
  return api.post('/provider/services', payload).then((r) => r.data)
}

export function updateService(serviceId, payload) {
  return api.patch(`/provider/services/${serviceId}`, payload).then((r) => r.data)
}

export function deleteService(serviceId) {
  return api.delete(`/provider/services/${serviceId}`)
}

export function getAnalytics() {
  return api.get('/provider/analytics').then((r) => r.data)
}

export function listTickets() {
  return api.get('/provider/support/tickets').then((r) => r.data)
}

export function createTicket(payload) {
  return api.post('/provider/support/tickets', payload).then((r) => r.data)
}
