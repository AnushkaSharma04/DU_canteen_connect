<template>
  <div class="wrapper">
    <Header />

    <div class="profile-container">
      <h2>Create Canteen Profile</h2>
      <form @submit.prevent="handleCanteenProfile">
        
        <div class="form-row">
          <div class="form-group">
            <label for="name">Canteen Name</label>
            <input v-model="name" type="text" id="name" />
          </div>
          <div class="form-group">
            <label for="location">Location</label>
            <input v-model="location" type="text" id="location" />
          </div>
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <input v-model="description" type="text" id="description" />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="contact">Contact Info</label>
            <input v-model="contact" type="text" id="contact" />
          </div>
          <div class="form-group">
            <label for="daysOpen">Days Open</label>
            <input v-model="daysOpen" type="text" id="daysOpen" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="timings">Opening Time</label>
            <input v-model="openingTime" type="text" id="openingTime" />
          </div>
          <div class="form-group">
            <label for="timings">Closing Time</label>
            <input v-model="closingTime" type="text" id="closingTime" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="peakHours">Starting Peak Hour</label>
            <input v-model="peakStart" type="text" id="peakStart" />
          </div>
          <div class="form-group">
            <label for="peakHours">Closing Peak Hour</label>
            <input v-model="peakEnd" type="text" id="peakEnd" />
          </div>
        </div>

        


        <div class="form-group">
          <label for="menuUpload">Upload Menu</label>
          <input type="file" id="menuUpload" @change="handleFileUpload" />
        </div>

        <button type="submit" class="create-btn">Create</button>
      </form>
      <p v-if="errorMsg" style="color:red; text-align:center;">{{ errorMsg }}</p>
    </div>
    <Footer />
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
import { createCanteenProfile } from '@/services/auth' // import API function

export default {
  components: { Header, Footer },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const owner_id = route.query.owner_id || localStorage.getItem("owner_id")
    const errorMsg = ref('')

    const name = ref('')
    const location = ref('')
    const description = ref('')
    const contact = ref('')
    const daysOpen = ref('')
    const openingTime = ref('')
    const closingTime = ref('')
    const peakStart = ref('')
    const peakEnd = ref('')
    const menuFile = ref(null)

    function handleFileUpload(event) {
      menuFile.value = event.target.files[0]
    }

    const handleCanteenProfile = async () => {
      try {
        // Get owner_id from query params (from signup redirect)
        const urlParams = new URLSearchParams(window.location.search)
        

        if (!owner_id) {
          errorMsg.value = "Owner ID missing"
          return
        }

        const profileData = {
          canteen_name: name.value,
          location: location.value,
          description: description.value,
          contact_number: contact.value,
          days_open: daysOpen.value,
          opening_time: openingTime.value,
          closing_time: closingTime.value,
          peak_hr_start_time: peakStart.value,
          peak_hr_end_time: peakEnd.value,
          

        }
        if (menuFile.value) {
      profileData.menu_file = menuFile.value
    }

        const res = await createCanteenProfile(owner_id, profileData)

        // Save JWT token returned from backend
        if (res.token) {
          localStorage.setItem('token', res.token)
        }
        if (res.redirect_url) {
        window.location.href = res.redirect_url
        return
      }


        // Fallback message if redirect_url is missing
        alert(response.message || 'Canteen profile created successfully!')

      } 

        
        catch (err) {
        console.error(err)
        errorMsg.value = err.response?.data?.message || "Failed to create profile"
      }
    }

    return {
      name, location, description, contact, daysOpen,
      openingTime, closingTime, peakStart, peakEnd, menuFile,
      handleFileUpload, handleCanteenProfile, errorMsg
    }
  }
}
</script>

<style scoped>
.wrapper {
  padding-top: 60px;
}

.profile-container {
  position: relative;
  max-width: 600px;
  margin: 5rem auto;
  padding: 2rem;
  background: rgba(219, 223, 208, 0.18);
  box-shadow: 0px 4px 10px 3px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(5px);
  border-radius: 25px;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #696D5F;
}

.form-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #696D5F;
}

input {
  padding: 0.75rem;
  border-radius: 10px;
  border: none;
  background: rgba(71, 71, 71, 0.41);
  color: white;
  font-size: 1rem;
  backdrop-filter: blur(2px);
}

input::placeholder {
  color: rgba(255, 255, 255, 0.58);
}

.create-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #474747;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 2rem;
}

.create-btn:hover {
  background-color: #333;
}
 /* 📱 Responsive Layout for Mobile & Tablets */
@media (max-width: 768px) {
  .profile-container {
    margin: 3rem 1rem;
    padding: 1.5rem;
  }

  .form-row {
    flex-direction: column;
    gap: 1rem;
  }

  input {
    font-size: 0.95rem;
    padding: 0.65rem;
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .create-btn {
    font-size: 1rem;
    padding: 0.75rem;
    margin-top: 1.5rem;
  }
}

</style>
