// This should be the only file aware that we use Opbeat for error reporting.
import { opbeatAppId, opbeatOrgId } from './settings'

const init = () => {
  window._opbeat('config', {
    orgId: opbeatOrgId,
    appId: opbeatAppId
  })
}

const setExtraContext = (extraContext) => {
  window._opbeat('setExtraContext', extraContext)
}

const capture = (err, extraContext = {}) => {
  Object.assign(extraContext, {payload: err.payload}, err.extra)
  setExtraContext(extraContext)
  window._opbeat('captureException', err)
}

const setUserContext = ({id, email}) => {
  window._opbeat('setUserContext', {
    is_authenticated: !!id,
    id: id,
    email: email,
    username: email
  })
}

export {
  init,
  capture,
  setExtraContext,
  setUserContext
}
