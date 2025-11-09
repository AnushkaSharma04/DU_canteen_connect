// src/services/admin.js
import api from './api'

// Get all open issues reported by users
export const getOpenIssues = async () => {
  const res = await api.get('/admin/app_issues/open')
  return res.data
}

// Get all app feedback/suggestions
export const getAppFeedbacks = async () => {
  const res = await api.get('/admin/app_feedbacks')
  return res.data
}
