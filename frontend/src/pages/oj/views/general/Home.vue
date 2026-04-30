<template>
  <div class="home-container">
    <Banner />
    <div class="content-wrapper">
      <!-- 환영 메시지 -->
      <div class="welcome-section">
        <h1 class="welcome-title">안녕하세요! 👋</h1>
        <p class="welcome-subtitle">재미없는 코딩 재밌게 해봐요..</p>
      </div>

      <!-- 공지사항 카드 -->
      <div class="card-section">
        <div class="section-header">
          <div class="section-title">
            <b-icon icon="chat-dots" class="section-icon"/>
            <span>공지사항</span>
          </div>
          <b-button
            variant="outline-primary"
            size="sm"
            @click="goAnnouncement()"
            class="view-all-btn"
          >
            전체보기
            <b-icon icon="arrow-right" class="ml-2"/>
          </b-button>
        </div>

        <div class="announcement-list">
          <div
            v-for="(announcement, index) in announcements"
            :key="index"
            class="announcement-item"
            @click="goAnnouncement(announcement)"
          >
            <div class="announcement-badge">
              <b-icon icon="pin-fill"></b-icon>
            </div>
            <div class="announcement-content">
              <div class="announcement-title">{{ announcement.title }}</div>
              <div class="announcement-date">{{ getTimeFormat(announcement.create_time, 'MMM D, YYYY') }}</div>
            </div>
            <b-icon icon="chevron-right" class="announcement-arrow"/>
          </div>
        </div>
      </div>

      <!-- 대회 카드 -->
      <div class="card-section">
        <div class="section-header">
          <div class="section-title">
            <b-icon icon="trophy" class="section-icon"/>
            <span>현재/예정된 대회</span>
          </div>
          <b-button
            variant="outline-primary"
            size="sm"
            @click="goContestList()"
            class="view-all-btn"
          >
            전체보기
            <b-icon icon="arrow-right" class="ml-2"/>
          </b-button>
        </div>

        <div class="contest-list">
          <div
            v-for="(contest, index) in contests"
            :key="index"
            class="contest-item"
            @click="goContest(contest)"
          >
            <div class="contest-status-icon">
              <b-icon :icon="contest.status === '0' ? 'hourglass-split' : 'calendar-event'" class="status-icon"/>
            </div>
            <div class="contest-content">
              <div class="contest-title">{{ contest.title }}</div>
              <div class="contest-date">{{ getTimeFormat(contest.start_time, 'MMM D, YYYY') }}</div>
            </div>
            <b-icon icon="chevron-right" class="contest-arrow"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Banner from '@oj/components/Banner.vue'
import api from '@oj/api'
import { mapState, mapGetters } from 'vuex'
import time from '@/utils/time'
import {
  CONTEST_TYPE,
  CONTEST_STATUS
} from '@/utils/constants'

export default {
  name: 'Home',
  components: {
    Banner
  },
  data () {
    return {
      announcements: [],
      contests: []
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      await this.getContestList()
      await this.getAnnouncementList()
    },
    async getAnnouncementList () {
      const res = await api.getAnnouncementList(0, 3)
      this.announcements = res.data.data.results
    },
    async getContestList () {
      const res = await api.getContestList(0, 10)
      let contests = res.data.data.results

      const status = [CONTEST_STATUS.UNDERWAY, CONTEST_STATUS.NOT_START]
      contests = contests.filter(contest => contest.status in status)
      if (contests.length >= 3) {
        this.contests = [contests[0], contests[1], contests[2]]
      } else {
        this.contests = [...contests]
      }
    },
    async goAnnouncement (item) {
      if (item && item.id) {
        await this.$router.push({ name: 'announcement-details', params: { announcementID: item.id } })
      } else {
        await this.$router.push({ name: 'announcement-list' })
      }
    },
    async goContest (item) {
      if (item.contest_type !== CONTEST_TYPE.PUBLIC && !this.isAuthenticated) {
        this.$error('Please login first!')
        await this.$store.dispatch('changeModalStatus', { mode: 'login', visible: true })
      } else {
        this.$router.push({
          name: 'contest-details',
          params: { contestID: item.id }
        })
      }
    },
    async goContestList () {
      await this.$router.push({ name: 'contest-list' })
    },
    getTimeFormat (value, format) {
      return time.utcToLocal(value, format)
    }
  },
  computed: {
    ...mapState({
      contest: (state) => state.contest.contest
    }),
    ...mapGetters([
      'countdown'
    ]),
    ...mapState('account', ['isAuthenticated'])
  }
}
</script>

<style lang="scss" scoped>
  // 색상 변수 - 파란색 테마
  $primary-blue: #4c6ef5;
  $primary-dark-blue: #364fc7;
  $primary-light-blue: #f0f3ff;
  $primary-blue-shadow: rgba(76, 110, 245, 0.2);
  $primary-blue-shadow-light: rgba(76, 110, 245, 0.1);
  $text-primary: #111111;
  $text-secondary: #888888;
  $bg-light: #f5f7fa;
  $bg-white: #ffffff;
  $border-light: #e9ecef;

  * {
    box-sizing: border-box;
  }

  .home-container {
    background: linear-gradient(135deg, #e7f0ff 0%, #d4e5ff 100%);
    min-height: 100vh;
    padding: 2rem 0;
  }

  .content-wrapper {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 1.5rem;
  }

  /* 환영 섹션 */
  .welcome-section {
    margin-bottom: 3rem;
    animation: slideInDown 0.6s ease-out;

    .welcome-title {
      font-size: 2.5rem;
      font-weight: 700;
      color: $text-primary;
      margin: 0 0 0.5rem 0;
      letter-spacing: -0.5px;
    }

    .welcome-subtitle {
      font-size: 1.1rem;
      color: $text-secondary;
      margin: 0;
      font-weight: 500;
    }
  }

  .card-section {
    background: $bg-white;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid $border-light;
    animation: slideInUp 0.6s ease-out;

    &:hover {
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
      transform: translateY(-4px);
    }
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid #f0f2f5;
    gap: 1rem;
  }

  .section-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.3rem;
    font-weight: 700;
    color: $text-primary;
    flex: 1;

    .section-icon {
      width: 28px;
      height: 28px;
      color: $primary-blue;
      transition: all 0.3s ease;
      flex-shrink: 0;
    }

    span {
      white-space: nowrap;
    }
  }

  .view-all-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 0.65rem 1.25rem;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: $primary-blue;
    border: 2px solid $primary-blue;
    background: transparent;
    cursor: pointer;
    white-space: nowrap;

    &:hover {
      background-color: $primary-light-blue;
      border-color: $primary-dark-blue;
      color: $primary-dark-blue;
      box-shadow: 0 4px 12px $primary-blue-shadow;
      transform: translateY(-2px);
    }

    &:active {
      transform: translateY(0);
    }
  }

  /* 공지사항 리스트 */
  .announcement-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .announcement-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem;
    background: #f8fbff;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid #e7f0ff;

    &:hover {
      background: $primary-light-blue;
      border-color: $primary-blue;
      transform: translateX(4px);
      box-shadow: 0 4px 12px $primary-blue-shadow-light;
    }
  }

  .announcement-badge {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, $primary-blue 0%, $primary-dark-blue 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: $bg-white;
    margin-right: 1rem;
    flex-shrink: 0;
    box-shadow: 0 2px 8px $primary-blue-shadow;
    font-size: 1.1rem;
  }

  .announcement-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    min-width: 0;
  }

  .announcement-title {
    font-size: 1rem;
    font-weight: 600;
    color: $text-primary;
    line-height: 1.5;
    word-break: break-word;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .announcement-date {
    font-size: 0.85rem;
    color: $text-secondary;
    font-weight: 500;
  }

  .announcement-arrow {
    width: 20px;
    height: 20px;
    color: #d0d8e8;
    margin-left: 1rem;
    transition: all 0.3s ease;
    flex-shrink: 0;

    .announcement-item:hover & {
      color: $primary-blue;
      transform: translateX(4px);
    }
  }

  /* 대회 리스트 */
  .contest-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .contest-item {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 1.25rem;
    background: #f8fbff;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid #e7f0ff;

    &:hover {
      background: $primary-light-blue;
      border-color: $primary-blue;
      transform: translateX(4px);
      box-shadow: 0 4px 12px $primary-blue-shadow-light;
    }
  }

  .contest-status-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, $primary-blue 0%, $primary-dark-blue 100%);
    border-radius: 12px;
    flex-shrink: 0;
    box-shadow: 0 2px 8px $primary-blue-shadow;

    .status-icon {
      width: 24px;
      height: 24px;
      color: $bg-white;
    }
  }

  .contest-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    min-width: 0;
  }

  .contest-title {
    font-size: 1rem;
    font-weight: 600;
    color: $text-primary;
    line-height: 1.5;
    word-break: break-word;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .contest-date {
    font-size: 0.85rem;
    color: $text-secondary;
    font-weight: 500;
  }

  .contest-arrow {
    width: 20px;
    height: 20px;
    color: #d0d8e8;
    transition: all 0.3s ease;
    flex-shrink: 0;

    .contest-item:hover & {
      color: $primary-blue;
      transform: translateX(4px);
    }
  }

  /* 애니메이션 */
  @keyframes slideInDown {
    from {
      opacity: 0;
      transform: translateY(-30px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
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

  /* 반응형 디자인 */
  @media screen and (max-width: 768px) {
    .home-container {
      padding: 1rem 0;
    }

    .content-wrapper {
      padding: 0 1rem;
    }

    .welcome-section {
      margin-bottom: 2rem;

      .welcome-title {
        font-size: 2rem;
      }

      .welcome-subtitle {
        font-size: 1rem;
      }
    }

    .card-section {
      padding: 1.5rem;
      margin-bottom: 1.5rem;
      border-radius: 14px;
    }

    .section-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
      margin-bottom: 1.5rem;
      padding-bottom: 1rem;
    }

    .section-title {
      font-size: 1.15rem;
    }

    .view-all-btn {
      width: 100%;
      justify-content: center;
      padding: 0.6rem 1rem;
    }

    .announcement-item,
    .contest-item {
      padding: 1rem;
      gap: 1rem;
    }

    .announcement-badge {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      margin-right: 0.75rem;
    }

    .announcement-title,
    .contest-title {
      font-size: 0.95rem;
    }

    .contest-status-icon {
      width: 40px;
      height: 40px;

      .status-icon {
        width: 20px;
        height: 20px;
      }
    }

    .announcement-arrow,
    .contest-arrow {
      width: 18px;
      height: 18px;
    }
  }

  @media screen and (max-width: 480px) {
    .welcome-section {
      .welcome-title {
        font-size: 1.5rem;
      }

      .welcome-subtitle {
        font-size: 0.95rem;
      }
    }

    .card-section {
      padding: 1.25rem;
      margin-bottom: 1.25rem;
    }

    .section-title {
      font-size: 1rem;

      .section-icon {
        width: 24px;
        height: 24px;
      }
    }

    .announcement-item,
    .contest-item {
      padding: 0.75rem;
      gap: 0.75rem;
    }

    .announcement-badge {
      width: 32px;
      height: 32px;
      margin-right: 0.5rem;
    }

    .announcement-title,
    .contest-title {
      font-size: 0.9rem;
    }

    .announcement-date,
    .contest-date {
      font-size: 0.75rem;
    }

    .contest-status-icon {
      width: 36px;
      height: 36px;
    }
  }
</style>
