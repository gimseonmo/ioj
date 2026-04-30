<template>
  <div class="login-container">
    <div class="login-wrapper">
      <div class="login-card">
        <!-- 로고 섹션 -->
        <div class="logo-section">
          <div class="logo-img">
            <img src="@/assets/logos/logo.svg" alt="SKKU Coding Platform"/>
          </div>
          <p class="welcome-text">환영합니다! 로그인하세요</p>
        </div>

        <!-- 폼 섹션 -->
        <b-form @on-enter="handleLogin" ref="formLogin" :model="formLogin" class="login-form">
          <div class="form-group">
            <label class="form-label">
              <b-icon icon="person-fill" class="label-icon"/>
              Student ID
            </label>
            <div class="input-wrapper">
              <b-icon icon="person" class="input-icon"/>
              <b-form-input
                v-model="formLogin.username"
                placeholder="학번을 입력하세요"
                @keydown.enter.native="handleLogin"
                class="form-input"
              />
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
                v-model="formLogin.password"
                placeholder="비밀번호를 입력하세요"
                @keydown.enter.native="handleLogin"
                class="form-input"
              />
            </div>
          </div>

          <!-- 로그인 버튼 -->
          <b-button
            class="login-btn"
            @click="handleLogin"
            :disabled="btnLoginLoading"
          >
            <b-spinner v-if="btnLoginLoading" small class="mr-2"></b-spinner>
            <span v-if="btnLoginLoading">로그인 중...</span>
            <span v-else>로그인</span>
          </b-button>
        </b-form>

        <!-- 하단 링크 -->
        <div class="footer-links">
          <a v-if="website.allow_register" @click.stop="handleBtnClick('SendEmailAuth')" class="footer-link">
            <b-icon icon="person-plus" class="mr-2"/>
            회원가입
          </a>
        </div>
      </div>

      <!-- 백그라운드 데코레이션 -->
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
  mixins: [FormMixin],
  data () {
    return {
      btnLoginLoading: false,
      formLogin: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    ...mapActions(['changeModalStatus', 'getProfile']),
    handleBtnClick (mode) {
      this.changeModalStatus({
        mode,
        visible: true
      })
    },
    async handleLogin () {
      this.btnLoginLoading = true
      const formData = Object.assign({}, this.formLogin)
      try {
        await api.login(formData)
        this.btnLoginLoading = false
        this.changeModalStatus({ visible: false })
        this.getProfile()
        this.$success('Welcome back!')
      } catch (err) {
        this.btnLoginLoading = false
      }
    }
  },
  computed: {
    ...mapGetters(['website', 'modalStatus']),
    visible: {
      get () {
        return this.modalStatus.visible
      },
      set (value) {
        this.changeModalStatus({ visible: value })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  // 색상 변수
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

  .login-container {
    background: linear-gradient(135deg, #e7f0ff 0%, #d4e5ff 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    position: relative;
    overflow: hidden;
  }

  .login-wrapper {
    width: 100%;
    max-width: 380px;
    position: relative;
    z-index: 1;
  }

  .login-card {
    background: $bg-white;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 20px 60px rgba(76, 110, 245, 0.15);
    border: 1px solid $border-light;
    animation: slideInUp 0.6s ease-out;
  }

  /* 로고 섹션 */
  .logo-section {
    text-align: center;
    margin-bottom: 2rem;
  }

  .logo-img {
    display: block;
    width: 70px;
    height: 70px;
    margin: 0 auto 1rem;
    animation: float 3s ease-in-out infinite;

    img {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
  }

  .welcome-text {
    font-size: 0.95rem;
    color: $text-secondary;
    margin: 0;
    font-weight: 500;
  }

  /* 폼 섹션 */
  .login-form {
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

    .form-input {
      width: 100%;
      padding: 0.75rem 1rem 0.75rem 40px;
      border-radius: 10px;
      border: 2px solid $border-light;
      font-size: 0.9rem;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      background-color: #fafbff;

      &::placeholder {
        color: #c0c0c0;
      }

      &:focus {
        border-color: $primary-blue;
        background-color: $bg-white;
        box-shadow: 0 0 0 3px $primary-light-blue;
        outline: none;
      }

      &:-webkit-autofill {
        -webkit-box-shadow: 0 0 0 30px $bg-white inset !important;
        -webkit-text-fill-color: $text-primary !important;
      }
    }
  }

  /* 로그인 버튼 */
  .login-btn {
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

  /* 하단 링크 */
  .footer-links {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.2rem;
    padding-top: 1.25rem;
    border-top: 1px solid $border-light;
  }

  .footer-link {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 0.85rem;
    color: $primary-blue;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;

    &:hover {
      color: $primary-dark-blue;
      transform: translateY(-2px);

      ::v-deep .bi {
        transform: scale(1.1);
      }
    }

    ::v-deep .bi {
      width: 15px;
      height: 15px;
      transition: transform 0.3s ease;
    }
  }

  .link-divider {
    width: 1px;
    height: 16px;
    background: $border-light;
  }

  /* 백그라운드 데코레이션 */
  .decoration {
    position: absolute;
    border-radius: 50%;
    opacity: 0.1;
    pointer-events: none;
  }

  .decoration-top {
    width: 300px;
    height: 300px;
    background: $primary-blue;
    top: -100px;
    left: -100px;
    animation: float 6s ease-in-out infinite;
  }

  .decoration-bottom {
    width: 250px;
    height: 250px;
    background: $primary-blue;
    bottom: -80px;
    right: -80px;
    animation: float 8s ease-in-out infinite reverse;
  }

  /* 애니메이션 */
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
      transform: translateY(-20px);
    }
  }

  /* 반응형 디자인 */
  @media (max-width: 768px) {
    .login-container {
      padding: 1.5rem;
    }

    .login-card {
      padding: 2rem;
      border-radius: 16px;
    }

    .logo-img {
      width: 65px;
      height: 65px;
      margin-bottom: 0.8rem;
    }

    .form-group {
      margin-bottom: 1.1rem;

      &:last-of-type {
        margin-bottom: 1.5rem;
      }
    }

    .input-wrapper .form-input {
      padding: 0.7rem 1rem 0.7rem 38px;
      font-size: 0.85rem;
    }

    .login-btn {
      padding: 0.8rem 1.5rem;
      font-size: 0.9rem;
    }

    .footer-links {
      gap: 1rem;
      padding-top: 1rem;
    }

    .footer-link {
      font-size: 0.8rem;
    }

    .decoration-top {
      width: 200px;
      height: 200px;
      top: -80px;
      left: -80px;
    }

    .decoration-bottom {
      width: 180px;
      height: 180px;
      bottom: -60px;
      right: -60px;
    }
  }

  @media (max-width: 480px) {
    .login-container {
      padding: 1rem;
    }

    .login-card {
      padding: 1.5rem;
      border-radius: 14px;
    }

    .logo-img {
      width: 60px;
      height: 60px;
      margin-bottom: 0.75rem;
    }

    .welcome-text {
      font-size: 0.9rem;
    }

    .form-group {
      margin-bottom: 1rem;

      &:last-of-type {
        margin-bottom: 1.25rem;
      }
    }

    .form-label {
      font-size: 0.85rem;
    }

    .input-wrapper .form-input {
      padding: 0.65rem 0.9rem 0.65rem 36px;
      font-size: 0.85rem;
    }

    .login-btn {
      padding: 0.75rem 1rem;
      font-size: 0.9rem;
    }

    .footer-links {
      flex-direction: column;
      gap: 0.8rem;
      padding-top: 1rem;
    }

    .link-divider {
      width: 20px;
      height: 1px;
    }

    .footer-link {
      font-size: 0.8rem;
    }

    .decoration-top,
    .decoration-bottom {
      display: none;
    }
  }
</style>
