import { capture } from './errorReporting'
import { getAuthToken } from './selectors'

const actionErrorValues = {
  PENDING: null,
  SUCCESSFUL: false,
  FAILED: true
}

function BitketApiError(message, payload, extra) {
  this.message = message
  this.stack = (new Error()).stack
  this.payload = payload
  this.extra = extra
}
BitketApiError.prototype = new Error()
BitketApiError.prototype.name = 'BitketApiError'

const fetchAction = ({actionType, url, options={}, extraMeta={}, useAuth=false}) => (dispatch, getState) => {
  const baseAction = {
    type: actionType,
    meta: {
      url: url,
      ...extraMeta
    }
  }

  const dispatchSuccessful = (payload) => dispatch(
    Object.assign({}, baseAction, {
      error: actionErrorValues.SUCCESSFUL,
      payload: payload
    })
  )

  const dispatchFailed = (error) => dispatch(
    Object.assign({}, baseAction, {
      error: actionErrorValues.FAILED,
      payload: error
    })
  )

  let defaultOptions = {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }
  const authToken = getAuthToken(getState())
  if (useAuth && authToken) {
    defaultOptions.headers['Authorization'] = `JWT ${authToken}`
  }

  dispatch(Object.assign({}, baseAction, {
    error: actionErrorValues.PENDING
  }))

  return fetch(url, Object.assign({}, defaultOptions, options))
    .then((response) => {
      // Note that fetch resolves on any successful HTTP request, i.e. 4xx and
      // 5xx as well.
      return response.json().then((payload) => {
        // Is the status code 200-299?
        if (response.ok) {
          return dispatchSuccessful(payload)
        } else {
          const err = new BitketApiError(payload.detail ? payload.detail : response.statusText, payload, {url, options})
          capture(err)
          return dispatchFailed(err)
        }
      }, (error) => {
        // We've got something other than a JSON body. Just use the generic
        // statusText in dispatch. error.message is probably more interesting
        // technically, though.
        const bitketError = new BitketApiError(response.statusText, error, {url, options})
        capture(bitketError)
        return dispatchFailed(bitketError)
      })
    }, (error) => {
      // We have a communication problem. response is a TypeError.
      const bitketError = new BitketApiError(error.message, error, {url, options})
      // Opbeat really don't want a TypeError
      capture(bitketError)
      return dispatchFailed(bitketError)
    })
}

export {
  actionErrorValues,
  BitketApiError,
  fetchAction
}
