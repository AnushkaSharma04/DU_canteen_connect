<template>
  <div class="wrapper">
    <Header />

    <div class="profile-container">
      <h2>Create Profile</h2>
      <form @submit.prevent="handleProfile">
        <div class="form-group">
          <label for="name">Name</label>
          <input v-model="name" type="text" id="name" required />
        </div>

        <div class="form-group">
          <label for="age">Age</label>
          <input v-model="age" type="number" id="age" required />
        </div>

        <div class="form-group radio-group">
          <label>User</label>
          <div class="radio-container">
            <div class="radio-option" v-for="option in roles" :key="option">
              <label>
                <input
                  type="radio"
                  :value="option"
                  v-model="selectedRole"
                  name="user-role"
                />
                {{ option }}
              </label>
            </div>
          </div>
        </div>

        <div class="next-action" @click="handleProfile">
          Next <span class="arrow">→</span>
        </div>
      </form>
    </div>
  </div>
</template>



<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Header from '../components/Header.vue'

export default {
    components: {
        Header
    },
    setup() {
        const name = ref('')
        const age = ref('')
        const roles = ['General', 'Canteen Owner'] 
        const selectedRole = ref('')
        
        const router = useRouter()

        function handleProfile() {
            if(selectedRole.value === "General"){
                router.push('/home');
            } else {
                router.push('/signup/canteenprofile');
            } 
        }
        return {
            name,
            age,
            roles,        
            selectedRole, 
            handleProfile  
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
  max-width: 500px;
  margin: 5rem auto;
  padding: 2rem;
  background: rgba(219, 223, 208, 0.18);
  box-shadow: 0px 4px 10px 3px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(5px);
  border-radius: 25px;
}

.form-group {
  margin-bottom: 2rem;
}

label, h2 {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #696D5F;
}

h2 {
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

.radio-group {
  margin-bottom: 2rem;
}

.radio-container {
  width: 100%;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0.75rem 1rem;
  margin-top: 1rem;
}

.radio-option {
  font-size: 1rem;
  color: #474747;
  margin-right: 1rem;
}


input[type="radio"] {
  margin-right: 0.5rem;
  accent-color: #696D5F;
}

.next-action {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  font-size: 1.1rem;
  font-weight: 600;
  color: #474747;
  cursor: pointer;
  margin-top: 2rem;
}

.arrow {
  margin-left: 0.5rem;
  font-size: 1.3rem;
}

</style>
