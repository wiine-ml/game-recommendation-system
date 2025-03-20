<template>
  <div class="container">
    <div class="login">
      <div class="login-container">
        <h1 class="welcome">欢迎登陆</h1>
        <div class="input-group">
          <label>账户邮箱</label>
          <input type="text" v-model="emailOrName" placeholder="请输入账户" />
        </div>
        <div class="input-group">
          <label>密码</label>
          <input type="password" v-model="password" placeholder="请输入密码" />
        </div>

        <div class="radio-group">
          <div>
            <input type="radio" id="isUser" name="LoginType" value="user" v-model="loginType" />
            <label for="isUser">用户</label>
          </div>
          <input
            type="radio"
            id="isDeveloper"
            name="LoginType"
            value="vendor"
            v-model="loginType"
          />
          <label for="isDeveloper">厂商</label>
          <div>
            <input
              type="radio"
              id="isAdministrator"
              name="LoginType"
              value="admin"
              v-model="loginType"
            />
            <label for="isAdministrator">管理员</label>
          </div>
        </div>

        <p class="register-tip">
          未有账户？
          <a href="#" class="register-link" @click.prevent="Switch2Register">去注册</a>
        </p>

        <button class="login-button" @click="submit">登陆</button>
      </div>
    </div>
  </div>
</template>

<script>
import RegistrationBox from './RegistrationBox.vue'
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      emailOrName: '',
      password: '',
      loginType: 'user',
    }
  },
  methods: {
    ...mapActions('user', ['fetchAvatar']),
    async submit() {
      try {
        console.log(this.loginType + '开始登录...')
        if (this.loginType === 'user') {
          console.log('用户登录中...')
          const response = await this.$store.dispatch('user/login', {
            emailOrName: this.emailOrName,
            password: this.password,
          })

          if (response.success) {
            alert('用户登录成功！')
            this.$emit('UpdateLoginView', null)
            location.reload()
          } else {
            alert('登录失败，请检查用户名或密码！')
          }
        } else if (this.loginType === 'admin') {
          console.log('管理员登录中...')
          const response = await this.$store.dispatch('admin/login', {
            emailOrName: this.emailOrName,
            password: this.password,
          })

          if (response.success) {
            alert('管理员登录成功！')
            this.$emit('UpdateLoginView', null)
            location.reload()
          } else {
            alert('登录失败，请检查用户名或密码！')
          }
        } else if (this.loginType === 'vendor') {
          console.log('厂商登录中...')
          const response = await this.$store.dispatch('vendor/login', {
            emailOrName: this.emailOrName,
            password: this.password,
          })
          console.log(response)
          if (response.success) {
            alert('厂商登录成功！')
            this.$emit('UpdateLoginView', null)
            location.reload()
          } else {
            alert('登录失败，请检查用户名或密码！')
          }
        }
      } catch (err) {
        console.log('登录失败', err)
        alert('登录失败，请检查用户名或密码！')
      } finally {
        if (this.isLogin) {
          this.fetchAvatar().then((response) => {
            if (response.success) {
              this.$store.commit('user/setAvatarFile', response.data.avatarFile)
            }
          })
        }
      }
    },
    Switch2Register() {
      this.$emit('UpdateLoginView', RegistrationBox)
    },
  },
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  background-color: var(--primary-color);
  color: var(--contrast-color);
  font-family: Arial, sans-serif;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login {
  padding: 20px;
}

.login-container {
  background-color: var(--secondary-color);
  padding: 40px;
  border-radius: 5px;
  width: 350px;
  box-shadow: 0 0 10px var(--secondary-color);
}

.welcome {
  text-align: center;
  margin-bottom: 30px;
  font-size: 32px;
  font-style: bold;
}

.input-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  background-color: var(--primary-color);
  border: none;
  border-radius: 5px;
  color: var(--contrast-color);
}

#isUser,
#isAdministrator {
  color: var(--contrast-color);
}

.register-tip {
  text-align: center;
  margin-bottom: 20px;
  font-size: 14px;
}

.register-link {
  color: var(--main-color);
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
}

.login-button {
  width: 100%;
  padding: 10px;
  background-color: var(--main-color);
  border: none;
  border-radius: 5px;
  color: var(--contrast-color);
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: var(--primary-color);
}

.radio-group {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.radio-group div {
  display: flex;
  align-items: center;
}

.radio-group label {
  white-space: nowrap;
  min-width: 90px;
}
</style>
