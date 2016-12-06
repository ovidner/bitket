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

  const dispatchFailed = (message) => dispatch(
    Object.assign({}, baseAction, {
      error: actionErrorValues.FAILED,
      payload: new Error(message)
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
          return dispatchFailed(response.statusText)
        }
      })
    })
    .catch((response) => {
      // We have a communication problem. response is a TypeError.
      return dispatchFailed(response.message)
    })
}

export {
  actionErrorValues,
  fetchAction
}
