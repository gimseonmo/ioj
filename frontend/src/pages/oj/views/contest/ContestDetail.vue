<template>
  <div class="contest-detail-container">
    <!-- 헤더 섹션 -->
    <div class="contest-header">
      <div class="header-content">
        <div class="header-title-group">
          <h1 class="header-title">{{ contest.title }}</h1>
          <status-badge
            class="header-badge"
            :status_name="contestStatus.name"
            :status_color="contestStatus.color"
            :status_endtime="contest.end_time"
          ></status-badge>
        </div>
        <p class="header-description">{{ makeGroupRequirementInfo(contest) }}</p>
      </div>
    </div>

    <!-- 탭 섹션 -->
    <div class="contest-content">
      <b-tabs
        v-model="tabIndex"
        content-class="tab-content"
        class="contest-tabs"
        pills
      >
        <!-- Top 탭 -->
        <b-tab title="소개" lazy>
          <template #title>
            <b-icon icon="info-circle-fill" class="tab-icon"></b-icon>
            <span>소개</span>
          </template>
          <div class="tab-panel">
            <div class="description-box" v-dompurify-html="contest.description"></div>
          </div>
        </b-tab>

        <!-- Problems 탭 -->
        <b-tab title="문제" lazy>
          <template #title>
            <b-icon icon="file-earmark-text" class="tab-icon"></b-icon>
            <span>문제</span>
          </template>
          <div class="tab-panel">
            <contest-problem-list></contest-problem-list>
          </div>
        </b-tab>

        <!-- Standings 탭 -->
        <b-tab title="순위" lazy>
          <template #title>
            <b-icon icon="trophy-fill" class="tab-icon"></b-icon>
            <span>순위</span>
          </template>
          <div class="tab-panel">
            <contest-ranking></contest-ranking>
          </div>
        </b-tab>

        <!-- Clarifications 탭 -->
        <b-tab title="질문" lazy>
          <template #title>
            <b-icon icon="chat-dots-fill" class="tab-icon"></b-icon>
            <span>질문</span>
          </template>
          <div class="tab-panel">
            <contest-clarification></contest-clarification>
          </div>
        </b-tab>
      </b-tabs>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import api from '@oj/api'
import { mapState, mapGetters, mapActions } from 'vuex'
import { types } from '@/store'
import { CONTEST_STATUS_REVERSE } from '@/utils/constants'
import StatusBadge from '../../components/StatusBadge.vue'
import ContestProblemList from './ContestProblemList.vue'
import ContestRanking from './ContestRanking.vue'
import ContestClarification from './ContestClarification.vue'

export default {
  name: 'ContestDetail',
  components: {
    StatusBadge,
    ContestProblemList,
    ContestRanking,
    ContestClarification
  },
  data () {
    return {
      contestID: '',
      contest: {},
      tabIndex: 0,
      timer: null
    }
  },
  async mounted () {
    this.contestID = this.$route.params.contestID
    this.route_name = this.$route.name
    try {
      const res = await this.$store.dispatch('getContest')
      this.changeDomTitle({ title: res.data.data.title })
      const data = res.data.data
      this.contest = data
      const endTime = moment(data.end_time)
      if (endTime.isAfter(moment(data.now))) {
        this.timer = setInterval(() => {
          this.$store.commit(types.NOW_ADD_1S)
        }, 1000)
      }
    } catch (err) {
      this.$error('경진대회를 불러올 수 없습니다.')
    }
  },
  beforeDestroy () {
    if (this.timer) {
      clearInterval(this.timer)
    }
  },
  methods: {
    ...mapActions(['changeDomTitle']),
    async getContestProblems () {
      try {
        const res = await this.$store.dispatch('getContestProblems')
        const data = res.data.data
        this.contestProblems = data
      } catch (err) {
      }
    },
    async handleRoute (route) {
      await this.$router.push(route)
    },
    async checkPassword () {
      if (this.contestPassword === '') {
        this.$error('Password can\'t be empty')
        return
      }
      this.btnLoading = true
      try {
        await api.checkContestPassword(this.contestID, this.contestPassword)
        this.$success('Succeeded')
        this.$store.commit(types.CONTEST_ACCESS, { access: true })
        this.btnLoading = false
      } catch (err) {
        this.btnLoading = false
      }
    },
    makeGroupRequirementInfo (contest) {
      if (!contest.allowed_groups || contest.allowed_groups.length === 0) {
        return '모든 사용자가 참가할 수 있습니다'
      }
      return '그룹: ' + contest.allowed_groups.map(g => g.name).join(', ')
    }
  },
  computed: {
    ...mapState({
      contest: state => state.contest.contest,
      problems: state => state.contest.contestProblems,
      now: state => state.contest.now
    }),
    ...mapGetters(
      ['contestMenuDisabled', 'contestRuleType', 'contestStatus', 'countdown', 'isContestAdmin',
        'OIContestRealTimePermission', 'passwordFormVisible', 'isAuthenticated', 'contestRuleType', 'OIContestRealTimePermission']
    ),
    contestStatus () {
      return {
        name: CONTEST_STATUS_REVERSE[this.contest.status].name,
        color: CONTEST_STATUS_REVERSE[this.contest.status].color
      }
    }
  },
  watch: {
    '$route' (newVal) {
      this.route_name = newVal.name
      this.contestID = newVal.params.contestID
      this.changeDomTitle({ title: this.contest.title })
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
  $text-light: #666666;
  $bg-white: #ffffff;
  $bg-light: #f8f9fa;
  $border-light: #e9ecef;
  $success-green: #51cf66;
  $warning-yellow: #ffd43b;
  $danger-red: #ff6b6b;

  .contest-detail-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #e7f0ff 0%, #d4e5ff 100%);
    padding: 2rem 0;
  }

  /* 헤더 섹션 */
  .contest-header {
    background: linear-gradient(135deg, $primary-blue 0%, $primary-dark-blue 100%);
    color: $bg-white;
    padding: 3rem 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 24px $primary-blue-shadow;
    animation: slideInDown 0.6s ease-out;
  }

  .header-content {
    max-width: 1200px;
    margin: 0 auto;
  }

  .header-title-group {
    display: flex;
    align-items: flex-start;
    gap: 1.5rem;
    margin-bottom: 1rem;

    @media (max-width: 768px) {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
  }

  .header-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    line-height: 1.2;
    word-break: break-word;

    @media (max-width: 768px) {
      font-size: 1.8rem;
    }

    @media (max-width: 480px) {
      font-size: 1.5rem;
    }
  }

  .header-badge {
    flex-shrink: 0;
    margin-top: 0.5rem;
  }

  .header-description {
    font-size: 1rem;
    opacity: 0.9;
    margin: 0;
    font-weight: 500;

    @media (max-width: 768px) {
      font-size: 0.95rem;
    }

    @media (max-width: 480px) {
      font-size: 0.9rem;
    }
  }

  /* 탭 섹션 */
  .contest-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
  }

  .contest-tabs {
    ::v-deep {
      .nav-pills {
        background: $bg-white;
        border-radius: 12px 12px 0 0;
        padding: 1rem;
        border: 1px solid $border-light;
        border-bottom: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;

        @media (max-width: 768px) {
          padding: 0.75rem 0.5rem;
          gap: 0.25rem;
        }

        .nav-link {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: $text-secondary;
          background: transparent;
          border: 2px solid transparent;
          border-radius: 10px;
          padding: 0.7rem 1.2rem;
          font-weight: 600;
          font-size: 0.95rem;
          cursor: pointer;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

          &:hover {
            background: $primary-light-blue;
            color: $primary-blue;
            border-color: $primary-blue;
            transform: translateY(-2px);
          }

          &.active {
            background: linear-gradient(135deg, $primary-blue 0%, $primary-dark-blue 100%);
            color: $bg-white;
            border-color: $primary-blue;
            box-shadow: 0 4px 12px $primary-blue-shadow;

            .tab-icon {
              transform: scale(1.1);
            }
          }

          .tab-icon {
            width: 18px;
            height: 18px;
            transition: transform 0.3s ease;
          }

          @media (max-width: 768px) {
            padding: 0.6rem 0.9rem;
            font-size: 0.9rem;

            .tab-icon {
              width: 16px;
              height: 16px;
            }

            span {
              display: none;
            }

            &.active span {
              display: inline;
            }
          }

          @media (max-width: 480px) {
            padding: 0.5rem 0.75rem;
            font-size: 0.85rem;

            span {
              display: none;
            }

            &.active span {
              display: inline;
            }
          }
        }
      }

      .tab-content {
        background: $bg-white;
        border: 1px solid $border-light;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        padding: 0;
      }
    }
  }

  .tab-panel {
    padding: 2rem;
    animation: fadeIn 0.4s ease-out;

    @media (max-width: 768px) {
      padding: 1.5rem;
    }

    @media (max-width: 480px) {
      padding: 1rem;
    }
  }

  /* 설명 박스 */
  .description-box {
    padding: 1.5rem;
    background: $bg-light;
    border-radius: 10px;
    border-left: 4px solid $primary-blue;
    line-height: 1.8;
    color: $text-primary;
    font-size: 0.95rem;

    ::v-deep h1,
    ::v-deep h2,
    ::v-deep h3,
    ::v-deep h4,
    ::v-deep h5,
    ::v-deep h6 {
      color: $primary-blue;
      margin-top: 1.5rem;
      margin-bottom: 1rem;
      font-weight: 700;

      &:first-child {
        margin-top: 0;
      }
    }

    ::v-deep p {
      margin-bottom: 1rem;

      &:last-child {
        margin-bottom: 0;
      }
    }

    ::v-deep code {
      background: $bg-white;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      color: $danger-red;
      font-family: 'Courier New', monospace;
      font-size: 0.9rem;
    }

    ::v-deep pre {
      background: $bg-white;
      padding: 1rem;
      border-radius: 8px;
      overflow-x: auto;
      margin: 1rem 0;
      border: 1px solid $border-light;

      code {
        background: transparent;
        padding: 0;
        color: $text-primary;
      }
    }

    ::v-deep ul,
    ::v-deep ol {
      margin-bottom: 1rem;
      padding-left: 2rem;

      li {
        margin-bottom: 0.5rem;
      }
    }

    ::v-deep table {
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0;

      th,
      td {
        padding: 0.75rem;
        border: 1px solid $border-light;
        text-align: left;
      }

      th {
        background: $primary-light-blue;
        color: $primary-blue;
        font-weight: 700;
      }

      tr:nth-child(even) {
        background: $bg-white;
      }

      tr:nth-child(odd) {
        background: rgba(76, 110, 245, 0.02);
      }
    }

    ::v-deep a {
      color: $primary-blue;
      text-decoration: none;
      font-weight: 600;
      transition: all 0.3s ease;

      &:hover {
        color: $primary-dark-blue;
        text-decoration: underline;
      }
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

  @keyframes fadeIn {
    from {
      opacity: 0;
    }

    to {
      opacity: 1;
    }
  }

  /* 반응형 디자인 */
  @media (max-width: 1024px) {
    .contest-header {
      padding: 2rem 1.5rem;
    }

    .contest-content {
      padding: 0 1.5rem;
    }

    .header-title {
      font-size: 2rem;
    }

    .header-description {
      font-size: 0.95rem;
    }
  }

  @media (max-width: 768px) {
    .contest-detail-container {
      padding: 1rem 0;
    }

    .contest-header {
      padding: 1.5rem 1rem;
      margin-bottom: 1.5rem;
    }

    .contest-content {
      padding: 0 1rem;
    }

    .header-title {
      font-size: 1.5rem;
    }

    .header-description {
      font-size: 0.9rem;
    }

    .tab-panel {
      padding: 1.25rem;
    }

    .description-box {
      padding: 1rem;
      font-size: 0.9rem;
    }
  }

  @media (max-width: 480px) {
    .contest-detail-container {
      padding: 0.75rem 0;
    }

    .contest-header {
      padding: 1.25rem 0.75rem;
      margin-bottom: 1rem;
    }

    .contest-content {
      padding: 0 0.75rem;
    }

    .header-title {
      font-size: 1.25rem;
    }

    .header-description {
      font-size: 0.85rem;
    }

    .tab-panel {
      padding: 0.75rem;
    }

    .description-box {
      padding: 0.75rem;
      font-size: 0.85rem;
      line-height: 1.6;

      ::v-deep h1,
      ::v-deep h2,
      ::v-deep h3 {
        font-size: 1.1rem;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
      }

      ::v-deep code {
        font-size: 0.8rem;
      }

      ::v-deep pre {
        padding: 0.75rem;
        font-size: 0.8rem;
      }

      ::v-deep table {
        font-size: 0.8rem;

        th,
        td {
          padding: 0.5rem;
        }
      }
    }

    ::v-deep .nav-pills {
      flex-direction: column;

      .nav-link {
        width: 100%;
        justify-content: center;
      }
    }
  }
</style>
