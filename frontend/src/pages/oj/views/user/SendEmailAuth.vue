<template>
  <div class="email-auth-container">
    <div class="email-auth-wrapper">
      <div class="email-auth-card">
        <div class="logo-section">
          <div class="logo-img">
            <b-icon icon="envelope-paper-fill" class="logo-icon"></b-icon>
          </div>
          <p class="welcome-text">학교 메일로 인증 링크를 보내드릴게요</p>
        </div>

        <template v-if="!successApply">
          <b-form class="email-auth-form">
            <div class="form-group">
              <label class="form-label">
                <b-icon icon="envelope-fill" class="label-icon"/>
                School Email
              </label>
              <div class="email-row">
                <div class="input-wrapper email-prefix">
                  <b-icon icon="at" class="input-icon"/>
                  <b-form-input
                    v-model="formEmailAuth.emailPrefix"
                    placeholder="학번만 입력"
                    maxlength="7"
                    @keydown.enter.native="sendEmail"
                    class="form-input"
                  />
                </div>
                <div class="email-domain">@shindo.hs.kr</div>
              </div>
              <p class="field-hint">{{ fullEmailPreview }}</p>
            </div>

            <div class="form-group">
              <label class="form-label">
                <b-icon icon="shield-check" class="label-icon"/>
                Captcha
              </label>
              <div class="captcha-row">
                <div class="input-wrapper captcha-input-wrap">
                  <b-icon icon="keyboard" class="input-icon"/>
                  <b-form-input
                    v-model="formEmailAuth.captcha"
                    placeholder="캡차 입력"
                    @keydown.enter.native="sendEmail"
                    class="form-input"
                  />
                </div>
                <img
                  class="captcha-img"
                  :src="captchaSrc"
                  alt="captcha"
                  @click="getCaptchaSrc"
                />
              </div>
            </div>

            <b-button
              class="send-btn"
              @click="sendEmail"
              :disabled="btnResetLoading"
            >
              <b-spinner v-if="btnResetLoading" small class="mr-2"></b-spinner>
              <span v-if="btnResetLoading">보내는 중...</span>
              <span v-else>인증 메일 보내기</span>
            </b-button>
          </b-form>
        </template>

        <template v-else>
          <div class="success-box">
            <b-icon icon="check-circle-fill" class="success-icon"></b-icon>
            <p class="success-title">인증 메일을 보냈습니다</p>
            <p class="success-desc">{{ fullEmailPreview }} 주소의 메일함에서 인증 링크를 눌러주세요.</p>
          </div>
        </template>

        <div class="footer-links">
          <a @click="changeModalStatus({ visible: true, mode: 'login' })" class="footer-link">
            <b-icon icon="box-arrow-in-right" class="mr-1"></b-icon>
            로그인으로 돌아가기
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@oj/api'
import { FormMixin } from '@oj/components/mixins'
import { mapActions } from 'vuex'

export default {
  name: 'SendEmailAuth',
  mixins: [FormMixin],
  data () {
    return {
      captchaSrc: '',
      successApply: false,
      btnResetLoading: false,
      formEmailAuth: {
        emailPrefix: '',
        captcha: ''
      }
    }
  },
  computed: {
    fullEmailPreview () {
      if (!this.formEmailAuth.emailPrefix) {
        return '@shindo.hs.kr'
      }
      return `${this.formEmailAuth.emailPrefix}@shindo.hs.kr`
    }
  },
  mounted () {
    this.getCaptchaSrc()
  },
  methods: {
    ...mapActions(['changeModalStatus']),
    async getCaptchaSrc () {
      try {
        const res = await api.getCaptcha()
        this.captchaSrc = res.data
      } catch (err) {
        this.$error('캡차를 불러올 수 없습니다.')
      }
    },
    async sendEmail () {
      if (!this.formEmailAuth.emailPrefix) {
        return this.$error('학번을 입력해주세요.')
      }

      if (!this.formEmailAuth.captcha) {
        return this.$error('캡차를 입력해주세요.')
      }

      this.btnResetLoading = true
      try {
        await api.sendEmailAuth({
          email: `${this.formEmailAuth.emailPrefix}@shindo.hs.kr`,
          captcha: this.formEmailAuth.captcha
        })
        this.successApply = true
      } catch (err) {
        this.formEmailAuth.captcha = ''
        this.getCaptchaSrc()
      } finally {
        this.btnResetLoading = false
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

.email-auth-container {
  background: linear-gradient(135deg, #e7f0ff 0%, #d4e5ff 100%);
  width: 100%;
}

.email-auth-wrapper {
  width: 100%;
  max-width: 420px;
  margin: 0 auto;
}

.email-auth-card {
  background: $bg-white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(76, 110, 245, 0.15);
  border: 1px solid $border-light;
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

.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  color: $text-primary;
  margin-bottom: 0.6rem;

  .label-icon {
    width: 16px;
    height: 16px;
    color: $primary-blue;
  }
}

.input-wrapper {
  position: relative;

  .input-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    width: 18px;
    height: 18px;
    color: $text-secondary;
    pointer-events: none;
  }
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 40px;
  border-radius: 10px;
  border: 2px solid $border-light;
  font-size: 0.9rem;
  background-color: #fafbff;
  color: $text-primary;

  &:focus {
    border-color: $primary-blue;
    background-color: $bg-white;
    box-shadow: 0 0 0 3px $primary-light-blue;
    outline: none;
  }
}

.email-row,
.captcha-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.email-prefix,
.captcha-input-wrap {
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

.captcha-img {
  width: 120px;
  height: 46px;
  object-fit: cover;
  border-radius: 10px;
  border: 1px solid $border-light;
  cursor: pointer;
  background: #f5f7ff;
}

.field-hint {
  margin: 0.5rem 0 0;
  font-size: 0.82rem;
  color: $text-secondary;
}

.send-btn {
  width: 100%;
  padding: 0.85rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: $bg-white;
  background: linear-gradient(135deg, $primary-blue 0%, $primary-dark-blue 100%);
  border: none;
  border-radius: 10px;
  box-shadow: 0 8px 20px $primary-blue-shadow;
}

.success-box {
  text-align: center;
  padding: 1rem 0 0.5rem;
}

.success-icon {
  width: 44px;
  height: 44px;
  color: #2f9e44;
  margin-bottom: 0.75rem;
}

.success-title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: $text-primary;
}

.success-desc {
  font-size: 0.9rem;
  color: $text-secondary;
  line-height: 1.6;
  margin: 0;
}

.footer-links {
  text-align: center;
  padding-top: 1.25rem;
  margin-top: 1.25rem;
  border-top: 1px solid $border-light;
}

.footer-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  color: $primary-blue;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
}

@media (max-width: 576px) {
  .email-auth-card {
    padding: 1.5rem;
    border-radius: 18px;
  }

  .email-row,
  .captcha-row {
    flex-direction: column;
    align-items: stretch;
  }

  .email-domain,
  .captcha-img {
    width: 100%;
  }
}
</style>
