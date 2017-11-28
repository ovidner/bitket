import { createOpbeatMiddleware } from 'opbeat-react/redux'
import createLogger from 'redux-logger'

const loggerMiddleware = createLogger({
  // Transforms the state to regular JS types for easier debugging in console
  stateTransformer: (state) => state.toJS()
})

const errorReportingMiddleware = createOpbeatMiddleware()

export { loggerMiddleware, errorReportingMiddleware }
