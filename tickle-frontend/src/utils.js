import { fromJS } from 'immutable'
import jwtDecode from 'jwt-decode'

import * as actions from './actions'
import * as settings from './settings'
import * as selectors from './selectors'

const partialSubscribe = (store, select, onChange, fireNow = false) => {
  // Observes a Redux store. store should be a Redux store. select should be a
  // callback accepting the state as argument, returning a slice of the state to
  // observe. onChange should be a callback accepting the state as argument.
  // https://github.com/reactjs/redux/issues/303#issuecomment-125184409
  let currentState = select(store.getState())

  if (fireNow) {
    onChange(currentState)
  }

  return store.subscribe(() => {
    const nextState = select(store.getState())
    if (nextState !== currentState) {
      currentState = nextState
      onChange(currentState)
    }
  })
}

const autoFetchUserDependentData = (store) => partialSubscribe(store,
  selectors.getAuthToken, (state) => {
    store.dispatch(actions.fetchTicketTypes())
  }, true)

const autoPersistState = (store) => partialSubscribe(store, selectors.getStateToPersist, (state) => {
  window.localStorage.setItem(
    settings.persistedStateKey,
    JSON.stringify(state.toJS()))
})

const autoRefreshAuthToken = (store) => {
  let activeTimer = null

  const performRefresh = () => {
    console.log('Dispatching auth token refresh')
    store.dispatch(actions.refreshAuthToken(true))
  }

  const setUpTimer = (authToken) => {
    if (activeTimer) {
      window.clearTimeout(activeTimer)
    }

    if (authToken === null) {
      return
    }

    const expiryTime = jwtDecode(authToken).exp
    const timeToRefresh = (expiryTime * 1000) - Date.now() - settings.jwtRefreshMargin
    console.log('Refreshing auth token in', timeToRefresh, 'ms')

    if (timeToRefresh <= 0) {
      activeTimer = null
      performRefresh()
    } else {
      activeTimer = window.setTimeout(
        performRefresh,
        timeToRefresh
      )
    }
  }

  return partialSubscribe(store, selectors.getAuthToken, setUpTimer, true)
}

const getRedirectUri = (origin, providerId) => (
  `${origin}/log-in/${providerId}/`
)

const mergePersistedState = (state) => {
  const persistedStateJson = window.localStorage.getItem(settings.persistedStateKey)
  if (persistedStateJson) {
    return state.mergeDeep(fromJS(JSON.parse(persistedStateJson)))
  } else {
    return state
  }
}

// https://gist.github.com/peppelorum/5856691
const ninIsValid = (input) => {
  // Check valid length & form
  if (!input) { return false }

  if (input.indexOf('-') === -1) {
    if (input.length === 10) {
      input = input.slice(0, 6) + "-" + input.slice(6)
    } else {
      input = input.slice(0, 8) + "-" + input.slice(8)
    }
  }
  if (!input.match(/^(\d{2})(\d{2})(\d{2})\-(\d{4})|(\d{4})(\d{2})(\d{2})\-(\d{4})$/)) { return false }

  // Clean input
  input = input.replace('-', '')
  if (input.length === 12) {
    input = input.substring(2)
  }

  // Declare variables
  var d = new Date(((!!RegExp.$1) ? RegExp.$1 : RegExp.$5), (((!!RegExp.$2) ? RegExp.$2 : RegExp.$6)-1), ((!!RegExp.$3) ? RegExp.$3 : RegExp.$7)),
    sum = 0,
    numdigits = input.length,
    parity = numdigits % 2,
    i,
    digit

  // Check valid date
  if (Object.prototype.toString.call(d) !== "[object Date]" || isNaN(d.getTime())) return false

  // Check luhn algorithm
  for (i = 0; i < numdigits; i = i + 1) {
    digit = parseInt(input.charAt(i), 10)
    if (i % 2 === parity) { digit *= 2 }
    if (digit > 9) { digit -= 9 }
    sum += digit
  }
  return (sum % 10) === 0
}

export { autoFetchUserDependentData, autoPersistState, autoRefreshAuthToken, getRedirectUri, mergePersistedState, ninIsValid, partialSubscribe }
