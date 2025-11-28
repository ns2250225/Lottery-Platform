import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.locale('zh-cn')
dayjs.extend(relativeTime)

export const formatDate = (date: string | Date, format = 'YYYY-MM-DD HH:mm:ss') => {
  return dayjs(date).format(format)
}

export const fromNow = (date: string | Date) => {
  return dayjs(date).fromNow()
}

export const isDateValid = (date: string | Date) => {
  return dayjs(date).isValid()
}

export const addDays = (date: string | Date, days: number) => {
  return dayjs(date).add(days, 'day').toDate()
}

export const subtractDays = (date: string | Date, days: number) => {
  return dayjs(date).subtract(days, 'day').toDate()
}