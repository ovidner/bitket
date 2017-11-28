// This should be the only file aware that we use Opbeat for error reporting.
import { opbeatAppId, opbeatOrgId } from './settings'
import initOpbeat, { captureError, setExtraContext, setUserContext as opbeatSetUserContext } from 'opbeat-react'

const init = () => {
  initOpbeat({
    orgId: opbeatOrgId,
    appId: opbeatAppId
  })
}

const capture = (err, extraContext = {}) => {
  Object.assign(extraContext, {payload: err.payload}, err.extra)
  setExtraContext(extraContext)
  captureError(err)
}

const setUserContext = ({id, email}) => {
  opbeatSetUserContext({
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
