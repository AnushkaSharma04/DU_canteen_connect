<template>
  <div class="page-wrapper">
    <!-- Header -->
    <Header />
    <div class="admin-dashboard">
    <!-- Loading State -->
    <div v-if="loading" class="loading-message">
      <p>Loading admin data...</p>
    </div>

    <!-- Error State -->
    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
      <button @click="loadAdminData">Retry</button>
    </div>

    <!-- Content (only show when not loading and no error) -->
    <template v-if="!loading && !error">
      <!-- Reported Issues -->
      <section class="card issues-section">
        <h2>Reported Issues</h2>
        <ul class="issue-list" v-if="reportedIssues.length > 0">
          <li v-for="issue in reportedIssues" :key="issue.id">
            {{ issue.display }}
          </li>
        </ul>
        <p v-else class="empty-message">No issues reported yet.</p>
      </section>

      <!-- Feedback/Suggestions -->
      <section class="card feedback-section">
        <h2>Feedback/Suggestions</h2>
        <ul class="feedback-list" v-if="feedbackEntries.length > 0">
          <li v-for="feedback in feedbackEntries" :key="`${feedback.id}-${feedback.slot}`">
            {{ feedback.display }}
          </li>
        </ul>
        <p v-else class="empty-message">No feedback received yet.</p>
      </section>

      <!-- Reviews and Ratings -->
      <section class="card review-section">
        <h2>Reviews and Ratings</h2>
        <p class="info-message">Review management here.</p>
        <ul class="review-list" v-if="reviews.length > 0">
          <li v-for="(review, index) in reviews" :key="index" class="review-item">
            <span class="stars">{{ getStars(review.rating) }}</span>
            <span class="review-text">{{ review.text }}</span>
            <div class="review-actions">
              <button @click="editReview(index)">✎</button>
              <button @click="deleteReview(index)">✕</button>
            </div>
          </li>
        </ul>
      </section>
    </template>

  </div>
  <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { getOpenIssues, getAppFeedbacks } from '@/services/admin'

export default {
  name: 'AdminDashboard',
  components: { Header, Footer },
  data() {
    return {
      reportedIssues: [],
      feedbackEntries: [],
      reviews: [],
      loading: true,
      error: null
    }
  },
  async mounted() {
    // Verify JWT token exists
    const token = localStorage.getItem('token')
    if (!token) {
      this.$router.push('/desktop6')
      return
    }

    await this.loadAdminData()
  },
  methods: {
    async loadAdminData() {
      try {
        this.loading = true
        this.error = null

        // Fetch issues and feedbacks in parallel
        const [issuesResponse, feedbacksResponse] = await Promise.all([
          getOpenIssues(),
          getAppFeedbacks()
        ])

        // Process issues
        if (issuesResponse.issues) {
          this.reportedIssues = issuesResponse.issues.map(issue => ({
            id: issue.issue_id,
            userId: issue.user_id,
            role: issue.role,
            text: issue.issue_text,
            createdAt: issue.created_at,
            display: `User ${issue.user_id} (${issue.role}): ${issue.issue_text}`
          }))
        }

        // Process feedbacks
        if (feedbacksResponse.feedbacks) {
          this.feedbackEntries = feedbacksResponse.feedbacks.map(feedback => ({
            id: feedback.feedback_id,
            userId: feedback.user_id,
            text: feedback.feedback_text,
            slot: feedback.slot,
            createdAt: feedback.created_at,
            display: `User ${feedback.user_id}: ${feedback.feedback_text}`
          }))
        }

        this.loading = false
      } catch (err) {
        console.error('Error loading admin data:', err)
        this.error = err.response?.data?.message || 'Failed to load admin data'
        this.loading = false

        // If unauthorized, redirect to login
        if (err.response?.status === 401 || err.response?.status === 403) {
          localStorage.removeItem('token')
          this.$router.push('/desktop6')
        }
      }
    },
    getStars(rating) {
      return '✪'.repeat(rating)
    },
    editReview(index) {
      alert(`Edit review ${index + 1}`)
    },
    deleteReview(index) {
      this.reviews.splice(index, 1)
    }
  }
}
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.admin-dashboard {
  padding-top: 100px;
  max-width: 1200px;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Header */
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 75px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.logo {
  display: flex;
  align-items: center;
}

.logo-img {
  width: 40px;
  margin-right: 1rem;
}

.app-name {
  font-size: 1.8rem;
  font-weight: 600;
  font-family: 'Playfair Display', serif;
  font-style: italic;
  color: #474747;
}

.searchbar {
  width: 30%;
  height: 40px;
  border-radius: 20px;
  border: none;
  background: #d9d9d9;
  padding: 0 1rem;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  text-decoration: none;
  color: #474747;
  font-weight: 500;
}

/* Card */
.card {
  background: rgba(219, 223, 208, 0.18);
  backdrop-filter: blur(5px);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Loading and Error Messages */
.loading-message,
.error-message {
  text-align: center;
  padding: 2rem;
  background: rgba(219, 223, 208, 0.18);
  backdrop-filter: blur(5px);
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.error-message {
  color: #c0392b;
}

.error-message button {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: #474747;
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.empty-message,
.info-message {
  text-align: center;
  color: #666;
  font-style: italic;
  padding: 1rem;
}

/* Lists */
.issue-list,
.feedback-list,
.review-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0 0;
}

.issue-list li,
.feedback-list li {
  padding: 0.5rem 0;
  font-size: 1rem;
  color: #333;
  border-bottom: 1px dashed #aaa;
}

/* Reviews */
.review-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px dashed #aaa;
}

.stars {
  color: #f5a623;
  font-weight: bold;
  margin-right: 1rem;
}

.review-text {
  flex: 1;
  color: #333;
}

.review-actions button {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  margin-left: 0.5rem;
  color: #474747;
}

.footer{
  margin-top: auto;        /* pushes footer to bottom */
  position: relative; 
}
</style>
