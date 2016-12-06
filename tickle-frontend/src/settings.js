// These constants are replaced with values at build!

// Without trailing slash
const apiRoot = process.env.REACT_APP_API_ROOT

const authProviders = {
  facebook: {
    id: 'facebook',
    backendId: 'facebook',
    authUrl: 'https://www.facebook.com/v2.7/dialog/oauth',
    clientId: process.env.REACT_APP_AUTH_FACEBOOK_CLIENT_ID,
    scope: 'public_profile',
    scopeParam: 'scope'
  },
  google: {
    id: 'google',
    backendId: 'google-oauth2',
    authUrl: 'https://accounts.google.com/o/oauth2/v2/auth',
    clientId: process.env.REACT_APP_AUTH_GOOGLE_CLIENT_ID,
    scope: 'openid email profile',
    scopeParam: 'scope'
  },
  liu: {
    id: 'liu',
    backendId: 'liu',
    authUrl: `https://${process.env.REACT_APP_AUTH_LIU_ADFS_HOST}/adfs/oauth2/authorize`,
    clientId: process.env.REACT_APP_AUTH_LIU_CLIENT_ID,
    scope: process.env.REACT_APP_AUTH_LIU_RESOURCE,
    scopeParam: 'resource'
  }
}

// Number of milliseconds before JWT expiry to issue a refresh
const jwtRefreshMargin = 60 * 1000

const opbeatAppId = process.env.REACT_APP_OPBEAT_APP_ID
const opbeatOrgId = process.env.REACT_APP_OPBEAT_ORG_ID

const persistedStateKey = 'state'

const stripePublicKey = process.env.REACT_APP_STRIPE_PUBLIC_KEY

export { apiRoot, authProviders, jwtRefreshMargin, opbeatAppId, opbeatOrgId, persistedStateKey, stripePublicKey }
