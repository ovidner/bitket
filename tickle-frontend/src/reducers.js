import { List, OrderedMap, Map, Set, fromJS } from 'immutable'

import { actionTypes } from './actions'
import * as api from './api'
import { Money } from './dataTypes'

const initialState = Map.of(
  // Keys beginning with '_' are considered to be "meta" keys and are usually
  // filtered out by the selectors when getting the objects themselves.

  // _isPending keys are initialized as null to hint if the related entities has
  // even begun to load
  'session', Map.of(
    'auth', Map.of(
      '_isPending', null,
      '_error', null,
      'provider', null,
      'token', null
    ),
    'accessCodes', Map.of(
      '_isPending', null,
      '_error', null
    ),
    'selections', Map.of(
      'ticketTypes', Set.of(),
      'variationChoices', Map.of()
    ),
    'notes', Map.of(

    )
  ),
  'events', Map.of(
    '_isPending', null,
    '_error', null
  ),
  'organizations', Map.of(
    '_isPending', null,
    '_error', null
  ),
  'ticketTypes', Map.of(
    '_isPending', null,
    '_error', null
  ),
  'variations', Map.of(
    '_isPending', null,
    '_error', null
  ),
  'variationChoices', Map.of(
    '_isPending', null,
    '_error', null
  ),
  'purchase', Map.of(
    '_isOpen', false,
    '_isPending', null,
    '_error', null,
    'messages', List.of(),
    'tickets', List.of(),
    'transactions', List.of()
  )
)

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.ADD_ACCESS_CODE:
      switch (action.error) {
        case api.actionErrorValues.PENDING:
          return state
            .setIn(['session', 'accessCodes', '_isPending'], true)
            .setIn(['session', 'accessCodes', '_error'], null)
        case api.actionErrorValues.SUCCESSFUL:
          return state
            .setIn(['session', 'accessCodes', '_isPending'], false)
            .setIn(['session', 'accessCodes', '_error'], null)
            .mergeIn(['session', 'accessCodes', action.payload.token], Map.of(
              'token', action.payload.token,
              'ticketType', action.payload.ticket_type,
              'isUtilizable', action.payload.is_utilizable,
            ))
        case api.actionErrorValues.FAILED:
          return state
            .setIn(['session', 'accessCodes', '_isPending'], false)
            .setIn(['session', 'accessCodes', '_error'], action.payload.message)
        default:
          return state
      }

    case actionTypes.API.GET_AUTH_TOKEN:
      switch (action.error) {
        case api.actionErrorValues.PENDING:
          return state
            .setIn(['session', 'auth', '_isPending'], true)
            .setIn(['session', 'auth', '_error'], null)
        case api.actionErrorValues.SUCCESSFUL:
          return state
            .setIn(['session', 'auth', '_isPending'], false)
            .setIn(['session', 'auth', '_error'], null)
            .setIn(['session', 'auth', 'token'], action.payload.token)
        case api.actionErrorValues.FAILED:
          return (action.meta.auto ? (
            // Failed auto refreshings should end the session
            state.set('session', initialState.get('session'))
          ) : (
            state
          ))
            .setIn(['session', 'auth', '_isPending'], false)
            .setIn(['session', 'auth', '_error'], action.payload.message)
        default:
          return state
      }

    case actionTypes.API.GET_EVENTS:
      switch (action.error) {
        case api.actionErrorValues.PENDING:
          return state
            .setIn(['events', '_isPending'], true)
            .setIn(['events', '_error'], null)
        case api.actionErrorValues.SUCCESSFUL:
          return state
            .setIn(['events', '_isPending'], false)
            .setIn(['events', '_error'], null)
            .mergeIn(['events'], action.payload.reduce((collection, item) => (
              collection.set(item.url, fromJS(item))
            ), Map()))
        case api.actionErrorValues.FAILED:
          return state
            .setIn(['events', '_isPending'], false)
            .setIn(['events', '_error'], action.payload.message)
        default:
          return state
      }

    case actionTypes.API.GET_ORGANIZATIONS:
      switch (action.error) {
        case api.actionErrorValues.PENDING:
          return state
            .setIn(['organizations', '_isPending'], true)
            .setIn(['organizations', '_error'], null)
        case api.actionErrorValues.SUCCESSFUL:
          return state
            .setIn(['organizations', '_isPending'], false)
            .setIn(['organizations', '_error'], null)
            .mergeIn(['organizations'], action.payload.reduce((collection, item) => (
              collection.set(item.url, fromJS(item))
            ), Map()))
        case api.actionErrorValues.FAILED:
          return state
            .setIn(['organizations', '_isPending'], false)
            .setIn(['organizations', '_error'], action.payload.message)
        default:
          return state
      }

    case actionTypes.API.GET_TICKET_TYPES:
      switch (action.error) {
        case api.actionErrorValues.PENDING:
          return state
            .setIn(['ticketTypes', '_isPending'], true)
            .setIn(['ticketTypes', '_error'], null)
        case api.actionErrorValues.SUCCESSFUL:
          return state
            .setIn(['ticketTypes', '_isPending'], false)
            .setIn(['ticketTypes', '_error'], null)
            .mergeIn(['ticketTypes'], action.payload.reduce((collection, item) => (
              collection.set(item.url, Map.of(
                'url', item.url,
                'event', item.event,
                'name', item.name,
                'description', item.description,
                'price', Money(item.price),
                'modifiers', List(item.modifiers.map((modifier) => Map.of(
                  'condition', modifier.condition,
                  'delta', Money(modifier.delta)
                ))),
                'availability', Map.of(
                  'general', item.availability.general,
                  'totalQuantity', item.availability.total_quantity
                ),
                'conflictsWith', item.conflicts_with,
                'index', item.index
              ))
            ), Map()))
        case api.actionErrorValues.FAILED:
          return state
            .setIn(['ticketTypes', '_isPending'], false)
            .setIn(['ticketTypes', '_error'], action.payload.message)
        default:
          return state
      }

    case actionTypes.API.GET_VARIATIONS:
      switch (action.error) {
        case api.actionErrorValues.PENDING:
          return state
            .setIn(['variations', '_isPending'], true)
            .setIn(['variations', '_error'], null)
        case api.actionErrorValues.SUCCESSFUL:
          return state
            .setIn(['variations', '_isPending'], false)
            .setIn(['variations', '_error'], null)
            .mergeIn(['variations'], action.payload.reduce((collection, item) => (
              collection.set(item.url, Map.of(
                'url', item.url,
                'ticketType', item.ticket_type,
                'name', item.name,
                'index', item.index
              ))
            ), Map()))
        case api.actionErrorValues.FAILED:
          return state
            .setIn(['variations', '_isPending'], false)
            .setIn(['variations', '_error'], action.payload.message)
        default:
          return state
      }

    case actionTypes.API.GET_VARIATION_CHOICES:
      switch (action.error) {
        case api.actionErrorValues.PENDING:
          return state
            .setIn(['variationChoices', '_isPending'], true)
            .setIn(['variationChoices', '_error'], null)
        case api.actionErrorValues.SUCCESSFUL:
          return state
            .setIn(['variationChoices', '_isPending'], false)
            .setIn(['variationChoices', '_error'], null)
            .mergeIn(['variationChoices'], action.payload.reduce((collection, item) => (
              collection.set(item.url, Map.of(
                'url', item.url,
                'variation', item.variation,
                'name', item.name,
                'delta', Money(item.delta),
                'index', item.index
              ))
            ), Map()))
        case api.actionErrorValues.FAILED:
          return state
            .setIn(['variationChoices', '_isPending'], false)
            .setIn(['variationChoices', '_error'], action.payload.message)
        default:
          return state
      }

    case actionTypes.API.SUBMIT_PURCHASE:
      switch (action.error) {
        case api.actionErrorValues.PENDING:
          return state
            .set('purchase', initialState.get('purchase'))
            .setIn(['purchase', '_isOpen'], true)
            .setIn(['purchase', '_isPending'], true)
            .setIn(['purchase', '_error'], null)
        case api.actionErrorValues.SUCCESSFUL:
          return state
            .setIn(['purchase', '_isPending'], false)
            .setIn(['purchase', '_error'], null)
            .setIn(['purchase', 'messages'], fromJS(action.payload.messages))
            .setIn(['purchase', 'tickets'], fromJS(action.payload.tickets.map((ticket) => Map.of(
              'url', ticket.url,
              'ticketType', ticket.ticket_type,
              'variationChoices', ticket.variation_choices
            ))))
            .setIn(['purchase', 'transactions'], fromJS(action.payload.transactions))
        case api.actionErrorValues.FAILED:
          return state
            .setIn(['purchase', '_isPending'], false)
            .setIn(['purchase', '_error'], action.payload.message)
        default:
          return state
      }

    case actionTypes.DISMISS_PURCHASE:
      return state.setIn(['purchase', '_isOpen'], false)

    case actionTypes.LOG_OUT:
      return state.set('session', initialState.get('session'))

    case actionTypes.SELECT_TICKET_TYPE:
      return state.setIn(['session', 'selections', 'ticketTypes'],
        state.getIn(['session', 'selections', 'ticketTypes']).add(action.payload))

    case actionTypes.SELECT_VARIATION_CHOICE:
      return state.setIn(
        ['session', 'selections', 'variationChoices', action.payload.variationUrl],
        action.payload.variationChoiceUrl)

    case actionTypes.DESELECT_TICKET_TYPE:
      return state.setIn(['session', 'selections', 'ticketTypes'],
        state.getIn(['session', 'selections', 'ticketTypes']).delete(action.payload))

    default:
      return state
  }
}

export default reducer
export { initialState }
