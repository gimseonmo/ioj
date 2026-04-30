export const JUDGE_STATUS = {
  '-2': {
    name: '컴파일 오류가 발생했어요',
    short: '컴파일 오류',
    color: 'yellow',
    type: 'warning'
  },
  '-1': {
    name: '정답과 출력이 달라요',
    short: '오답',
    color: 'red',
    type: 'error'
  },
  0: {
    name: '정답이에요',
    short: '정답',
    color: 'green',
    type: 'success'
  },
  1: {
    name: '실행 시간이 너무 오래 걸렸어요',
    short: '시간 초과',
    color: 'red',
    type: 'error'
  },
  2: {
    name: '실행 시간이 너무 오래 걸렸어요',
    short: '시간 초과',
    color: 'red',
    type: 'error'
  },
  3: {
    name: '메모리를 너무 많이 사용했어요',
    short: '메모리 초과',
    color: 'red',
    type: 'error'
  },
  4: {
    name: '실행 중 오류가 발생했어요',
    short: '런타임 오류',
    color: 'red',
    type: 'error'
  },
  5: {
    name: '채점 시스템 오류가 발생했어요',
    short: '시스템 오류',
    color: 'red',
    type: 'error'
  },
  6: {
    name: '채점을 기다리고 있어요',
    short: '대기 중',
    color: 'yellow',
    type: 'warning'
  },
  7: {
    name: '채점 중이에요',
    short: '채점 중',
    color: 'blue',
    type: 'info'
  },
  8: {
    name: '일부 테스트만 맞았어요',
    short: '부분 정답',
    color: 'blue',
    type: 'info'
  },
  9: {
    name: '제출하고 있어요',
    short: '제출 중',
    color: 'yellow',
    type: 'warning'
  }
}

export const DIFFICULTY_COLOR = {
  Level1: '#CC99C9',
  Level2: '#9EC1CF',
  Level3: '#A1F2C2',
  Level4: '#B8FF81',
  Level5: '#F3EC53',
  Level6: '#FEB144',
  Level7: '#FF6663'
}

export const CONTEST_STATUS = {
  NOT_START: '1',
  UNDERWAY: '0',
  ENDED: '-1'
}

export const CONTEST_STATUS_REVERSE = {
  1: {
    name: 'Not Started',
    color: '#5398D9'
  },
  0: {
    name: 'Underway',
    color: '#8DC63F'
  },
  '-1': {
    name: 'Ended',
    color: '#D75B66'
  }
  // #D75B66 #23345C #F1BA48 #BD8A44
}

export const ASSIGNMENT_STATUS = {
  NOT_START: '1',
  UNDERWAY: '0',
  ENDED: '-1'
}

export const ASSIGNMENT_STATUS_REVERSE = {
  1: {
    name: 'Not Started',
    color: '#5398D9'
  },
  0: {
    name: 'Underway',
    color: '#F1BA48'
  },
  '-1': {
    name: 'Ended',
    color: '#D75B66'
  }
  // #D75B66 #23345C #F1BA48 #BD8A44
}

export const ASSIGNMENT_SUBMISSION_STATUS = {
  NOT_SUBMITTED: '1',
  SUBMITTING: '0',
  SUBMITTED: '-1'
}

export const ASSIGNMENT_SUBMISSION_STATUS_REVERSE = {
  1: {
    name: 'Not Submitted',
    color: '#5398D9'
  },
  0: {
    name: 'Submitting',
    color: '#F1BA48'
  },
  '-1': {
    name: 'Submitted',
    color: '#D75B66'
  }
  // #D75B66 #23345C #F1BA48 #BD8A44
}

export const RULE_TYPE = {
  ACM: 'ACM',
  OI: 'OI'
}

export const CONTEST_TYPE = {
  PUBLIC: 'Public',
  PRIVATE: 'Password Protected'
}

export const USER_TYPE = {
  REGULAR_USER: 'Regular User',
  ADMIN: 'Admin',
  SUPER_ADMIN: 'Super Admin'
}

export const PROBLEM_PERMISSION = {
  NONE: 'None',
  OWN: 'Own',
  ALL: 'All'
}

export const STORAGE_KEY = {
  AUTHED: 'authed',
  PROBLEM_CODE: 'problemCode',
  languages: 'languages'
}

export function buildProblemCodeKey (problemID, contestID = null) {
  if (contestID) {
    return `${STORAGE_KEY.PROBLEM_CODE}_${contestID}_${problemID}`
  }
  return `${STORAGE_KEY.PROBLEM_CODE}_NaN_${problemID}`
}
