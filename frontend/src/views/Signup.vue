<template>
  <div class="wrapper">
    <Header />

    <div class="signup-container">
      <h2>Signup</h2>
      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label for="name">Name</label>
          <input v-model="name" type="text" id="name" />
        </div>

        <div class="form-group">
          <label for="phone">Phone</label>
          <input v-model="phone" type="tel" id="phone" />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input v-model="email" type="email" id="email" />
        </div>

        <div class="form-group radio-group">
          <label>User Type</label>
          <div class="radio-container">
            <div
              class="radio-option"
              v-for="option in roles"
              :key="option"
              :class="{ selected: selectedRole === option }"
            >
              <label>
                <input
                  type="radio"
                  :value="option"
                  v-model="selectedRole"
                  name="user-role"
                />
                <span class="custom-radio">{{ option }}</span>
              </label>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input v-model="password" type="password" id="password" />
        </div>

        <div class="form-group">
          <label for="confirmPassword">Re-enter Password</label>
          <input v-model="confirmPassword" type="password" id="confirmPassword" />
          <p v-if="passwordMismatch" class="error-text">Passwords do not match</p>
        </div>


        <button @click="handleProfile" type="submit" class="signup-btn">Signup</button>
      </form>

      <div class="login-prompt">
        <p>Already have an account?</p>
        <router-link to="/login" class="signup-link">Login</router-link>
      </div>
    </div>
    <Footer />
  </div>
</template>


<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'

export default {
  components: { Header, Footer },


    setup() {
        const name = ref('')
        const phone = ref('')
        const password = ref('')
        const email = ref('')
        const confirmPassword = ref('')
        const passwordMismatch = ref(false)
        const roles = ['General', 'Canteen Owner'] 
        const selectedRole = ref('')
        
        const router = useRouter()

        function handleProfile() {
          if (password.value !== confirmPassword.value) {
            passwordMismatch.value = true
            return
          } else {
            passwordMismatch.value = false
          }

          if (selectedRole.value === "General") {
            router.push('/home')
          } else {
            router.push('/signup/canteenprofile')
          }
        }
        return {
          name,
          phone,
          email,
          password,
          confirmPassword,
          passwordMismatch,
          roles,
          selectedRole,
          handleProfile
        }
    }
  }
</script>


<style scoped>
.error-text {
  color: #ff4d4d;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.wrapper{
    padding-top: 60px;
}
.signup-container {
  position:relative;
  max-width: 500px;
  margin: 5rem auto;
  padding: 2rem;
  background: rgba(219, 223, 208, 0.18);
  box-shadow: 0px 4px 10px 3px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(5px);
  border-radius: 25px;
}

.form-group {
  margin-bottom: 1.5rem;
}

label,h2 {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #696D5F;
}

h2{
    position: relative;
    text-align: center;
}

input {
  width: 100%;
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

.signup-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #474747;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
}

.signup-btn:hover {
  background-color: #333;
}

.login-prompt {
  text-align: center;
  margin-top: 2rem;
  font-size: 1rem;
  color: #696D5F;
}

.login-prompt a {
  text-decoration: underline;
  color: #696D5F;
}

.radio-group label {
  margin-bottom: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  color: #696D5F;
}

.radio-container {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.radio-option {
  background: rgba(71, 71, 71, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.3s ease;
  border: 2px solid transparent;
}

.radio-option:hover {
  background: rgba(71, 71, 71, 0.5);
}

.radio-option.selected {
  border-color: #DBDFD0;
  background: rgba(71, 71, 71, 0.6);
}

.radio-option input[type="radio"] {
  display: none;
}

.custom-radio {
  color: white;
  font-size: 1rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .signup-container {
    margin: 3rem 1rem;
    padding: 1.5rem;
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }

  input {
    font-size: 0.95rem;
    padding: 0.65rem;
  }

  .signup-btn {
    font-size: 1rem;
    padding: 0.75rem;
  }

  .radio-container {
    flex-direction: column;
    gap: 0.75rem;
  }

  .radio-option {
    width: 100%;
    text-align: center;
  }

  .custom-radio {
    font-size: 0.95rem;
  }

  .login-prompt {
    font-size: 0.95rem;
    margin-top: 1.5rem;
  }
}


</style>
