import * as api from './api'
import { apiRoot, authProviders } from './settings'
import * as selectors from './selectors'
import { getRedirectUri } from './utils'

const actionTypes = {
  ADD_ACCESS_CODE: 'ADD_ACCESS_CODE',
  API: {
    GET_AUTH_TOKEN: 'API.GET_AUTH_TOKEN',
    GET_EVENTS: 'API.GET_EVENTS',
    GET_ORGANIZATIONS: 'API.GET_ORGANIZATIONS',
    GET_TICKET_TYPES: 'API.GET_TICKET_TYPES',
    GET_VARIATIONS: 'API.GET_VARIATIONS',
    GET_VARIATION_CHOICES: 'API.GET_VARIATION_CHOICES',
    SUBMIT_PURCHASE: 'API.SUBMIT_PURCHASE'
  },
  LOG_OUT: 'LOG_OUT',
  SELECT_TICKET_TYPE: 'SELECT_TICKET_TYPE',
  SELECT_VARIATION_CHOICE: 'SELECT_VARIATION_CHOICE',
  DESELECT_TICKET_TYPE: 'DESELECT_TICKET_TYPE'
}

const addAccessCode = (accessCode) => api.fetchAction({
  actionType: actionTypes.ADD_ACCESS_CODE,
  url: `${apiRoot}/access-codes/${accessCode}/`,
  extraMeta: {
    code: accessCode
  }
})

const fetchAuthToken = (providerId, code) => api.fetchAction({
  actionType: actionTypes.API.GET_AUTH_TOKEN,
  url: `${apiRoot}/auth-token/`,
  options: {
    method: 'POST',
    body: JSON.stringify({
      redirect_uri: getRedirectUri(window.location.origin, providerId),
      provider: authProviders[providerId].backendId,
      code
    })
  }
})

const refreshAuthToken = (auto = false) => (dispatch, getState) => api.fetchAction({
  actionType: actionTypes.API.GET_AUTH_TOKEN,
  url: `${apiRoot}/auth-token/refresh/`,
  options: {
    method: 'POST',
    body: JSON.stringify({
      token: selectors.getAuthToken(getState())
    })
  },
  extraMeta: {
    auto
  },
  useAuth: true
})(dispatch, getState)

const fetchEvents = () => api.fetchAction({
  actionType: actionTypes.API.GET_EVENTS,
  url: `${apiRoot}/events/`
})

const fetchOrganizations = () => api.fetchAction({
  actionType: actionTypes.API.GET_ORGANIZATIONS,
  url: `${apiRoot}/organizations/`
})

const fetchTicketTypes = () => api.fetchAction({
  actionType: actionTypes.API.GET_TICKET_TYPES,
  url: `${apiRoot}/ticket-types/`,
  useAuth: true
})

const fetchVariations = () => api.fetchAction({
  actionType: actionTypes.API.GET_VARIATIONS,
  url: `${apiRoot}/variations/`
})

const fetchVariationChoices = () => api.fetchAction({
  actionType: actionTypes.API.GET_VARIATION_CHOICES,
  url: `${apiRoot}/variation-choices/`
})

const logOut = () => ({
  type: actionTypes.LOG_OUT
})

const performPurchase = (stripeToken) => (dispatch, getState) => {
  return api.fetchAction({
    actionType: actionTypes.API.SUBMIT_PURCHASE,
    url: `${apiRoot}/purchases/`,
    options: {
      method: 'POST',
      body: JSON.stringify(selectors.getPurchaseBody(getState(), stripeToken))
    },
    useAuth: true
  })(dispatch, getState)
}

const selectTicketType = (ticketTypeUrl) => ({
  type: actionTypes.SELECT_TICKET_TYPE,
  payload: ticketTypeUrl
})

const deselectTicketType = (ticketTypeUrl) => ({
  type: actionTypes.DESELECT_TICKET_TYPE,
  payload: ticketTypeUrl
})

const selectVariationChoice = (variationUrl, variationChoiceUrl) => ({
  type: actionTypes.SELECT_VARIATION_CHOICE,
  payload: {variationUrl, variationChoiceUrl}
})

export {
  actionTypes,
  addAccessCode,
  fetchAuthToken,
  fetchEvents,
  fetchOrganizations,
  fetchTicketTypes,
  fetchVariations,
  fetchVariationChoices,
  logOut,
  performPurchase,
  refreshAuthToken,
  selectTicketType,
  selectVariationChoice,
  deselectTicketType
}
