import { capture } from './errorReporting'
import { getAuthToken } from './selectors'

const actionErrorValues = {
  PENDING: null,
  SUCCESSFUL: false,
  FAILED: true
}

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
          const err = new Error(payload.detail)
          capture(err, {url, options, payload})
          return dispatchFailed(err)
        }
      }, (error) => {
        // We've got something other than a JSON body. Just use the generic
        // statusText in dispatch. error.message is probably more interesting
        // technically, though.
        capture(new Error(error.message), {url, options})
        return dispatchFailed(new Error(response.statusText))
      })
    }, (error) => {
      // We have a communication problem. response is a TypeError.

      // Opbeat really don't want a TypeError
      capture(new Error(error.message), {error, url, options})
      return dispatchFailed(error)
    })
}

export {
  actionErrorValues,
  fetchAction
}
