export const getStatusType = (status: string) => {
  switch (status) {
    case 'not_started':
      return 'info'
    case 'in_progress':
      return 'success'
    case 'finished':
      return 'warning'
    default:
      return ''
  }
}

export const getStatusText = (status: string) => {
  switch (status) {
    case 'not_started':
      return '未开始'
    case 'in_progress':
      return '进行中'
    case 'finished':
      return '已结束'
    default:
      return ''
  }
}

export const getPrizeLevelText = (level: string) => {
  switch (level) {
    case 'first':
      return '一等奖'
    case 'second':
      return '二等奖'
    case 'third':
      return '三等奖'
    case 'special':
      return '特等奖'
    case 'participation':
      return '参与奖'
    default:
      return level
  }
}

export const getPrizeLevelType = (level: string) => {
  switch (level) {
    case 'first':
      return 'danger'
    case 'second':
      return 'warning'
    case 'third':
      return 'success'
    case 'special':
      return 'primary'
    case 'participation':
      return 'info'
    default:
      return ''
  }
}

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

export const debounce = (func: Function, wait: number) => {
  let timeout: ReturnType<typeof setTimeout>
  return function(...args: any[]) {
    clearTimeout(timeout)
    timeout = setTimeout(() => func.apply(this, args), wait)
  }
}

export const throttle = (func: Function, limit: number) => {
  let inThrottle: boolean
  return function(...args: any[]) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}