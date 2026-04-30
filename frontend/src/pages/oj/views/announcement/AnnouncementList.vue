<template>
  <div>
    <page-top>
      <template #title>
        <span class="title-icon">📢</span>
        <span class="title-text">공지사항</span>
      </template>
      <template #description>
        최신 소식과 중요한 공지사항을 확인하세요
      </template>
    </page-top>

    <div class="announcement-container">
      <div class="announcement-section">
        <!-- 검색 및 필터 -->
        <div class="filter-section">
          <div class="search-box">
            <b-icon icon="search" class="search-icon"></b-icon>
            <b-form-input
              v-model="searchKeyword"
              placeholder="공지사항 검색..."
              class="search-input"
              @input="filterAnnouncements"
            />
          </div>
          <div class="filter-stats">
            <span class="stat-item">
              <b-icon icon="pin-fill" class="stat-icon"></b-icon>
              고정됨: {{ topFixedCount }}
            </span>
            <span class="stat-divider">|</span>
            <span class="stat-item">
              <b-icon icon="file-text" class="stat-icon"></b-icon>
              전체: {{ announcements.length }}
            </span>
          </div>
        </div>

        <!-- 공지사항 리스트 -->
        <div class="announcements-list">
          <div
            v-if="filteredAnnouncements.length === 0"
            class="empty-state"
          >
            <b-icon icon="inbox" class="empty-icon"></b-icon>
            <p class="empty-text">공지사항이 없습니다.</p>
          </div>

          <div
            v-for="(announcement, index) in paginatedAnnouncements"
            :key="announcement.id"
            class="announcement-item"
            :class="{ 'is-pinned': announcement.top_fixed }"
            @click="goAnnouncement(announcement)"
          >
            <div class="announcement-badge-group">
              <b-icon
                v-if="announcement.top_fixed"
                icon="pin-fill"
                class="pin-badge"
                title="고정됨"
              ></b-icon>
              <span class="index-badge">{{ calculateIdx(index) }}</span>
            </div>

            <div class="announcement-content">
              <h3 class="announcement-title">
                {{ announcement.title }}
              </h3>
              <p class="announcement-preview" v-if="announcement.content">
                {{ announcement.content.substring(0, 100) }}{{ announcement.content.length > 100 ? '...' : '' }}
              </p>
              <div class="announcement-meta">
                <span class="meta-item">
                  <b-icon icon="calendar-event" class="meta-icon"></b-icon>
                  {{ getTimeFormat(announcement.create_time) }}
                </span>
              </div>
            </div>

            <div class="announcement-arrow">
              <b-icon icon="chevron-right" class="arrow-icon"></b-icon>
            </div>

            <div class="announcement-overlay"></div>
          </div>
        </div>

        <!-- 페이지네이션 -->
        <div class="pagination-section" v-if="filteredAnnouncements.length > 0">
          <b-pagination
            v-model="currentPage"
            :total-rows="filteredAnnouncements.length"
            :per-page="perPage"
            limit="5"
            class="pagination-custom"
          ></b-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@oj/api'
import time from '@/utils/time'
import PageTop from '@oj/components/PageTop.vue'

export default {
  name: 'Announcement',
  components: {
    PageTop
  },
  data () {
    return {
      perPage: 10,
      currentPage: 1,
      btnLoading: false,
      announcements: [],
      searchKeyword: '',
      topFixedCount: 0
    }
  },
  computed: {
    isContest () {
      return !!this.$route.params.contestID
    },
    filteredAnnouncements () {
      if (!this.searchKeyword) {
        return this.announcements
      }
      return this.announcements.filter(announcement =>
        announcement.title.toLowerCase().includes(this.searchKeyword.toLowerCase()) ||
        (announcement.content && announcement.content.toLowerCase().includes(this.searchKeyword.toLowerCase()))
      )
    },
    paginatedAnnouncements () {
      const start = (this.currentPage - 1) * this.perPage
      const end = start + this.perPage
      return this.filteredAnnouncements.slice(start, end)
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      if (this.isContest) {
        await this.getContestAnnouncementList()
      } else {
        await this.getAnnouncementList()
      }
    },
    async getAnnouncementList () {
      this.btnLoading = true
      try {
        const res = await api.getAnnouncementList(0, 250)
        this.btnLoading = false
        const announcements = res.data.data.results
        const topFixed = announcements.filter(
          (announcement) => announcement.top_fixed === true
        )
        this.topFixedCount = topFixed.length
        const notTopFixed = announcements.filter(
          (announcement) => announcement.top_fixed === false
        )
        this.announcements = [...topFixed, ...notTopFixed]
      } catch (err) {
        this.btnLoading = false
        this.$error('공지사항을 불러오는데 실패했습니다.')
      }
    },
    async getContestAnnouncementList () {
      this.btnLoading = true
      try {
        const res = await api.getContestAnnouncementList(this.$route.params.contestID)
        this.btnLoading = false
        const announcements = res.data.data
        const topFixed = announcements.filter(
          (announcement) => announcement.top_fixed === true
        )
        this.topFixedCount = topFixed.length
        const notTopFixed = announcements.filter(
          (announcement) => announcement.top_fixed === false
        )
        this.announcements = [...topFixed, ...notTopFixed]
      } catch (err) {
        this.btnLoading = false
        this.$error('공지사항을 불러오는데 실패했습니다.')
      }
    },
    async goAnnouncement (announcement) {
      await this.$router.push({
        name: 'announcement-details',
        params: { announcementID: announcement.id }
      })
    },
    filterAnnouncements () {
      this.currentPage = 1
    },
    calculateIdx (index) {
      return (this.currentPage - 1) * this.perPage + index + 1
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-MM-DD')
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
  $warning-yellow: #ffd43b;

  .title-icon {
    font-size: 2.5rem;
    margin-right: 1rem;
  }

  .title-text {
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a1a;
  }

  .announcement-container {
    width: 100%;
    background: linear-gradient(135deg, #e7f0ff 0%, #d4e5ff 100%);
    min-height: calc(100vh - 200px);
    padding: 3rem 2rem;
  }

  .announcement-section {
    max-width: 900px;
    margin: 0 auto;
  }

  /* 필터 섹션 */
  .filter-section {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    margin-bottom: 2.5rem;
    flex-wrap: wrap;

    @media (max-width: 768px) {
      flex-direction: column;
      align-items: stretch;
    }
  }

  .search-box {
    position: relative;
    flex: 1;
    min-width: 250px;
    display: flex;
    align-items: center;

    .search-icon {
      position: absolute;
      left: 14px;
      width: 18px;
      height: 18px;
      color: $text-secondary;
      pointer-events: none;
      flex-shrink: 0;
    }

    .search-input {
      width: 100%;
      padding: 0.8rem 1rem 0.8rem 40px;
      border-radius: 10px;
      border: 2px solid $primary-blue;
      font-size: 0.95rem;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      background-color: $bg-white;

      &::placeholder {
        color: #c0c0c0;
      }

      &:focus {
        outline: none;
        box-shadow: 0 0 0 4px $primary-light-blue;
        border-color: $primary-dark-blue;
      }
    }
  }

  .filter-stats {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1.25rem;
    background: $bg-white;
    border-radius: 10px;
    border: 1px solid $border-light;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);

    @media (max-width: 768px) {
      justify-content: center;
      width: 100%;
    }
  }

  .stat-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    color: $text-primary;
    font-size: 0.9rem;

    .stat-icon {
      width: 18px;
      height: 18px;
      color: $primary-blue;
    }
  }

  .stat-divider {
    color: $border-light;
    font-weight: 300;
  }

  /* 공지사항 리스트 */
  .announcements-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .empty-state {
    text-align: center;
    padding: 3rem 2rem;
    background: $bg-white;
    border-radius: 12px;
    border: 2px dashed $border-light;
    animation: fadeIn 0.6s ease-out;

    .empty-icon {
      width: 48px;
      height: 48px;
      color: $text-secondary;
      margin-bottom: 1rem;
    }

    .empty-text {
      font-size: 1.1rem;
      color: $text-secondary;
      margin: 0;
      font-weight: 500;
    }
  }

  .announcement-item {
    position: relative;
    background: $bg-white;
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid $border-light;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    align-items: center;
    gap: 1.25rem;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    animation: slideInUp 0.5s ease-out;

    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 24px rgba(76, 110, 245, 0.15);
      border-color: $primary-blue;

      .announcement-overlay {
        opacity: 0.05;
      }

      .arrow-icon {
        transform: translateX(4px);
      }

      .announcement-title {
        color: $primary-blue;
      }
    }

    &.is-pinned {
      border-left: 4px solid $warning-yellow;
      background: linear-gradient(135deg, rgba(255, 212, 59, 0.02) 0%, transparent 100%);
    }

    .announcement-overlay {
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

  .announcement-badge-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-shrink: 0;
    position: relative;
    z-index: 1;
  }

  .pin-badge {
    width: 20px;
    height: 20px;
    color: $warning-yellow;
    flex-shrink: 0;
  }

  .index-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: $primary-light-blue;
    color: $primary-blue;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.85rem;
    flex-shrink: 0;
  }

  .announcement-content {
    flex: 1;
    min-width: 0;
    position: relative;
    z-index: 1;
  }

  .announcement-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: $text-primary;
    margin: 0 0 0.5rem 0;
    line-height: 1.4;
    transition: color 0.3s ease;
    word-break: break-word;
  }

  .announcement-preview {
    font-size: 0.9rem;
    color: $text-light;
    margin: 0.5rem 0;
    line-height: 1.5;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }

  .announcement-meta {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 0.75rem;

    .meta-item {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.85rem;
      color: $text-secondary;

      .meta-icon {
        width: 16px;
        height: 16px;
      }
    }
  }

  .announcement-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: $primary-light-blue;
    border-radius: 8px;
    flex-shrink: 0;
    position: relative;
    z-index: 1;
    transition: all 0.3s ease;

    .arrow-icon {
      width: 20px;
      height: 20px;
      color: $primary-blue;
      transition: transform 0.3s ease;
    }
  }

  /* 페이지네이션 */
  .pagination-section {
    display: flex;
    justify-content: center;
    padding: 2rem 0;

    ::v-deep .pagination-custom {
      .page-link {
        border-radius: 8px;
        border: 1px solid $border-light;
        color: $text-primary;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 0 0.35rem;
        padding: 0.6rem 0.9rem;
        font-weight: 500;

        &:hover:not(.disabled) {
          background-color: $primary-light-blue;
          border-color: $primary-blue;
          color: $primary-blue;
          transform: translateY(-2px);
        }

        &.active {
          background-color: $primary-blue;
          border-color: $primary-blue;
          color: $bg-white;
          box-shadow: 0 4px 12px $primary-blue-shadow;
        }

        &.disabled {
          opacity: 0.4;
          cursor: not-allowed;
        }
      }
    }
  }

  /* 애니메이션 */
  @keyframes slideInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
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
    .announcement-container {
      padding: 2rem 1.5rem;
    }

    .announcement-item {
      padding: 1.25rem;
      gap: 1rem;

      .announcement-title {
        font-size: 1rem;
      }
    }
  }

  @media (max-width: 768px) {
    .announcement-container {
      padding: 1.5rem 1rem;
    }

    .filter-section {
      gap: 1rem;
    }

    .search-box {
      min-width: auto;
    }

    .filter-stats {
      flex-direction: column;
      gap: 0.75rem;
    }

    .announcement-item {
      flex-direction: column;
      align-items: flex-start;
      padding: 1.25rem;

      .announcement-badge-group {
        width: 100%;
      }

      .announcement-content {
        width: 100%;
      }

      .announcement-arrow {
        position: absolute;
        right: 1rem;
        top: 1rem;
      }
    }

    .announcement-title {
      font-size: 1rem;
    }
  }

  @media (max-width: 480px) {
    .announcement-container {
      padding: 1rem 0.75rem;
    }

    .announcement-section {
      max-width: 100%;
    }

    .filter-section {
      flex-direction: column;
      gap: 0.75rem;
      margin-bottom: 1.5rem;
    }

    .search-box {
      width: 100%;
    }

    .filter-stats {
      width: 100%;
      padding: 0.6rem 1rem;
      font-size: 0.8rem;
    }

    .stat-item {
      font-size: 0.8rem;

      .stat-icon {
        width: 16px;
        height: 16px;
      }
    }

    .announcement-item {
      padding: 1rem;
      gap: 0.75rem;
    }

    .index-badge {
      width: 28px;
      height: 28px;
      font-size: 0.8rem;
    }

    .pin-badge {
      width: 18px;
      height: 18px;
    }

    .announcement-title {
      font-size: 0.95rem;
    }

    .announcement-preview {
      font-size: 0.85rem;
    }

    .announcement-meta {
      gap: 0.75rem;

      .meta-item {
        font-size: 0.8rem;

        .meta-icon {
          width: 14px;
          height: 14px;
        }
      }
    }

    .announcement-arrow {
      width: 32px;
      height: 32px;

      .arrow-icon {
        width: 18px;
        height: 18px;
      }
    }

    ::v-deep .pagination-custom {
      .page-link {
        padding: 0.5rem 0.75rem;
        font-size: 0.85rem;
      }
    }

    .title-icon {
      font-size: 1.8rem;
      margin-right: 0.75rem;
    }

    .title-text {
      font-size: 1.5rem;
    }
  }
</style>
