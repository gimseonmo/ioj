<template>
  <div class="register-container">
    <div class="register-wrapper">
      <div class="register-card">
        <div class="logo-section">
          <div class="logo-img">
            <b-icon icon="person-plus-fill" class="logo-icon"></b-icon>
          </div>
          <p class="welcome-text">새 계정을 만들어 시작해보세요</p>
        </div>

        <b-form ref="formRegister" :model="formRegister" class="register-form">
          <div class="form-group">
            <label class="form-label">
              <b-icon icon="person-fill" class="label-icon"/>
              학번
            </label>
            <div class="input-wrapper">
              <b-icon icon="person" class="input-icon"/>
              <b-form-input
                v-model="formRegister.username"
                placeholder="학번을 입력하세요"
                maxlength="20"
                @keydown.enter.native="handleRegister"
                class="form-input"
              />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">
              <b-icon icon="envelope-fill" class="label-icon"/>
              School Email
            </label>
            <div class="email-row">
              <div class="input-wrapper email-prefix">
                <b-icon icon="at" class="input-icon"/>
              <b-form-input
                v-model="formRegister.emailPrefix"
                placeholder="학번만 입력"
                maxlength="7"
                @keydown.enter.native="handleRegister"
                class="form-input"
              />
              </div>
              <div class="email-domain">@shindo.hs.kr</div>
            </div>
            <p class="field-hint">{{ fullEmailPreview }}</p>
          </div>

          <div class="form-group">
            <label class="form-label">
              <b-icon icon="grid-fill" class="label-icon"/>
              Position
            </label>
            <div class="role-grid">
              <button
                v-for="role in roleOptions"
                :key="role.value"
                type="button"
                class="role-card"
                :class="{ active: formRegister.major === role.value }"
                @click="formRegister.major = role.value"
              >
                <b-icon :icon="role.icon" class="role-icon"></b-icon>
                <span class="role-title">{{ role.label }}</span>
                <span class="role-desc">{{ role.description }}</span>
              </button>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">
              <b-icon icon="lock-fill" class="label-icon"/>
              Password
            </label>
            <div class="input-wrapper">
              <b-icon icon="lock" class="input-icon"/>
              <b-form-input
                type="password"
                v-model="formRegister.password"
                placeholder="비밀번호를 입력하세요"
                @keydown.enter.native="handleRegister"
                class="form-input"
              />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">
              <b-icon icon="shield-lock-fill" class="label-icon"/>
              Password Confirm
            </label>
            <div class="input-wrapper">
              <b-icon icon="shield-lock" class="input-icon"/>
              <b-form-input
                type="password"
                v-model="formRegister.passwordAgain"
                placeholder="비밀번호를 다시 입력하세요"
                @keydown.enter.native="handleRegister"
                class="form-input"
              />
            </div>
          </div>

          <b-button
            class="register-btn"
            @click="handleRegister"
            :disabled="btnRegisterLoading"
          >
            <b-spinner v-if="btnRegisterLoading" small class="mr-2"></b-spinner>
            <span v-if="btnRegisterLoading">가입 중...</span>
            <span v-else>회원가입</span>
          </b-button>
        </b-form>

        <div class="footer-links">
          <p class="footer-text">이미 계정이 있으신가요?</p>
          <a @click="switchMode('login')" class="footer-link">
            <b-icon icon="box-arrow-in-right" class="mr-1"></b-icon>
            로그인
          </a>
        </div>
      </div>

      <div class="decoration decoration-top"></div>
      <div class="decoration decoration-bottom"></div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import api from '@oj/api'
import { FormMixin } from '@oj/components/mixins'

export default {
  name: 'Register',
  mixins: [FormMixin],
  data () {
    return {
      btnRegisterLoading: false,
      formRegister: {
        username: '',
        emailPrefix: '',
        password: '',
        passwordAgain: '',
        major: ''
      },
      roleOptions: [
        {
          value: 'Developer',
          label: '개발자',
          description: '코드를 작성하고 문제를 해결해요',
          icon: 'code-slash'
        },
        {
          value: 'Planner',
          label: '기획자',
          description: '아이디어와 흐름을 설계해요',
          icon: 'pencil-square'
        }
      ]
    }
  },
  computed: {
    ...mapGetters(['website', 'modalStatus']),
    fullEmailPreview () {
      if (!this.formRegister.emailPrefix) {
        return '@shindo.hs.kr'
      }
      return `${this.formRegister.emailPrefix}@shindo.hs.kr`
    }
  },
  methods: {
    ...mapActions(['changeModalStatus', 'getProfile']),
    switchMode (mode) {
      this.changeModalStatus({
        mode,
        visible: true
      })
    },
    async handleRegister () {
      const formData = Object.assign({}, this.formRegister)

      if (!formData.emailPrefix || !/^\d{7}$/.test(formData.emailPrefix)) {
        return this.$error('이메일에는 학번 7자리를 입력해주세요.')
      }

      if (!formData.major) {
        return this.$error('역할을 선택해주세요.')
      }

      if (!formData.password || formData.password.length < 6) {
        return this.$error('비밀번호는 최소 6자 이상이어야 합니다.')
      }

      if (formData.password !== formData.passwordAgain) {
        return this.$error('비밀번호가 일치하지 않습니다.')
      }

      const payload = {
        username: formData.username,
        email: `${formData.emailPrefix}@shindo.hs.kr`,
        password: formData.password,
        major: formData.major
      }

      this.btnRegisterLoading = true

      try {
        await api.register(payload)
        this.$success('회원가입이 완료되었습니다! 로그인하세요.', 2500)
        this.changeModalStatus({ visible: false })
        this.switchMode('login')
      } catch (err) {
      } finally {
        this.btnRegisterLoading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
$primary-blue: #4c6ef5;
$primary-dark-blue: #364fc7;
$primary-light-blue: #f0f3ff;
$primary-blue-shadow: rgba(76, 110, 245, 0.2);
$text-primary: #111111;
$text-secondary: #888888;
$bg-white: #ffffff;
$border-light: #e9ecef;

* {
  box-sizing: border-box;
}

.register-container {
  background: linear-gradient(135deg, #e7f0ff 0%, #d4e5ff 100%);
  min-height: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  position: relative;
  overflow: visible;
}

.register-wrapper {
  width: 100%;
  max-width: 420px;
  position: relative;
  z-index: 1;
  max-height: min(85vh, 760px);
}

.register-card {
  background: $bg-white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(76, 110, 245, 0.15);
  border: 1px solid $border-light;
  animation: slideInUp 0.6s ease-out;
  max-height: inherit;
  overflow-y: auto;
  overscroll-behavior: contain;
}

.logo-section {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-img {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 70px;
  margin: 0 auto 1rem;
  border-radius: 20px;
  background: linear-gradient(135deg, $primary-light-blue 0%, #dbe4ff 100%);
  animation: float 3s ease-in-out infinite;

  .logo-icon {
    width: 34px;
    height: 34px;
    color: $primary-blue;
  }
}

.welcome-text {
  font-size: 0.95rem;
  color: $text-secondary;
  margin: 0;
  font-weight: 500;
}

.register-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;

  &:last-of-type {
    margin-bottom: 1.75rem;
  }
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  color: $text-primary;
  margin-bottom: 0.6rem;
  cursor: default;

  .label-icon {
    width: 16px;
    height: 16px;
    color: $primary-blue;
  }
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;

  .input-icon {
    position: absolute;
    left: 12px;
    width: 18px;
    height: 18px;
    color: $text-secondary;
    pointer-events: none;
    flex-shrink: 0;
  }
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 40px;
  border-radius: 10px;
  border: 2px solid $border-light;
  font-size: 0.9rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background-color: #fafbff;
  color: $text-primary;

  &::placeholder {
    color: #c0c0c0;
  }

  &:focus {
    border-color: $primary-blue;
    background-color: $bg-white;
    box-shadow: 0 0 0 3px $primary-light-blue;
    outline: none;
  }
}

.email-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.email-prefix {
  flex: 1;
}

.email-domain {
  min-width: 120px;
  padding: 0.8rem 0.9rem;
  border-radius: 10px;
  background: $primary-light-blue;
  border: 1px solid #d9e2ff;
  color: $primary-dark-blue;
  font-size: 0.88rem;
  font-weight: 700;
  text-align: center;
}

.field-hint {
  margin: 0.5rem 0 0;
  font-size: 0.82rem;
  color: $text-secondary;
}

.role-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;
}

.role-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.35rem;
  width: 100%;
  border: 2px solid $border-light;
  border-radius: 14px;
  background: #fafbff;
  padding: 1rem;
  transition: all 0.25s ease;
  text-align: left;
  color: $text-primary;

  &:hover {
    transform: translateY(-2px);
    border-color: #cfd9ff;
    box-shadow: 0 10px 24px rgba(76, 110, 245, 0.08);
  }

  &.active {
    border-color: $primary-blue;
    background: $primary-light-blue;
    box-shadow: 0 12px 28px rgba(76, 110, 245, 0.12);
  }
}

.role-icon {
  width: 18px;
  height: 18px;
  color: $primary-blue;
}

.role-title {
  font-size: 0.95rem;
  font-weight: 700;
}

.role-desc {
  font-size: 0.8rem;
  line-height: 1.45;
  color: $text-secondary;
}

.register-btn {
  width: 100%;
  padding: 0.85rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: $bg-white;
  background: linear-gradient(135deg, $primary-blue 0%, $primary-dark-blue 100%);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 20px $primary-blue-shadow;
  letter-spacing: 0.5px;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px $primary-blue-shadow;
    background: linear-gradient(135deg, #5b78ff 0%, #3d58d4 100%);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.8;
    cursor: not-allowed;
  }

  .spinner-border {
    width: 0.9rem;
    height: 0.9rem;
    border-width: 0.2em;
  }
}

.footer-links {
  text-align: center;
  padding-top: 1.25rem;
  border-top: 1px solid $border-light;
}

.footer-text {
  font-size: 0.9rem;
  color: $text-secondary;
  margin-bottom: 0.75rem;
  margin-top: 0;
  font-weight: 500;
}

.footer-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  color: $primary-blue;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;

  &:hover {
    color: $primary-dark-blue;
    transform: translateY(-2px);
  }
}

.decoration {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(76, 110, 245, 0.15) 0%, rgba(76, 110, 245, 0) 70%);
  z-index: -1;
}

.decoration-top {
  width: 200px;
  height: 200px;
  top: -60px;
  right: -80px;
}

.decoration-bottom {
  width: 240px;
  height: 240px;
  bottom: -100px;
  left: -100px;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-6px);
  }
}

@media (max-width: 576px) {
  .register-container {
    padding: 0;
  }

  .register-card {
    padding: 1.5rem;
    border-radius: 18px;
  }

  .email-row {
    flex-direction: column;
    align-items: stretch;
  }

  .email-domain {
    min-width: auto;
  }

  .role-grid {
    grid-template-columns: 1fr;
  }
}
</style>
