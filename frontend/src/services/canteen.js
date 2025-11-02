import api from './api'

export const fetchAllCanteens = async () => {
  const res = await api.get('/canteens')
  return res.data.canteens || []
}

export const fetchCanteenInfo = async (canteenId) => {
  const res = await api.get(`/canteen_info?canteen_id=${canteenId}`)
  return res.data.canteen_info || {}
}

export const fetchCanteenMenu = async (canteenId) => {
  const res = await api.get(`/canteen_menu_details?canteen_id=${canteenId}`)
  return res.data || {}
}

export const fetchCanteenReviews = async (canteenId) => {
  const res = await api.get(`/canteen_review_ratings?canteen_id=${canteenId}`)
  return res.data.data || []
}
// gpt added this too
export const submitCanteenReview = async (canteenId, reviewData) => {
  const formData = new FormData()
  formData.append('canteen_id', canteenId)
  formData.append('overall_rating', reviewData.overallRating)
  formData.append('food_rating', reviewData.foodRating)
  formData.append('hygiene_rating', reviewData.hygieneRating)
  formData.append('staff_rating', reviewData.staffRating)
  formData.append('facilities_rating', reviewData.facilityRating)
  formData.append('review_text', reviewData.text)
  
  const res = await api.post('/add_review_rating', formData)
  return res.data
}
// gpt added this function
export const searchCanteens = async (query) => {
  const res = await api.get(`/search/canteens?q=${encodeURIComponent(query)}`)
  return res.data.results || []
}