<template>
  <nav class="header-nav">
    <!-- 로고 -->
    <div class="header-logo">
      <a href="/" class="logo-link">
        <img
          src="@/assets/logos/logo.png"
          class="logo-image"
          alt="Sindo High School"
        />
      </a>
    </div>

    <!-- 네비게이션 메뉴 -->
    <div class="nav-menu">
      <a href="/" class="nav-item">
        <b-icon icon="house" class="nav-icon"></b-icon>
        <span>홈</span>
      </a>
      <a href="/problem" class="nav-item">
        <b-icon icon="file-text" class="nav-icon"></b-icon>
        <span>문제</span>
      </a>
      <a href="/announcement" class="nav-item">
        <b-icon icon="bell" class="nav-icon"></b-icon>
        <span>공지</span>
      </a>

      <a href="/contest" class="nav-item">
        <b-icon icon="trophy" class="nav-icon"></b-icon>
        <span>대회</span>
      </a>
    </div>

    <!-- 사용자 드롭다운 -->
    <div class="header-user">
      <dropdown placement="right" width="w-48" id="dropdown">
        <template v-slot:button>
          <button class="user-button">
            <b-icon icon="person-circle" font-scale="1.5" class="user-icon"></b-icon>
          </button>
        </template>

        <template v-slot:content v-if="!isAuthenticated">
          <button
            @click="handleBtnClick('login')"
            class="dropdown-item"
          >
            <b-icon icon="box-arrow-in-right" class="dropdown-icon"></b-icon>
            <span>로그인</span>
          </button>
          <button
            @click="handleBtnClick('register')"
            class="dropdown-item"
          >
            <b-icon icon="person-plus" class="dropdown-icon"></b-icon>
            <span>회원가입</span>
          </button>
        </template>

        <template v-slot:content v-else>
          <div class="dropdown-user-info">
            <div class="user-name">{{ user.username }}</div>
            <div class="user-email">{{ user.email }}</div>
          </div>
          <div class="dropdown-divider"></div>
          <button
            v-if="isAdminRole"
            @click="goManagement()"
            class="dropdown-item"
          >
            <b-icon icon="sliders" class="dropdown-icon"></b-icon>
            <span>관리자 페이지</span>
          </button>
          <a
            href="/#"
            class="dropdown-item"
          >
            <b-icon icon="gear" class="dropdown-icon"></b-icon>
            <span>설정</span>
          </a>
          <a
            href="/logout"
            class="dropdown-item logout-item"
          >
            <b-icon icon="box-arrow-right" class="dropdown-icon"></b-icon>
            <span>로그아웃</span>
          </a>
        </template>
      </dropdown>
    </div>

    <!-- 모달 -->
    <modal v-if="modalVisible" v-on:close="modalVisible = false">
      <component
        :is="modalStatus.mode"
        v-if="modalVisible"
      />
    </modal>
  </nav>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import Dropdown from './Dropdown.vue'
import Modal from './Modal.vue'
import register from '@oj/views/user/Register'
import login from '@oj/views/user/Login'
import ApplyResetPassword from '@oj/views/user/ApplyResetPassword'
import DeleteAccount from '@oj/views/user/DeleteAccount'
import SendEmailAuth from '@oj/views/user/SendEmailAuth'

export default {
  components: {
    Dropdown,
    Modal,
    login,
    register,
    ApplyResetPassword,
    DeleteAccount,
    SendEmailAuth
  },
  mounted () {
    this.getProfile()
  },
  methods: {
    ...mapActions(['getProfile', 'changeModalStatus']),
    handleBtnClick (mode) {
      this.changeModalStatus({
        visible: true,
        mode: mode
      })
    },
    goManagement () {
      if (!this.isSuperAdmin) {
        window.open('/professor/')
      } else {
        window.open('/admin/')
      }
    }
  },
  computed: {
    ...mapGetters(['website', 'modalStatus', 'user', 'isAuthenticated', 'isAdminRole', 'isSuperAdmin']),
    modalVisible: {
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
  $text-primary: #111111;
  $text-secondary: #888888;
  $bg-white: #ffffff;
  $border-light: #e9ecef;

  .header-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: $bg-white;
    border-bottom: 1px solid $border-light;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    position: sticky;
    top: 0;
    z-index: 50;
    gap: 2rem;

    @media (max-width: 768px) {
      padding: 0.75rem 1rem;
      gap: 1rem;
    }
  }

  /* 로고 */
  .header-logo {
    flex-shrink: 0;

    .logo-link {
      display: inline-flex;
      align-items: center;
      transition: transform 0.3s ease;

      &:hover {
        transform: scale(1.05);
      }
    }

    .logo-image {
      height: 40px;
      width: auto;

      @media (max-width: 768px) {
        height: 32px;
      }
    }
  }

  /* 네비게이션 메뉴 */
  .nav-menu {
    display: flex;
    gap: 1.5rem;
    flex: 1;
    justify-content: center;
    align-items: center;

    @media (max-width: 1024px) {
      gap: 1rem;
    }

    @media (max-width: 768px) {
      gap: 0.5rem;
      flex: 0;
    }

    @media (max-width: 480px) {
      display: none;
    }
  }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.95rem;
    color: $text-primary;
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid transparent;
    white-space: nowrap;

    &:hover {
      background: $primary-light-blue;
      border-color: $primary-blue;
      color: $primary-blue;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(76, 110, 245, 0.15);

      .nav-icon {
        color: $primary-blue;
      }
    }

    &:active {
      transform: translateY(0);
    }
  }

  .nav-icon {
    width: 18px;
    height: 18px;
    color: $text-secondary;
    transition: all 0.3s ease;
  }

  /* 사용자 섹션 */
  .header-user {
    flex-shrink: 0;
  }

  .user-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    border: 2px solid $border-light;
    background: $bg-white;
    cursor: pointer;
    transition: all 0.3s ease;
    color: $text-primary;

    &:hover {
      border-color: $primary-blue;
      background: $primary-light-blue;
      box-shadow: 0 4px 12px rgba(76, 110, 245, 0.15);
      transform: translateY(-2px);

      .user-icon {
        color: $primary-blue;
      }
    }

    &:active {
      transform: translateY(0);
    }
  }

  .user-icon {
    width: 24px;
    height: 24px;
    color: $text-secondary;
    transition: all 0.3s ease;
  }

  /* 드롭다운 스타일 */
  ::v-deep .dropdown-content {
    background: $bg-white;
    border-radius: 12px;
    border: 1px solid $border-light;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    padding: 0.5rem;
    min-width: 200px;
  }

  .dropdown-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    width: 100%;
    padding: 0.75rem 1rem;
    border: none;
    background: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 500;
    color: $text-primary;
    text-align: left;
    transition: all 0.3s ease;

    &:hover {
      background: $primary-light-blue;
      color: $primary-blue;

      .dropdown-icon {
        color: $primary-blue;
        transform: translateX(4px);
      }
    }

    &.logout-item {
      color: #ff6b6b;

      &:hover {
        background: #ffe0e0;
        color: #ff6b6b;

        .dropdown-icon {
          color: #ff6b6b;
        }
      }
    }
  }

  .dropdown-icon {
    width: 18px;
    height: 18px;
    color: $text-secondary;
    transition: all 0.3s ease;
    flex-shrink: 0;
  }

  .dropdown-user-info {
    padding: 1rem;
    border-bottom: 1px solid $border-light;
    margin-bottom: 0.5rem;

    .user-name {
      font-weight: 700;
      color: $text-primary;
      font-size: 1rem;
      margin-bottom: 0.25rem;
    }

    .user-email {
      font-size: 0.85rem;
      color: $text-secondary;
    }
  }

  .dropdown-divider {
    height: 1px;
    background: $border-light;
    margin: 0.5rem 0;
  }

  /* 반응형 디자인 */
  @media (max-width: 1024px) {
    .header-nav {
      gap: 1rem;
    }

    .nav-menu {
      gap: 0.75rem;
    }

    .nav-item {
      padding: 0.65rem 0.85rem;
      font-size: 0.9rem;

      span {
        display: none;

        @media (min-width: 768px) {
          display: inline;
        }
      }
    }
  }

  @media (max-width: 768px) {
    .header-nav {
      padding: 0.75rem 1rem;
    }

    .nav-menu {
      display: none;
    }

    .user-button {
      width: 40px;
      height: 40px;
    }
  }
</style>
