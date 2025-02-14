export const nthNumber = (number) => {
  return number > 0
    ? ['th', 'st', 'nd', 'rd'][
      (number > 3 && number < 21) || number % 10 > 3 ? 0 : number % 10
    ]
    : ''
}

export const getCurrentDate = () => {
  const today = new Date()
  const day = today.getDate()
  const month = today.toLocaleString('en-US', { month: 'long' })
  const suffix = nthNumber(day)

  return `${month} ${day+suffix}`
}

export const getCurrentTime = () => (new Date()).toLocaleString('en-US', {
  hour: 'numeric',
  minute: '2-digit',
  hour12: true
})

export const apiDefaults = {
  defaultVal: location.hostname == 'localhost' ? 
    {clientPrincipal: {userDetails: 'localuser@test.com', userId: '1234test1234'}} : 
    null,
  condition: location.hostname !== 'localhost'
}

export function randomInteger(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}