<template>
  <div class="container">
    <div class="login">
      <div class="login-container">
        <h1 class="welcome">用户注册</h1>
        <!--邮箱-->
        <div class="input-group">
          <label>邮箱</label>
          <input type="email" v-model="email" placeholder="请输入邮箱" />
        </div>
        <!--用户名-->
        <div class="input-group">
          <label>用户名</label>
          <input type="text" v-model="username" placeholder="请输入用户名" />
        </div>
        <!--密码-->
        <div class="input-group">
          <label>密码</label>
          <input type="password" v-model="password" placeholder="请输入密码" />
        </div>
        <!--确认密码-->
        <div class="input-group">
          <label>确认密码</label>
          <input type="password" v-model="confirmPassword" placeholder="请再次输入密码" />
        </div>
        <p class="register-tip">
          已有账户？
          <a href="#" class="register-link" @click="Switch2Login">去登陆</a>
        </p>
        <button class="login-button" @click="submit">登陆</button>
      </div>
    </div>
  </div>
</template>

<script>
import DataService from '@/services/DataService.js'
import LoginBox from './LoginBox.vue'
export default {
  data() {
    return {
      email: '',
      username: '',
      password: '',
      confirmPassword: '',
    }
  },
  emits: ['UpdateLoginView'],
  methods: {
    Switch2Login() {
      this.$emit('UpdateLoginView', LoginBox)
    },
    submit() {
      if (!this.email) {
        alert('请输入邮箱')
        return
      }
      if (!this.username) {
        alert('请输入用户名')
        return
      }
      if (!this.password) {
        alert('请输入密码')
        return
      }
      if (this.password !== this.confirmPassword) {
        alert('两次输入的密码不一致')
        return
      }
      DataService.post('/register', {
        email: this.email,
        username: this.username,
        password: this.password,
      })
        .then((response) => {
          if (response.data.success) {
            console.log('注册成功！', response.data)
            alert('注册成功！请登录！')
            this.$emit('UpdateLoginView', 'LoginBox')
          } else {
            console.log('注册失败！', response.data)
            alert('注册失败！请重试！')
          }
        })
        .catch((error) => {
          console.error('注册失败！', error)
          alert('注册失败，请稍后再试！')
        })
    },
  },
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  background-color: var(--primary-color); /* 页面深黑色背景 */
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
  background-color: var(--secondary-color); /* 登录窗口黑灰色背景 */
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
</style>
