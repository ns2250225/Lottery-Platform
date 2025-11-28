export const validatePhone = (phone: string): boolean => {
  const phoneRegex = /^1[3-9]\d{9}$/
  return phoneRegex.test(phone)
}

export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  return emailRegex.test(email)
}

export const validateRequired = (value: unknown): boolean => {
  if (value === null || value === undefined) return false
  if (typeof value === 'string') return value.trim() !== ''
  if (typeof value === 'number') return !isNaN(value)
  if (typeof value === 'boolean') return true
  if (Array.isArray(value)) return value.length > 0
  return true
}

export const validateLength = (value: string, min: number, max: number): boolean => {
  if (typeof value !== 'string') return false
  return value.length >= min && value.length <= max
}

export const validateNumber = (value: unknown): boolean => {
  if (typeof value === 'number') return !isNaN(value) && isFinite(value)
  if (typeof value === 'string') {
    const parsed = parseFloat(value)
    return !isNaN(parsed) && isFinite(parsed)
  }
  return false
}

export const validatePositiveNumber = (value: unknown): boolean => {
  if (typeof value === 'number') return validateNumber(value) && value > 0
  if (typeof value === 'string') {
    const parsed = parseFloat(value)
    return validateNumber(parsed) && parsed > 0
  }
  return false
}

export const validateInteger = (value: unknown): boolean => {
  if (typeof value === 'number') return Number.isInteger(value)
  if (typeof value === 'string') {
    const parsed = Number(value)
    return !isNaN(parsed) && Number.isInteger(parsed)
  }
  return false
}

export const validatePositiveInteger = (value: unknown): boolean => {
  if (typeof value === 'number') return validateInteger(value) && value > 0
  if (typeof value === 'string') {
    const parsed = Number(value)
    return validateInteger(parsed) && parsed > 0
  }
  return false
}