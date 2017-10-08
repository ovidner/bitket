import createLogger from 'redux-logger'

import { capture } from './errorReporting'

const loggerMiddleware = createLogger({
  // Transforms the state to regular JS types for easier debugging in console
  stateTransformer: (state) => state.toJS()
})

const errorReportingMiddleware = (store) => (next) => (action) => {
  try {
    return next(action)
  } catch (error) {
    capture(error, {
      action: action,
      state: store.getState()
    })

    throw error
  }
}

export { loggerMiddleware, errorReportingMiddleware }
