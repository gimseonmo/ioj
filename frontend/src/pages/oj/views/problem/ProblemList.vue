<template>
  <div class="problem-container">
    <page-top>
      <template #title>
        <span class="text-white">문제</span>
      </template>
      <template #description>
        알아서 풀어보시길.. <br>* 문제 번호와 난이도는 무관
      </template>
    </page-top>

    <div class="problem-wrapper">
      <!-- 문제 그룹 섹션 -->
      <div v-for="problemSetGroup in problemSetGroups" :key="problemSetGroup.id" class="group-section">
        <div class="group-header">
          <b-icon icon="folder2-open" class="group-icon"/>
          <h3 class="group-title">{{ problemSetGroup.title }}</h3>
        </div>
        <problem-set-group :problem-set-group="problemSetGroup"></problem-set-group>
      </div>

      <!-- 모든 문제 섹션 -->
      <div class="all-problems-section">
        <div class="section-header">
          <div class="section-title">
            <b-icon icon="code-slash" class="section-icon"/>
            <span>모든 문제</span>
          </div>
        </div>

        <!-- 필터 섹션 -->
        <div class="filter-section tag-filter-item .filter-item">
          <div class="filter-group">
            <!-- 난이도 필터 -->
            <div class="filter-item">
              <label class="filter-label">
                <b-icon icon="thermometer-half" class="filter-icon"/>
                난이도
              </label>
              <b-dropdown :text="difficulty" class="difficulty-dropdown" variant="outline-primary">
                <b-dropdown-item @click="filterByDifficulty('All')">
                  <b-icon icon="circle-fill" style="color: #999;" class="mr-2"/>
                  전체
                </b-dropdown-item>
                <b-dropdown-item @click="filterByDifficulty('Level1')">
                  <b-icon icon="circle-fill" style="color: #FFB800;" class="mr-2"/>
                  Level 1
                </b-dropdown-item>
                <b-dropdown-item @click="filterByDifficulty('Level2')">
                  <b-icon icon="circle-fill" style="color: #FF9500;" class="mr-2"/>
                  Level 2
                </b-dropdown-item>
                <b-dropdown-item @click="filterByDifficulty('Level3')">
                  <b-icon icon="circle-fill" style="color: #FF7D00;" class="mr-2"/>
                  Level 3
                </b-dropdown-item>
                <b-dropdown-item @click="filterByDifficulty('Level4')">
                  <b-icon icon="circle-fill" style="color: #FF5722;" class="mr-2"/>
                  Level 4
                </b-dropdown-item>
                <b-dropdown-item @click="filterByDifficulty('Level5')">
                  <b-icon icon="circle-fill" style="color: #E63946;" class="mr-2"/>
                  Level 5
                </b-dropdown-item>
                <b-dropdown-item @click="filterByDifficulty('Level6')">
                  <b-icon icon="circle-fill" style="color: #A4161A;" class="mr-2"/>
                  Level 6
                </b-dropdown-item>
                <b-dropdown-item @click="filterByDifficulty('Level7')">
                  <b-icon icon="circle-fill" style="color: #670000;" class="mr-2"/>
                  Level 7
                </b-dropdown-item>
              </b-dropdown>
            </div>

            <!-- 태그 필터 -->
            <!-- 태그 필터 -->
            <div class="filter-item tag-filter-item">
              <label class="filter-label">
                <b-icon icon="tag" class="filter-icon"/>
                태그
              </label>
              <b-form-checkbox
                v-model="checked"
                name="check-button"
                switch
                class="tag-switch"
              >
              </b-form-checkbox>
            </div>

            <!-- 검색 필터 -->
            <div class="filter-item search-item tag-filter-item">
              <label class="filter-label">
                <b-icon icon="search" class="filter-icon"/>
                검색
              </label>
              <div class="search-box" style="width: 70%;">
                <b-icon icon="magnifying-glass" class="search-icon"/>
                <b-input
                  placeholder="문제 검색..."
                  class="search-input"
                  v-model="keyword"
                  @input="filterByKeyword"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- 테이블 섹션 -->
        <div class="table-section">
          <b-table
            hover
            :items="problemList"
            :fields="problemTableColumns"
            :per-page="perPage"
            :current-page="currentPage"
            head-variant="light"
            @row-clicked="goProblem"
            class="problem-table"
            responsive
          >
            <template #head()="data">
              <div class="table-header-cell">
                {{ data.label }}
              </div>
            </template>

            <template #cell(title)="data">
              <div class="problem-title-cell">
                <span>{{ data.value }}</span>
                <b-icon
                  v-if="data.item.my_status===0"
                  icon="check-circle-fill"
                  class="completed-icon"
                  font-scale="1.1"
                ></b-icon>
              </div>
            </template>

            <template #cell(difficulty)="data">
              <div class="difficulty-cell">
                <b-icon
                  icon="circle-fill"
                  class="difficulty-dot"
                  :style="'color:' + difficultyColor(data.value)"
                />
                <span>{{ data.value }}</span>
              </div>
            </template>

            <template #cell(AC_Rate)="data">
              <div class="ac-rate-cell">
                {{ getACRate(data.item.accepted_number, data.item.submission_number) }}
              </div>
            </template>

            <template v-slot:cell(tags)="data">
              <div v-show="checked" class="tags-cell">
                <b-badge
                  v-for="item in data.item.tags"
                  :key="item"
                  class="tag-badge"
                >
                  {{ item }}
                </b-badge>
              </div>
            </template>

            <template v-slot:head(tags)="field">
              <div v-show="checked">{{ field.label }}</div>
            </template>
          </b-table>
        </div>

        <!-- 페이지네이션 -->
        <div class="pagination-section">
          <b-pagination
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            limit="5"
            class="problem-pagination"
          ></b-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import api from '@oj/api'
import { ProblemMixin } from '@oj/components/mixins'
import { DIFFICULTY_COLOR } from '@/utils/constants'
import ProblemSetGroup from '@oj/components/ProblemSetGroup.vue'
import PageTop from '@oj/components/PageTop.vue'

export default {
  name: 'problemList',
  components: {
    ProblemSetGroup,
    PageTop
  },
  mixins: [ProblemMixin],
  data () {
    return {
      perPage: 20,
      currentPage: 1,
      checked: false,
      problemList: [],
      limit: 50,
      total: 0,
      keyword: '',
      difficulty: 'All',
      tag: '',
      page: 1,
      problemTableColumns: [
        {
          label: '#',
          key: '_id'
        },
        {
          label: '문제',
          key: 'title',
          tdClass: 'problem-title-field',
          thClass: 'problem-title-field'
        },
        {
          label: '난이도',
          key: 'difficulty',
          tdClass: 'difficulty-field'
        },
        {
          label: '제출',
          key: 'submission_number'
        },
        'AC_Rate',
        {
          label: '태그',
          key: 'tags'
        }
      ]
    }
  },
  computed: {
    rows () {
      return this.problemList.length
    },
    ...mapGetters(['isAuthenticated'])
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      await this.getTagList()
      await this.getProblemSetGroupList()
      await this.getProblemList()
    },
    async getProblemSetGroupList () {
      const res = await api.getProblemSetGroup()
      this.problemSetGroups = res.data.data
    },
    async getTagList () {
      const res = await api.getProblemTagList()
      this.tagList = res.data.data
    },
    async getProblemList () {
      const offset = (this.page - 1) * this.limit
      const res = await api.getProblemList(offset, this.limit,
        {
          difficulty: this.difficulty === 'All' ? '' : this.difficulty,
          keyword: this.keyword,
          tag: this.tag,
          page: this.page
        }
      )
      this.total = res.data.data.total
      this.problemList = res.data.data.results
      if (this.isAuthenticated) {
        this.addStatusColumn(this.problemTableColumns, res.data.data.results)
      }
    },
    async filterByDifficulty (item) {
      this.difficulty = item
      this.page = 1
      await this.getProblemList()
    },
    async filterByKeyword () {
      this.page = 1
      await this.getProblemList()
    },
    difficultyColor (value) {
      return DIFFICULTY_COLOR[value]
    },
    async goProblem (item) {
      await this.$router.push({ name: 'problem-details', params: { problemID: item._id } })
    }
  },
  watch: {
    async 'isAuthenticated' (newVal) {
      await this.init()
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
  $primary-blue-shadow-light: rgba(76, 110, 245, 0.1);
  $text-primary: #111111;
  $text-secondary: #888888;
  $bg-light: #f5f7fa;
  $bg-white: #ffffff;
  $border-light: #e9ecef;
  $success-green: #51cf66;

  * {
    box-sizing: border-box;
  }

  .problem-container {
    background: $bg-white;
    min-height: 100vh;
    padding: 0;
    margin: 0;
    width: 100%;
    display: flex;
    flex-direction: column;
  }

  .problem-wrapper {
    width: 100vw;
    margin: 0;
    margin-left: calc(-50vw + 50%);
    padding: 3rem 2rem;
    background: linear-gradient(135deg, #e7f0ff 0%, #d4e5ff 100%);
    min-height: calc(100vh - 200px);
    flex: 1;
  }

  /* 문제 그룹 섹션 */
  .group-section {
    background: $bg-white;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid $border-light;
    animation: slideInUp 0.6s ease-out;

    &:hover {
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
      transform: translateY(-2px);
    }
  }
  .filter-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;

    &.search-item {
      flex: 1;
      min-width: 250px;

      @media (max-width: 768px) {
        min-width: auto;
      }
    }

    // 태그 필터 라인 정렬
    &.tag-filter-item {
      flex-direction: row;
      align-items: center;
      gap: 1rem;

      .filter-label {
        margin: 0;
      }

      .tag-switch {
        margin-top: 0;
      }
    }
  }

  .tag-switch {
    margin-top: 0.25rem;

    ::v-deep .custom-control-label {
      cursor: pointer;
      font-weight: 500;
      color: $text-secondary;

      &::before {
        border-color: $primary-blue;
      }
    }

    ::v-deep .custom-switch .custom-control-input:checked ~ .custom-control-label::before {
      background-color: $primary-blue;
      border-color: $primary-blue;
    }
  }
  .group-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #f0f2f5;

    .group-icon {
      width: 24px;
      height: 24px;
      color: $primary-blue;
      flex-shrink: 0;
    }

    .group-title {
      font-size: 1.2rem;
      font-weight: 700;
      color: $text-primary;
      margin: 0;
    }
  }

  /* 모든 문제 섹션 */
  .all-problems-section {
    background: $bg-white;
    border-radius: 16px;
    padding: 2rem;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    border: 1px solid $border-light;
    animation: slideInUp 0.6s ease-out 0.1s both;

    &:hover {
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
      transform: translateY(-2px);
    }
  }

  .section-header {
    display: flex;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid #f0f2f5;
  }

  .section-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.3rem;
    font-weight: 700;
    color: $text-primary;
    letter-spacing: -0.5px;

    .section-icon {
      width: 28px;
      height: 28px;
      color: $primary-blue;
      flex-shrink: 0;
    }
  }

  /* 필터 섹션 */
  .filter-section {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: #f8fbff;
    border-radius: 12px;
    border: 1px solid #e7f0ff;
  }

  .filter-group {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    align-items: flex-end;

    @media (max-width: 1024px) {
      gap: 1rem;
    }

    @media (max-width: 768px) {
      flex-direction: column;
      align-items: stretch;
    }
  }

  .filter-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;

    &.search-item {
      flex: 1;
      min-width: 250px;

      @media (max-width: 768px) {
        min-width: auto;
      }
    }
  }

  .filter-label {
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 600;
    font-size: 0.95rem;
    color: $text-primary;
    cursor: default;

    .filter-icon {
      width: 16px;
      height: 16px;
      color: $primary-blue;
      flex-shrink: 0;
    }
  }

  .difficulty-dropdown {
    border-radius: 8px;
    border: 2px solid $primary-blue;
    color: $primary-blue;
    font-weight: 600;
    padding: 0.5rem 1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background-color: $bg-white;
    cursor: pointer;

    &:hover {
      background-color: $primary-light-blue;
      border-color: $primary-dark-blue;
      color: $primary-dark-blue;
      box-shadow: 0 4px 12px $primary-blue-shadow;
    }

    &:active {
      transform: scale(0.98);
    }
  }

  .tag-switch {
    ::v-deep .custom-control-label {
      cursor: pointer;
      font-weight: 500;
      color: $text-secondary;

      &::before {
        border-color: $primary-blue;
      }
    }

    ::v-deep .custom-switch .custom-control-input:checked ~ .custom-control-label::before {
      background-color: $primary-blue;
      border-color: $primary-blue;
    }
  }

  .search-box {
    position: relative;
    width: 100%;
    display: flex;
    align-items: center;

    .search-icon {
      position: absolute;
      left: 12px;
      width: 18px;
      height: 18px;
      color: $text-secondary;
      pointer-events: none;
      flex-shrink: 0;
    }

    .search-input {
      width: 100%;
      padding: 0.65rem 1rem 0.65rem 40px;
      border-radius: 8px;
      border: 2px solid $border-light;
      font-size: 0.95rem;
      transition: all 0.3s ease;
      background-color: $bg-white;

      &::placeholder {
        color: #c0c0c0;
      }

      &:focus {
        border-color: $primary-blue;
        box-shadow: 0 0 0 3px $primary-light-blue;
        outline: none;
      }
    }
  }

  /* 테이블 섹션 */
  .table-section {
    margin-bottom: 2rem;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid $border-light;
  }

  ::v-deep .problem-table {
    margin-bottom: 0;
    background: $bg-white;

    thead {
      background: linear-gradient(135deg, #f0f3ff 0%, #e7f0ff 100%);
      border-bottom: 2px solid $border-light;

      th {
        padding: 1.25rem 1.5rem;
        font-weight: 700;
        color: $text-primary;
        font-size: 0.95rem;
        border: none;
        letter-spacing: 0.3px;
      }
    }

    tbody {
      tr {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        border-bottom: 1px solid #f0f2f5;

        &:hover {
          background-color: #fafbff;
          box-shadow: inset 0 0 0 1px $primary-light-blue;

          td {
            color: $primary-blue;
          }

          .problem-title-cell {
            color: $primary-blue;

            span {
              text-decoration: underline;
              text-decoration-color: $primary-blue;
              text-underline-offset: 3px;
            }
          }
        }

        &:last-child {
          border-bottom: none;
        }

        td {
          padding: 1.25rem 1.5rem;
          font-size: 0.95rem;
          color: $text-primary;
          transition: all 0.3s ease;
          vertical-align: middle;
        }
      }
    }
  }

  .table-header-cell {
    font-weight: 700;
    color: $text-primary;
    letter-spacing: 0.3px;
  }

  .problem-title-cell {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 600;
    color: $text-primary;
    transition: all 0.3s ease;

    span {
      transition: all 0.3s ease;
    }

    .completed-icon {
      color: $success-green;
      flex-shrink: 0;
      font-size: 1.1rem;
    }
  }

  .difficulty-cell {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 600;

    .difficulty-dot {
      width: 14px;
      height: 14px;
      flex-shrink: 0;
    }
  }

  .ac-rate-cell {
    font-weight: 600;
    color: $text-secondary;
  }

  .tags-cell {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;

    .tag-badge {
      background: $primary-light-blue;
      color: $primary-blue;
      border: 1px solid $primary-blue;
      padding: 0.4rem 0.85rem;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 600;
      transition: all 0.3s ease;

      &:hover {
        background: $primary-blue;
        color: $bg-white;
      }
    }
  }

  /* 페이지네이션 */
  .pagination-section {
    display: flex;
    justify-content: center;
    padding: 2rem 0 1rem 0;

    ::v-deep .problem-pagination {
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
      transform: translateY(30px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* 반응형 디자인 */
  @media (max-width: 1024px) {
    .problem-wrapper {
      padding: 2rem 1.5rem;
    }

    .group-section,
    .all-problems-section {
      padding: 1.5rem;
    }

    .filter-group {
      gap: 1rem;
    }

    ::v-deep .problem-table {
      font-size: 0.9rem;

      thead th,
      tbody td {
        padding: 1rem 1.25rem;
      }
    }
  }

  @media (max-width: 768px) {
    .problem-wrapper {
      padding: 1.5rem 1rem;
    }

    .group-section,
    .all-problems-section {
      padding: 1.25rem;
      border-radius: 12px;
    }

    .group-header {
      gap: 10px;
      margin-bottom: 1.5rem;

      .group-icon {
        width: 22px;
        height: 22px;
      }

      .group-title {
        font-size: 1.1rem;
      }
    }

    .section-header {
      margin-bottom: 1.5rem;
    }

    .section-title {
      font-size: 1.1rem;
      gap: 10px;

      .section-icon {
        width: 24px;
        height: 24px;
      }
    }

    .filter-section {
      padding: 1rem;
      margin-bottom: 1.5rem;
    }

    .filter-group {
      flex-direction: column;
      align-items: stretch;
      gap: 1rem;
    }

    .filter-item.search-item {
      min-width: auto;
      flex: none;
    }

    .difficulty-dropdown {
      width: 100%;
    }

    ::v-deep .problem-table {
      font-size: 0.85rem;

      thead th,
      tbody td {
        padding: 0.85rem 1rem;
      }
    }

    .problem-title-field {
      width: 35%;
    }

    .tags-cell {
      .tag-badge {
        padding: 0.35rem 0.7rem;
        font-size: 0.8rem;
      }
    }
  }

  @media (max-width: 480px) {
    .problem-wrapper {
      padding: 1rem 0.75rem;
    }

    .group-section,
    .all-problems-section {
      padding: 1rem;
      border-radius: 12px;
    }

    .group-header {
      gap: 8px;
      margin-bottom: 1rem;

      .group-icon {
        width: 20px;
        height: 20px;
      }

      .group-title {
        font-size: 1rem;
      }
    }

    .section-title {
      font-size: 1rem;
      gap: 8px;

      .section-icon {
        width: 22px;
        height: 22px;
      }
    }

    .filter-section {
      padding: 0.75rem;
      margin-bottom: 1rem;
    }

    .filter-label {
      font-size: 0.9rem;

      .filter-icon {
        width: 16px;
        height: 16px;
      }
    }

    .search-box {
      .search-input {
        padding: 0.6rem 1rem 0.6rem 38px;
        font-size: 0.9rem;
      }
    }

    ::v-deep .problem-table {
      font-size: 0.8rem;

      thead th,
      tbody td {
        padding: 0.7rem 0.85rem;
      }
    }

    .problem-title-cell {
      gap: 0.5rem;

      .completed-icon {
        font-size: 1rem;
      }
    }

    .tags-cell {
      gap: 0.5rem;

      .tag-badge {
        padding: 0.3rem 0.6rem;
        font-size: 0.75rem;
      }
    }
  }
</style>
