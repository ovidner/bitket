export const getBackendEnv = () => {
  const backendEnvElementContent = window.document.getElementById('BACKEND_INJECTED_ENV').textContent

  let backendEnv
  try {
    backendEnv = JSON.parse(backendEnvElementContent)
  } catch(e) {
    if (process.env.NODE_ENV !== 'production') {
      console.warn(
        `Backend injected environment could not be parsed. This is
        normal when running in development mode (yarn start).`
      )
    }
  }
  return backendEnv
}

const env = Object.assign({}, {
  // These may be replaced with values at build!
  API_ROOT: process.env.REACT_APP_API_ROOT,
  AUTH_FACEBOOK_AUTHORIZATION_URL: process.env.AUTH_FACEBOOK_AUTHORIZATION_URL,
  AUTH_FACEBOOK_CLIENT_ID: process.env.REACT_APP_AUTH_FACEBOOK_CLIENT_ID,
  AUTH_GOOGLE_AUTHORIZATION_URL: process.env.REACT_APP_AUTH_GOOGLE_AUTHORIZATION_URL,
  AUTH_GOOGLE_CLIENT_ID: process.env.REACT_APP_AUTH_GOOGLE_CLIENT_ID,
  AUTH_LIU_AUTHORIZATION_URL: process.env.REACT_APP_AUTH_LIU_AUTHORIZATION_URL,
  AUTH_LIU_CLIENT_ID: process.env.REACT_APP_AUTH_LIU_CLIENT_ID,
  AUTH_LIU_RESOURCE: process.env.REACT_APP_AUTH_LIU_RESOURCE,
  OPBEAT_APP_ID: process.env.REACT_APP_OPBEAT_APP_ID,
  OPBEAT_ORG_ID: process.env.REACT_APP_OPBEAT_ORG_ID,
  STRIPE_PUBLIC_KEY: process.env.REACT_APP_STRIPE_PUBLIC_KEY,
  TYPEKIT_ID: process.env.REACT_APP_TYPEKIT_ID
}, getBackendEnv() || {})

// Without trailing slash
const apiRoot = env.API_ROOT || '/api'

const authProviders = {
  facebook: {
    id: 'facebook',
    backendId: 'facebook',
    authUrl: env.AUTH_FACEBOOK_AUTHORIZATION_URL,
    clientId: env.AUTH_FACEBOOK_CLIENT_ID,
    scope: 'public_profile,email',
    scopeParam: 'scope'
  },
  google: {
    id: 'google',
    backendId: 'google-oauth2',
    authUrl: env.AUTH_GOOGLE_AUTHORIZATION_URL,
    clientId: env.AUTH_GOOGLE_CLIENT_ID,
    scope: 'openid email profile',
    scopeParam: 'scope'
  },
  liu: {
    id: 'liu',
    backendId: 'liu',
    authUrl: env.AUTH_LIU_AUTHORIZATION_URL,
    clientId: env.AUTH_LIU_CLIENT_ID,
    scope: env.AUTH_LIU_RESOURCE,
    scopeParam: 'resource'
  }
}

// Number of milliseconds before JWT expiry to issue a refresh
const jwtRefreshMargin = 60 * 1000

const opbeatAppId = env.OPBEAT_APP_ID
const opbeatOrgId = env.OPBEAT_ORG_ID

const persistedStateKey = 'state'
const persistedStateTimestampKey = 'stateTimestamp'
// The threshold for destroying persisted state. If the state is older than
// this (or not set), it will be destroyed. UTC timestamp, use
// (new Date).getTime()
const persistedStateTimestampThreshold = 1481422195713

const stripePublicKey = env.STRIPE_PUBLIC_KEY

const typekitId = process.env.REACT_APP_TYPEKIT_ID

export { apiRoot, authProviders, jwtRefreshMargin, opbeatAppId, opbeatOrgId, persistedStateKey, persistedStateTimestampKey, persistedStateTimestampThreshold, stripePublicKey, typekitId }
