import { Map } from 'immutable'
import jwtDecode from 'jwt-decode'

import { sumMoney } from './dataTypes'

// Filters '_isPending' and other meta-keys.
const isMeta = (value, key) => key.startsWith('_')
const isNotMeta = (value, key) => !isMeta(value, key)

const authIsPending = (state) => state
  .getIn(['session', 'auth', '_isPending'])

const getAuthToken = (state) => state
  .getIn(['session', 'auth', 'token'])

const getCurrentUser = (state) => {
  const token = getAuthToken(state)
  return token ? jwtDecode(token) : null
}

const getAllAccessCodes = (state, meta=false) => state
  .getIn(['session', 'accessCodes'])
  .filter(meta ? isMeta : isNotMeta)

const getAllEvents = (state, meta=false) => state
  .get('events')
  .filter(meta ? isMeta : isNotMeta)

const getAllOrganizations = (state, meta=false) => state
  .get('organizations')
  .filter(meta ? isMeta : isNotMeta)

const getAllTicketTypes = (state, meta=false) => state
  .get('ticketTypes')
  .filter(meta ? isMeta : isNotMeta)

const getAllVariations = (state, meta=false) => state
  .get('variations')
  .filter(meta ? isMeta : isNotMeta)

const getAllVariationChoices = (state, meta=false) => state
  .get('variationChoices')
  .filter(meta ? isMeta : isNotMeta)

const getEvent = (state, eventUrl) => getAllEvents(state)
  .get(eventUrl)

const getEventFromSlug = (state, slug) => getAllEvents(state)
  .find(e => e.get('slug') === slug)

const getOrganization = (state, organizationUrl) => getAllOrganizations(state)
  .get(organizationUrl)

const getTicketType = (state, ticketTypeUrl) => getAllTicketTypes(state)
  .get(ticketTypeUrl)

const getTicketTypesOfEvent = (state, eventUrl) => getAllTicketTypes(state)
  .filter(t => t.get('event') === eventUrl)

const getSelectedTicketTypes = (state) => state
  .getIn(['session', 'selections', 'ticketTypes'])

const getSelectedTicketTypesOfEvent = (state, eventUrl) => getTicketTypesOfEvent(state, eventUrl)
  .filter((ticketType) => (
    getSelectedTicketTypes(state).includes(ticketType.get('url'))
  ))

const getSelectedVariationChoices = (state) => state
  .getIn(['session', 'selections', 'variationChoices'])

const getStateToPersist = (state) => state
  .filter((value, key) => (
    key === 'session'
  ))
  .deleteIn(['session', 'accessCodes'])
  .deleteIn(['session', 'auth', '_isPending'])
  .deleteIn(['session', 'auth', '_error'])

const getVariationsOfTicketType = (state, ticketTypeUrl) => getAllVariations(state)
  .filter((v) => v.get('ticketType') === ticketTypeUrl)

const getVariationChoicesOfVariation = (state, variationUrl) => getAllVariationChoices(state)
  .filter((v) => v.get('variation') === variationUrl)

const getSelectedVariationChoicesOfTicketType = (state, ticketTypeUrl) => getSelectedVariationChoices(state)
  .filter((variationChoiceUrl, variationUrl) => getVariationsOfTicketType(state, ticketTypeUrl).has(variationUrl))

const getSelectedConflictsOfTicketType = (state, ticketTypeUrl) => getAllTicketTypes(state)
  .filter((_, url) => getSelectedTicketTypes(state)
    .includes(url))
  .filter((_, url) => getTicketType(state, ticketTypeUrl)
    .get('conflictsWith')
    .includes(url))

const getPriceOfTicketType = (state, ticketTypeUrl) => {
  const ticketType = getTicketType(state, ticketTypeUrl)
  const basePrice = ticketType.get('price')
  const modifierDeltas = ticketType.get('modifiers').map(m => m.get('delta'))
  const variationChoiceDeltas = getSelectedVariationChoicesOfTicketType(state, ticketTypeUrl)
    .map((v) => getAllVariationChoices(state).getIn([v, 'delta']))
    .toList()

  return sumMoney(basePrice, ...modifierDeltas, ...variationChoiceDeltas)
}

const getTotalAmountForEvent = (state, eventUrl) => {
  const amounts = getSelectedTicketTypesOfEvent(state, eventUrl)
    .map((ticketType) => getPriceOfTicketType(state, ticketType.get('url')))
    .toList()

  return sumMoney(...amounts)
}

const getPurchase = (state) => state.get('purchase')

const makePurchaseBody = (state, eventUrl, stripeToken, nin) => {

  return {
    access_codes: getAllAccessCodes(state).map(c => c.get('token')).toList().toJS(),
    tickets: getSelectedTicketTypesOfEvent(state, eventUrl).map(ticketType => Map.of(
      'ticket_type', ticketType.get('url'),
      'variation_choices', getSelectedVariationChoicesOfTicketType(state, ticketType.get('url')).toList()
    )).toList().toJS(),
    payment: {
      type: 'stripe',
      payload: stripeToken,
      amount: getTotalAmountForEvent(state, eventUrl)
    },
    user: {
      nin: nin
    }
  }
}

const isLoggedIn = (state) => !!getAuthToken(state)

const ticketTypeHasValidVariationChoiceSelections = (state, ticketTypeUrl) => (
  getVariationsOfTicketType(state, ticketTypeUrl)
    .every((_, url) => getSelectedVariationChoices(state).has(url))
)

const ticketTypeIsSelectable = (state, ticketTypeUrl) => {
  const ticketType = getTicketType(state, ticketTypeUrl)

  return ticketType.getIn(['availability', 'quantity']) && (
    ticketType.getIn(['availability', 'general']) ||
    getAllAccessCodes(state)
      .some((accessCode) => (
        accessCode.get('isUtilizable') &&
        accessCode.get('ticketType') === ticketTypeUrl))
    )
}

const eventHasValidSelections = (state, eventUrl) => {
  const selectedTicketTypes = getSelectedTicketTypesOfEvent(state, eventUrl)

  if (selectedTicketTypes.isEmpty()) return false

  return selectedTicketTypes.every((ticketType) => (
    ticketType.getIn(['availability', 'quantity']) && (ticketType.getIn(['availability', 'general']) || ticketType.getIn(['availability', 'personal']))
  ))
}

export {
  authIsPending,
  getAllAccessCodes,
  getAllEvents,
  getAllOrganizations,
  getAllTicketTypes,
  getAllVariations,
  getAllVariationChoices,
  getAuthToken,
  getCurrentUser,
  getEvent,
  getEventFromSlug,
  getOrganization,
  getPriceOfTicketType,
  getPurchase,
  makePurchaseBody,
  getSelectedConflictsOfTicketType,
  getSelectedTicketTypes,
  getSelectedVariationChoices,
  getSelectedVariationChoicesOfTicketType,
  getStateToPersist,
  getTicketType,
  getTicketTypesOfEvent,
  getTotalAmountForEvent,
  getVariationsOfTicketType,
  getVariationChoicesOfVariation,
  isLoggedIn,
  isNotMeta,
  ticketTypeHasValidVariationChoiceSelections
}
