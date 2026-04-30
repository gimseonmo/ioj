<template>
  <div>
    <page-top>
      <template #title>
        <span class="title-white">🏆 INGENIOUS </span>
        <span class="title-gold">CONTEST 🏅</span>
      </template>
      <template #description>
        최고의 프로그래밍 경진대회에 참가하세요!
      </template>
    </page-top>

    <div class="contest-list-container">
      <!-- Active Contests -->
      <div v-if="contestsUnderway.length || contestsUnderwayNoPermission.length" class="contests-section">
        <div class="section-header">
          <b-icon icon="play-circle-fill" class="section-icon"></b-icon>
          <h2 class="section-title">진행 중인 경진대회</h2>
          <span class="contest-count">{{ contestsUnderway.length + contestsUnderwayNoPermission.length }}</span>
        </div>

        <div class="contests-grid">
          <div
            v-for="(contest, index) in contestsUnderway"
            :key="'unp' + index"
            class="contest-card contest-card-active"
            @click="goContest(contest)"
          >
            <div class="card-header">
              <div class="card-badge badge-active">진행 중</div>
              <div class="card-participants">
                <b-icon icon="people-fill" class="icon-small"></b-icon>
                {{ contest.participants_count }}
              </div>
            </div>

            <div class="card-content">
              <h3 class="card-title">{{ contest.title }}</h3>
              <p class="card-subtitle">{{ makeGroupRequirementInfo(contest) }}</p>
            </div>

            <div class="card-footer">
              <span class="time-info">
                <b-icon icon="clock-history" class="icon-small"></b-icon>
                {{ contest.startedTimeFromNow }}
              </span>
              <div class="card-action">
                <b-icon icon="arrow-right" class="action-icon"></b-icon>
              </div>
            </div>

            <div class="card-overlay"></div>
          </div>

          <div
            v-for="(contest, index) in contestsUnderwayNoPermission"
            :key="'unn' + index"
            class="contest-card contest-card-locked"
            @click="showContestInformationModal(contest)"
          >
            <div class="card-header">
              <div class="card-badge badge-locked">제한됨</div>
              <div class="card-participants">
                <b-icon icon="people-fill" class="icon-small"></b-icon>
                {{ contest.participants_count }}
              </div>
            </div>

            <div class="card-content">
              <h3 class="card-title">{{ contest.title }}</h3>
              <p class="card-subtitle">{{ makeGroupRequirementInfo(contest) }}</p>
            </div>

            <div class="card-footer">
              <span class="time-info">
                <b-icon icon="clock-history" class="icon-small"></b-icon>
                {{ contest.startedTimeFromNow }}
              </span>
              <div class="card-action">
                <b-icon icon="zoom-in" class="action-icon"></b-icon>
              </div>
            </div>

            <div class="card-overlay"></div>
          </div>
        </div>

        <b-button
          v-if="contestsUnderwayRendered < contestsUnderwayTotal"
          @click="loadMoreContests(CONTEST_STATUS.UNDERWAY)"
          class="load-more-btn"
        >
          더보기
        </b-button>
      </div>

      <!-- Upcoming Contests -->
      <div v-if="contestsUpcoming.length || contestsUpcomingNoPermission.length" class="contests-section">
        <div class="section-header">
          <b-icon icon="calendar-event" class="section-icon"></b-icon>
          <h2 class="section-title">예정된 경진대회</h2>
          <span class="contest-count">{{ contestsUpcoming.length + contestsUpcomingNoPermission.length }}</span>
        </div>

        <div class="contests-grid">
          <div
            v-for="(contest, index) in contestsUpcoming"
            :key="'upp' + index"
            class="contest-card contest-card-upcoming"
            @click="showContestInformationModal(contest)"
          >
            <div class="card-header">
              <div class="card-badge badge-upcoming">예정</div>
              <div class="card-participants">
                <b-icon icon="people-fill" class="icon-small"></b-icon>
                {{ contest.participants_count }}
              </div>
            </div>

            <div class="card-content">
              <h3 class="card-title">{{ contest.title }}</h3>
              <p class="card-subtitle">{{ makeGroupRequirementInfo(contest) }}</p>
            </div>

            <div class="card-footer">
              <span class="time-info">
                <b-icon icon="hourglass-start" class="icon-small"></b-icon>
                {{ contest.remainTime }}
              </span>
              <div class="card-action">
                <b-icon icon="zoom-in" class="action-icon"></b-icon>
              </div>
            </div>

            <div class="card-overlay"></div>
          </div>

          <div
            v-for="(contest, index) in contestsUpcomingNoPermission"
            :key="'upn' + index"
            class="contest-card contest-card-locked"
            @click="showContestInformationModal(contest)"
          >
            <div class="card-header">
              <div class="card-badge badge-locked">제한됨</div>
              <div class="card-participants">
                <b-icon icon="people-fill" class="icon-small"></b-icon>
                {{ contest.participants_count }}
              </div>
            </div>

            <div class="card-content">
              <h3 class="card-title">{{ contest.title }}</h3>
              <p class="card-subtitle">{{ makeGroupRequirementInfo(contest) }}</p>
            </div>

            <div class="card-footer">
              <span class="time-info">
                <b-icon icon="hourglass-start" class="icon-small"></b-icon>
                {{ contest.remainTime }}
              </span>
              <div class="card-action">
                <b-icon icon="zoom-in" class="action-icon"></b-icon>
              </div>
            </div>

            <div class="card-overlay"></div>
          </div>
        </div>

        <b-button
          v-if="contestsUpcomingRendered < contestsUpcomingTotal"
          @click="loadMoreContests(CONTEST_STATUS.NOT_START)"
          class="load-more-btn"
        >
          더보기
        </b-button>
      </div>

      <!-- Finished Contests -->
      <div class="contests-section">
        <div class="section-header" @click="showFinishedContests = !showFinishedContests" style="cursor: pointer;">
          <b-icon icon="check-circle-fill" class="section-icon"></b-icon>
          <h2 class="section-title">종료된 경진대회</h2>
          <span class="contest-count">{{ contestsFinishedTotal }}</span>
          <b-icon
            :icon="showFinishedContests ? 'chevron-up' : 'chevron-down'"
            class="toggle-icon"
          ></b-icon>
        </div>

        <div v-show="showFinishedContests" class="contests-grid">
          <div
            v-for="(contest, index) in contestsFinished"
            :key="'fi' + index"
            class="contest-card contest-card-finished"
            @click="goContest(contest)"
          >
            <div class="card-header">
              <div class="card-badge badge-finished">종료</div>
              <div class="card-participants">
                <b-icon icon="people-fill" class="icon-small"></b-icon>
                {{ contest.participants_count }}
              </div>
            </div>

            <div class="card-content">
              <h3 class="card-title">{{ contest.title }}</h3>
              <p class="card-subtitle">{{ makeGroupRequirementInfo(contest) }}</p>
            </div>

            <div class="card-footer">
              <span class="time-info">
                <b-icon icon="calendar-check" class="icon-small"></b-icon>
                {{ contest.finishedTimeFromNow }}
              </span>
              <div class="card-action">
                <b-icon icon="arrow-right" class="action-icon"></b-icon>
              </div>
            </div>

            <div class="card-overlay"></div>
          </div>
        </div>

        <b-pagination
          v-show="showFinishedContests"
          v-model="currentPage"
          :per-page="perPage"
          align="center"
          :total-rows="contestsFinishedTotal"
          class="pagination-custom"
        />
      </div>
    </div>

    <!-- Contest Information Modal -->
    <b-modal
      id="modal-contest-information"
      size="xl"
      centered
      class="contest-modal"
    >
      <template #modal-header>
        <h5 class="modal-title">경진대회 정보</h5>
        <b-button variant="link" @click="$bvModal.hide('modal-contest-information')">
          <b-icon icon="x-lg"></b-icon>
        </b-button>
      </template>

      <contest-information
        :title="contestInformation.title"
        :requirements="contestInformation.requirements"
        :constraints="contestInformation.constraints"
        :scoring="contestInformation.scoring"
        :prizes="contestInformation.prizes"
        :description="contestInformation.description"
      >
      </contest-information>

      <template #modal-footer>
        <b-button variant="secondary" @click="$bvModal.hide('modal-contest-information')">
          닫기
        </b-button>
        <b-button variant="primary" @click="goContest(contestInformation)">
          경진대회 입장
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
// 스크립트는 기존과 동일하게 유지
import api from '@oj/api'
import { mapGetters, mapActions } from 'vuex'
import utils from '@/utils/utils'
import time from '@/utils/time'
import { CONTEST_STATUS_REVERSE, CONTEST_TYPE, CONTEST_STATUS } from '@/utils/constants'
import PageTop from '@oj/components/PageTop.vue'
import ContestInformation from '@oj/components/ContestInformation.vue'
import store from '@/store'
import moment from 'moment'

export default {
  name: 'ContestList',
  async beforeRouteEnter (to, from, next) {
    try {
      const res = await api.getContestList(0, 10, {
        status: CONTEST_STATUS.UNDERWAY
      })
      const res2 = await api.getContestList(0, 10, {
        status: CONTEST_STATUS.NOT_START
      })
      const res3 = await api.getContestList(0, 20, {
        status: CONTEST_STATUS.ENDED
      })
      next((vm) => {
        vm.contestsUnderway = res.data.data.results
        vm.contestsUnderwayRendered = 10
        vm.contestsUnderwayTotal = res.data.data.total

        vm.contestsUpcoming = res2.data.data.results
        vm.contestsUpcomingRendered = 10
        vm.contestsUpcomingTotal = res2.data.data.total

        vm.contestsFinished = res3.data.data.results
        vm.contestsFinishedTotal = res3.data.data.total
      })
    } catch (err) {
      next()
    }
  },
  async mounted () {
    if (this.isAuthenticated) {
      this.filterWithGroupPermission()
    }
    this.calculateTimeDiff()
    setInterval(() => {
      this.calculateTimeDiff()
    }, 10000)
  },
  components: {
    ContestInformation,
    PageTop
  },
  data () {
    return {
      showCannotParticipate: false,
      showFinishedContests: false,
      CONTEST_STATUS: CONTEST_STATUS,
      route_name: '',
      query: {
        status: '',
        keyword: '',
        rule_type: ''
      },
      rows: '',
      contestsUnderway: [],
      contestsUnderwayNoPermission: [],
      contestsUnderwayRendered: 0,
      contestsUnderwayTotal: 0,

      contestsUpcoming: [],
      contestsUpcomingNoPermission: [],
      contestsUpcomingRendered: 0,
      contestsUpcomingTotal: 0,

      contestsFinished: [],
      contestsFinishedNoPermission: [],
      contestsFinishedTotal: 0,
      perPage: 20,
      currentPage: 1,

      contestInformation: {},
      CONTEST_STATUS_REVERSE: CONTEST_STATUS_REVERSE,
      cur_contest_id: '',
      contestListFields: [
        {
          label: 'Title',
          key: 'title'
        },
        {
          label: 'Start time',
          key: 'start_time'
        },
        {
          label: 'Duration',
          key: 'duration'
        },
        {
          label: 'Status',
          key: 'status'
        }
      ]
    }
  },
  methods: {
    ...mapActions(['changeDomTitle', 'getGroupList']),
    async handleRoute (route) {
      await this.$router.push(route)
    },
    async init () {
      const route = this.$route.query
      this.query.status = route.status || ''
      this.query.rule_type = route.rule_type || ''
      this.query.keyword = route.keyword || ''
      this.page = parseInt(route.page) || 1
      await this.getContestList()
      await this.filterWithGroupPermission()
    },
    async getContestList () {
      try {
        const res = await api.getContestList(0, 10, {
          status: CONTEST_STATUS.UNDERWAY
        })
        const res2 = await api.getContestList(0, 10, {
          status: CONTEST_STATUS.NOT_START
        })
        const res3 = await api.getContestList(0, 20, {
          status: CONTEST_STATUS.ENDED
        })
        this.contestsUnderway = res.data.data.results
        this.contestsUnderwayRendered = 10
        this.contestsUnderwayTotal = res.data.data.total

        this.contestsUpcoming = res2.data.data.results
        this.contestsUpcomingRendered = 10
        this.contestsUpcomingTotal = res2.data.data.total

        this.contestsFinished = res3.data.data.results
        this.contestsFinishedTotal = res3.data.data.total
      } catch (err) {
      }
    },
    async currentChange (page) {
      this.currentPage = page
      const res = await api.getContestList(20 * (page - 1), 20, {
        status: CONTEST_STATUS.ENDED
      })
      this.contestsFinished = res.data.data.results
      this.calculateTimeDiff()
    },
    async filterWithGroupPermission () {
      await store.dispatch('getGroupList')
      this.group_as_member = [...this.adminGroups, ...this.groups]
      function partition (array, filter) {
        const pass = []
        const fail = []
        array.forEach((e, idx, arr) => (filter(e, idx, arr) ? pass : fail).push(e))
        return [pass, fail]
      }
      const [a, b] = partition(this.contestsUnderway, contest => {
        if (!contest.allowed_groups.length) {
          return true
        }
        for (const allowedGroup of contest.allowed_groups) {
          if (allowedGroup.id in this.group_as_member) {
            return true
          }
        }
        return false
      })
      this.contestsUnderway = a
      this.contestsUnderwayNoPermission = b

      const [c, d] = partition(this.contestsUpcoming, contest => {
        if (!contest.allowed_groups.length) {
          return true
        }
        for (const allowedGroup of contest.allowed_groups) {
          if (allowedGroup.id in this.group_as_member) {
            return true
          }
        }
        return false
      })
      this.contestsUpcoming = c
      this.contestsUpcomingNoPermission = d
    },
    async loadMoreContests (status) {
      if (status === CONTEST_STATUS.UNDERWAY) {
        const res = await api.getContestList(this.contestsUnderwayRendered, 10, {
          status: CONTEST_STATUS.UNDERWAY
        })
        this.contestsUnderwayRendered += 10
        this.contestsUnderway = this.contestsUnderway.concat(res.data.data.results)
      } else if (status === CONTEST_STATUS.NOT_START) {
        const res = await api.getContestList(this.contestsUpcoming, 10, {
          status: CONTEST_STATUS.ENDED
        })
        this.contestsUpcomingRendered += 10
        this.contestsUpcoming = this.contestsUpcoming.concat(res.data.data.results)
      }
    },
    async changeRoute () {
      const query = Object.assign({}, this.query)
      query.page = this.page
      await this.$router.push({
        name: 'contest-list',
        query: utils.filterEmptyValue(query)
      })
    },
    async goContest (item) {
      this.cur_contest_id = item.id
      if (!this.isAuthenticated) {
        this.$error('Please login first!')
        await this.$store.dispatch('changeModalStatus', { mode: 'login', visible: true })
      } else {
        if (item.contest_type === CONTEST_TYPE.PRIVATE && !this.isContestAdmin) {
          this.$error('This contest is locked')
        } else {
          await this.$router.push({ name: 'contest-details', params: { contestID: item.id } })
        }
      }
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-MM-DD HH:mm')
    },
    getDuration (startTime, endTime) {
      return time.duration(startTime, endTime)
    },
    contestStatus (value) {
      return {
        name: CONTEST_STATUS_REVERSE[value].name,
        color: CONTEST_STATUS_REVERSE[value].color
      }
    },
    showContestInformationModal (contest) {
      this.contestInformation = contest
      this.$bvModal.show('modal-contest-information')
    },
    makeGroupRequirementInfo (contest) {
      return 'For ' + (contest.allowed_groups.map(g => g.name).join(', ') || 'All Groups')
    },
    calculateTimeDiff () {
      for (const contest of this.contestsUpcoming) {
        this.$set(contest, 'remainTime', moment().to(moment(contest.start_time)))
      }
      for (const contest of this.contestsUpcomingNoPermission) {
        this.$set(contest, 'remainTime', moment().to(moment(contest.start_time)))
      }
      for (const contest of this.contestsFinished) {
        this.$set(contest, 'finishedTimeFromNow', moment(contest.end_time).fromNow())
      }
      for (const contest of this.contestsUnderway) {
        this.$set(contest, 'startedTimeFromNow', moment(contest.start_time).fromNow())
      }
      for (const contest of this.contestsUnderwayNoPermission) {
        this.$set(contest, 'startedTimeFromNow', moment(contest.start_time).fromNow())
      }
    }
  },
  computed: {
    ...mapGetters(
      ['contestMenuDisabled', 'countdown', 'isContestAdmin',
        'OIContestRealTimePermission', 'passwordFormVisible', 'isAuthenticated',
        'groups', 'adminGroups', 'otherGroups']
    ),
    updateCurrentPage () {
      return this.currentChange(this.currentPage)
    }
  },
  watch: {
    async '$route' (newVal, oldVal) {
      if (newVal !== oldVal) {
        await this.init()
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
  $text-light: #666666;
  $bg-white: #ffffff;
  $bg-light: #f8f9fa;
  $border-light: #e9ecef;
  $success-green: #51cf66;
  $warning-yellow: #ffd43b;
  $danger-red: #ff6b6b;

  .title-white {
    color: #1a1a1a;
    font-weight: 700;
    font-size: 2.5rem;
  }

  .title-gold {
    color: #ffffff;
    font-weight: 700;
    font-size: 2.5rem;
  }

  .contest-list-container {
    margin: 0 auto;
    width: 100%;
    max-width: 1200px;
    padding: 3rem 2rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  }

  /* Section Header */
  .contests-section {
    margin-bottom: 3.5rem;
    animation: fadeInUp 0.6s ease-out;
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 3px solid $primary-blue;

    .section-icon {
      width: 28px;
      height: 28px;
      color: $primary-blue;
      flex-shrink: 0;
    }

    .section-title {
      font-size: 1.5rem;
      font-weight: 700;
      color: $text-primary;
      margin: 0;
    }

    .contest-count {
      margin-left: auto;
      padding: 0.5rem 1rem;
      background: $primary-light-blue;
      color: $primary-blue;
      border-radius: 20px;
      font-weight: 600;
      font-size: 0.9rem;
    }

    .toggle-icon {
      width: 24px;
      height: 24px;
      color: $primary-blue;
      transition: transform 0.3s ease;
    }
  }

  /* Contest Grid */
  .contests-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }

  /* Contest Card */
  .contest-card {
    position: relative;
    background: $bg-white;
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid $border-light;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 24px rgba(76, 110, 245, 0.15);
      border-color: $primary-blue;

      .card-overlay {
        opacity: 0.05;
      }

      .action-icon {
        transform: translateX(4px);
      }
    }

    .card-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: $primary-blue;
      opacity: 0;
      transition: opacity 0.3s ease;
      pointer-events: none;
      z-index: 0;
    }
  }

  .contest-card-active {
    border-left: 4px solid $success-green;
  }

  .contest-card-upcoming {
    border-left: 4px solid $warning-yellow;
  }

  .contest-card-finished {
    border-left: 4px solid $text-light;
  }

  .contest-card-locked {
    opacity: 0.7;
    border-left: 4px solid $danger-red;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
  }

  .card-badge {
    display: inline-block;
    padding: 0.4rem 0.85rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
  }

  .badge-active {
    background: rgba(81, 207, 102, 0.1);
    color: $success-green;
  }

  .badge-upcoming {
    background: rgba(255, 212, 59, 0.1);
    color: $warning-yellow;
  }

  .badge-finished {
    background: rgba(102, 102, 102, 0.1);
    color: $text-light;
  }

  .badge-locked {
    background: rgba(255, 107, 107, 0.1);
    color: $danger-red;
  }

  .card-participants {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: $text-light;
    font-weight: 600;
  }

  .card-content {
    margin-bottom: 1.5rem;
    position: relative;
    z-index: 1;
    flex: 1;
  }

  .card-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: $text-primary;
    margin: 0 0 0.5rem 0;
    line-height: 1.4;
    word-break: break-word;
  }

  .card-subtitle {
    font-size: 0.85rem;
    color: $text-light;
    margin: 0;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 1rem;
    border-top: 1px solid $border-light;
    position: relative;
    z-index: 1;
  }

  .time-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: $text-light;

    .icon-small {
      width: 16px;
      height: 16px;
    }
  }

  .card-action {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: $primary-light-blue;
    border-radius: 8px;
    transition: all 0.3s ease;

    .action-icon {
      width: 18px;
      height: 18px;
      color: $primary-blue;
      transition: transform 0.3s ease;
    }
  }

  /* Load More Button */
  .load-more-btn {
    display: block;
    margin: 2rem auto 0;
    padding: 0.85rem 2rem;
    background: $bg-light;
    color: $primary-blue;
    border: 2px solid $primary-blue;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      background: $primary-blue;
      color: $bg-white;
      box-shadow: 0 8px 20px $primary-blue-shadow;
    }

    &:active {
      transform: scale(0.98);
    }
  }

  /* Pagination */
  .pagination-custom {
    margin-top: 2rem;
    justify-content: center;

    ::v-deep .page-link {
      color: $primary-blue;
      border-color: $border-light;
      border-radius: 6px;
      margin: 0 0.25rem;
      transition: all 0.3s ease;

      &:hover {
        background-color: $primary-light-blue;
        color: $primary-blue;
        border-color: $primary-blue;
      }
    }

    ::v-deep .page-item.active .page-link {
      background-color: $primary-blue;
      border-color: $primary-blue;
      color: $bg-white;
      box-shadow: 0 4px 12px $primary-blue-shadow;
    }
  }

  /* Modal */
  ::v-deep .contest-modal {
    .modal-content {
      border: none;
      border-radius: 12px;
      box-shadow: 0 20px 60px rgba(76, 110, 245, 0.15);
    }

    .modal-header {
      border-bottom: 1px solid $border-light;
      background: $bg-light;
      padding: 1.5rem;

      .modal-title {
        font-weight: 700;
        color: $text-primary;
      }
    }

    .modal-footer {
      border-top: 1px solid $border-light;
      background: $bg-light;
      padding: 1.5rem;

      .btn-primary {
        background: $primary-blue;
        border-color: $primary-blue;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;

        &:hover {
          background: $primary-dark-blue;
          border-color: $primary-dark-blue;
          box-shadow: 0 4px 12px $primary-blue-shadow;
        }
      }

      .btn-secondary {
        color: $primary-blue;
        border-color: $border-light;
        border-radius: 8px;
        transition: all 0.3s ease;

        &:hover {
          border-color: $primary-blue;
          background: transparent;
        }
      }
    }
  }

  /* 애니메이션 */
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* 반응형 디자인 */
  @media (max-width: 1024px) {
    .contest-list-container {
      padding: 2rem 1.5rem;
    }

    .contests-grid {
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem;
    }

    .section-header {
      .section-title {
        font-size: 1.3rem;
      }
    }

    .title-white,
    .title-gold {
      font-size: 2rem;
    }
  }

  @media (max-width: 768px) {
    .contest-list-container {
      padding: 1.5rem 1rem;
    }

    .contests-grid {
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }

    .section-header {
      flex-direction: column;
      align-items: flex-start;
      border-bottom: 2px solid $primary-blue;

      .contest-count {
        margin-left: 0;
      }

      .toggle-icon {
        position: absolute;
        right: 0;
        top: 0;
      }
    }

    .section-title {
      font-size: 1.15rem;
    }

    .contest-card {
      padding: 1.25rem;
    }

    .card-title {
      font-size: 1rem;
    }

    .title-white,
    .title-gold {
      font-size: 1.5rem;
    }
  }

  @media (max-width: 480px) {
    .contest-list-container {
      padding: 1rem 0.75rem;
    }

    .contests-grid {
      grid-template-columns: 1fr;
    }

    .contests-section {
      margin-bottom: 2.5rem;
    }

    .section-header {
      padding-bottom: 0.75rem;
      margin-bottom: 1.5rem;

      .section-title {
        font-size: 1.1rem;
      }

      .section-icon {
        width: 24px;
        height: 24px;
      }

      .contest-count {
        padding: 0.35rem 0.75rem;
        font-size: 0.8rem;
      }
    }

    .contest-card {
      padding: 1rem;
    }

    .card-header {
      margin-bottom: 0.75rem;
    }

    .card-content {
      margin-bottom: 1rem;
    }

    .card-title {
      font-size: 0.95rem;
    }

    .card-subtitle {
      font-size: 0.8rem;
    }

    .card-footer {
      padding-top: 0.75rem;
    }

    .time-info {
      font-size: 0.8rem;
    }

    .card-participants {
      font-size: 0.8rem;
    }

    .title-white,
    .title-gold {
      font-size: 1.3rem;
    }

    .load-more-btn {
      width: 100%;
      padding: 0.75rem 1rem;
      font-size: 0.9rem;
    }
  }
</style>
