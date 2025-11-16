// src/services/user.js
import api from './api'

// Protected: requires Authorization header with JWT (api.js adds it)
export const fetchUserInfo = async () => {
  const res = await api.get('/display_user_info')
  return res.data // backend should return user info object
}

export const fetchUserReviews = async () => {
  const res = await api.get('/display_user_reviews')
  return res.data // backend should return list/structure of reviews
}

// Feedback about the app (text)
export const submitAppFeedback = async (payload) => {
  // payload: { feedback_text: "..." }
  const res = await api.post('/give_app_feedback', payload)
  return res.data
}

// Report an issue (text)
export const submitAppIssue = async (payload) => {
  // payload: { issue_text: "..." }
  const res = await api.post('/report_app_issue', payload)
  return res.data
}

// Update user profile (name, email, phone_number, password)
export const updateUserProfile = async (payload) => {
  const formData = new FormData()
  for (const key in payload) {
    if (payload[key] !== null && payload[key] !== undefined && payload[key] !== '') {
      formData.append(key, payload[key])
    }
  }
  const res = await api.post('/user_profile_update', formData)
  return res.data
}
