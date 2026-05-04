<template>
  <b-modal id="submission-detail-modal" centered hide-backdrop hide-footer @shown="rerenderCodemirror()">
    <template #modal-header="{ close }">
      <div class="modal-title-close">
        <h1>Submission #{{submission_detail.id}}</h1>
        <div class="modal-header-actions">
          <b-button
            class="ai-tutor-button"
            variant="primary"
            :disabled="aiTutorLoading || !submission_detail.code"
            @click="requestAITutor"
          >
            <b-spinner v-if="aiTutorLoading" small />
            <b-icon v-else icon="lightbulb" />
            AI 튜터
          </b-button>
          <b-icon icon="x" class="close-icon" @click="close()"/>
        </div>
      </div>
    </template>
    <div id="submission-info-table">
      <b-table borderless class="align-center"
        :items="[submission_detail]"
        :fields="submission_info_table_fields">
        <template #cell(create_time)="data">
          <span>{{data.item.create_time.split(/[T]|[.]|[+]/).slice(0,2).join(' ')}}</span>
        </template>
        <template #cell(result)="data">
          <span :style="'color: '+resultTextColor(data.item.result)">{{getJudgeStatus(data.item.result)}}</span>
        </template>
      </b-table>
    </div>
    <div id="submission-compile-error-message" v-if="compile_error_message_show">
      <p class="text-danger"> Compile error message: {{ submission_detail.statistic_info.err_info }} </p>
    </div>
    <div id="submission-ai-tutor" v-if="aiTutorVisible">
      <b-alert v-if="aiTutorError" show variant="danger">
        {{ aiTutorError }}
      </b-alert>
      <div v-if="aiTutorLoading" class="ai-tutor-loading">
        <b-spinner variant="primary" />
        <span>AI 튜터가 제출 코드를 분석하고 있습니다.</span>
      </div>
      <b-tabs v-else content-class="ai-tutor-tab-content" pills>
        <b-tab title="디버깅" active>
          <div class="ai-tutor-section">
            <h3>버그 분석</h3>
            <p>{{ aiTutorResult.bug_analysis || '아직 분석 결과가 없습니다.' }}</p>
          </div>
        </b-tab>
        <b-tab title="테스트">
          <div class="ai-tutor-section">
            <h3>숨은 테스트 케이스</h3>
            <ol v-if="aiTutorResult.test_cases.length">
              <li v-for="(testCase, index) in aiTutorResult.test_cases" :key="index">
                {{ testCase }}
              </li>
            </ol>
            <p v-else>아직 생성된 테스트 케이스가 없습니다.</p>
          </div>
        </b-tab>
        <b-tab title="풀이 단계">
          <div class="ai-tutor-section">
            <h3>단계별 풀이 가이드</h3>
            <ol v-if="aiTutorResult.steps.length">
              <li v-for="(step, index) in aiTutorResult.steps" :key="index">
                {{ step }}
              </li>
            </ol>
            <p v-else>아직 생성된 풀이 단계가 없습니다.</p>
          </div>
        </b-tab>
      </b-tabs>
    </div>
    <div id="submission-source-code">
      <h3>Source Code</h3>
      <p>({{ getCodeSize(submission_detail.code) }} Bytes)</p>
      <CodeMirror
        readOnly
        :key="codemirror_key"
        :value="submission_detail.code"
        :language="submission_detail.language"
        theme="material"/>
    </div>
    <div id="submission-detail-table">
      <b-table class="align-center"
        v-if="submission_detail.info"
        :items="submission_detail.info.data"
        :per-page="5"
        :fields="submission_detail_table_fields">
        <template #cell(result)="data">
          <span :style="'color: '+resultTextColor(data.item.result)">{{getJudgeStatus(data.item.result)}}</span>
        </template>
      </b-table>
    </div>
  </b-modal>
</template>
<script>
import CodeMirror from '@oj/components/CodeMirror.vue'
import { JUDGE_STATUS } from '@/utils/constants'
import api from '../../api.js'

export default {
  name: 'SubmissionDetailModal',
  props: ['submission_detail', 'problem_title'],
  mounted () {
  },
  components: {
    CodeMirror
  },
  data () {
    return {
      submission_info_table_fields: [
        { label: 'Submission Time', key: 'create_time' },
        { label: 'User', key: 'username' },
        { label: 'Language', key: 'language' },
        { label: 'Result', key: 'result' }
      ],
      submission_detail_table_fields: [
        { label: '#', key: 'test_case' },
        { label: 'Result', key: 'result' },
        { label: 'Exec time', key: 'real_time' },
        { label: 'Memory', key: 'memory' }
      ],
      codemirror_key: 1,
      aiTutorVisible: false,
      aiTutorLoading: false,
      aiTutorError: '',
      aiTutorResult: {
        bug_analysis: '',
        test_cases: [],
        steps: []
      }
    }
  },
  methods: {
    resultTextColor (result) {
      return JUDGE_STATUS[result].color
    },
    rerenderCodemirror () {
      this.codemirror_key += 1
    },
    getJudgeStatus (result) {
      return JUDGE_STATUS[result].name
    },
    getCodeSize (code) {
      const blob = new Blob([code]).size
      return blob
    },
    async requestAITutor () {
      this.aiTutorVisible = true
      this.aiTutorLoading = true
      this.aiTutorError = ''
      try {
        const res = await api.getAITutorHelp({
          problem: this.buildAITutorProblemText(),
          code: this.submission_detail.code || '',
          error_log: this.buildAITutorErrorLog()
        })
        const result = res.data.data || {}
        this.aiTutorResult = {
          bug_analysis: result.bug_analysis || '',
          test_cases: Array.isArray(result.test_cases) ? result.test_cases : [],
          steps: Array.isArray(result.steps) ? result.steps : []
        }
      } catch (err) {
        this.aiTutorError = this.getRequestErrorMessage(err)
      } finally {
        this.aiTutorLoading = false
      }
    },
    buildAITutorProblemText () {
      return [
        `제목: ${this.problem_title || this.submission_detail.problem_name || this.submission_detail.problem || ''}`,
        '교수 채점 화면에서 선택한 학생 제출 코드입니다. 문제 원문이 없으면 코드와 채점 결과를 중심으로 분석해주세요.'
      ].filter(Boolean).join('\n\n')
    },
    buildAITutorErrorLog () {
      const result = this.submission_detail.result
      const status = JUDGE_STATUS[result] ? JUDGE_STATUS[result].name : ''
      const errInfo = this.submission_detail.statistic_info && this.submission_detail.statistic_info.err_info
        ? this.submission_detail.statistic_info.err_info
        : ''
      return [
        `언어: ${this.submission_detail.language || ''}`,
        status ? `채점 상태: ${status}` : '',
        errInfo ? `컴파일/런타임 메시지: ${errInfo}` : ''
      ].filter(Boolean).join('\n')
    },
    getRequestErrorMessage (err) {
      if (err && err.data && err.data.data) {
        return err.data.data
      }
      if (err && err.response && err.response.data && err.response.data.data) {
        return err.response.data.data
      }
      return 'AI 튜터 요청에 실패했습니다.'
    }
  },
  computed: {
    compile_error_message_show () {
      return this.submission_detail &&
        this.submission_detail.statistic_info &&
        this.submission_detail.statistic_info.err_info
    }
  }
}
</script>

<style lang="scss" scoped>
  ::v-deep .modal {
    .modal-dialog {
      min-width: 1200px;

      .modal-content {
        color: black;
        border: none;
        border-radius: 10px;
        background: #F6F6F6;
        box-shadow: 0px 0px 15px #000000;

        .modal-header {
          border-bottom: none;

          .modal-title-close {
            width: 100%;
            display: flex;
            flex-direction: row;
            justify-content: space-between;

            h1 {
              display: inline-block;
              margin-top: 10px;
              margin-left: 10px;
              font-size: 35px;
            }

            .close-icon {
              font-size: 60px;
            }

            .modal-header-actions {
              display: flex;
              align-items: center;
              gap: 12px;
            }

            .ai-tutor-button {
              display: inline-flex;
              align-items: center;
              gap: 6px;
              min-width: 100px;
              height: 38px;
              font-size: 14px;
            }
          }
        }

        .modal-body {
          padding: 0;

          #clarifications-table {
            table {
              color: black;

              th {
                min-width: 230px;
                padding: 15px 25px;
                border: none;
              }

              td {
                min-width: 230px;
                padding: 15px 25px;
                border-top: 1px solid #3B4F56;
              }
            }
          }

          #my-submissions-table, #all-submissions-table {
            table {
              color: black;

              th {
                min-width: 100px;
                padding: 15px 25px;
                border: none;
              }

              td {
                min-width: 100px;
                padding: 15px 25px;
                border-top: 1px solid #3B4F56;
              }
            }
          }

          #submission-info-table {
            table {
              color: black;
              font-size: 15px;
            }

            tr th:first-child,
            tr td:first-child {
              padding-left: 50px;
            }

            tr th:last-child,
            tr td:last-child {
              padding-right: 50px;
            }
          }

          #submission-compile-error-message {
            padding: 20px 50px;
          }

          #submission-ai-tutor {
            padding: 0 50px 20px;
          }

          .ai-tutor-loading {
            display: flex;
            align-items: center;
            gap: 10px;
            min-height: 80px;
          }

          .ai-tutor-section {
            padding: 18px 0 4px;

            h3 {
              margin-bottom: 10px;
              font-size: 22px;
            }

            p, li {
              font-size: 15px;
              line-height: 1.6;
              white-space: pre-wrap;
            }
          }

          #submission-source-code {
            padding: 20px 50px;
            padding-bottom: 40px;
            color: black;

            h3 {
              font-size: 30px;
              display: inline;
            }
            p {
              font-size: 25px;
            }
          }

          #submission-source-code::v-deep .CodeMirror-sizer {
            margin-left: 38px !important;
          }

          #submission-source-code::v-deep .CodeMirror-gutter-wrapper {
            left: -38px !important;
          }

          #submission-detail-table {
            table {
              font-size: 13px;
              color: black;
              border-collapse: collapse;

              th {
                border: none;
              }

              td {
                border-color: #3B4F56;
              }

              tr th:first-child,
              tr td:first-child {
                padding-left: 70px;
              }

              tr th:last-child,
              tr td:last-child {
                padding-right: 70px;
              }
            }
          }
        }
      }
    }
  }
</style>
