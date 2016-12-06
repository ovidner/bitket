import { List, Map, Set, fromJS } from 'immutable'

import { actionTypes } from './actions'
import * as api from './api'
import { Money } from './dataTypes'

const initialState = Map.of(
  // Keys beginning with '_' are considered to be "meta" keys and are usually
  // filtered out by the selectors when getting the objects themselves.
  'session', Map.of(
    'auth', Map.of(
      '_isPending', false,
      '_error', null,
      'provider', null,
      'token', null
    ),
    'accessCodes', Map.of(
      '_isPending', false,
      '_error', null
    ),
    'selections', Map.of(
      'ticketTypes', Set.of(),
      'variationChoices', Map.of()
    )
  ),
  'events', Map.of(
    '_isPending', false,
    '_error', null
  ),
  'organizations', Map.of(
    '_isPending', false,
    '_error', null
  ),
  'ticketTypes', Map.of(
    '_isPending', false,
    '_error', null,
    'https://backend.bitket.se/v1/ticket-types/c6b86cc6-4f04-4651-bd64-6d50640fc7c4/', Map.of(
      'url', 'https://backend.bitket.se/v1/ticket-types/c6b86cc6-4f04-4651-bd64-6d50640fc7c4/',
      'id', 'c6b86cc6-4f04-4651-bd64-6d50640fc7c4',
      'event', 'https://backend.bitket.se/v1/events/effad9ec-a50c-4484-af54-3df8288689be/',
      'name', 'Entrance ticket',
      'description', '',
      'conflictsWith', List.of(
        'https://backend.bitket.se/v1/ticket-types/4badfcb8-ed51-4ba7-9a5e-3898ef91af44/'
      ),
      'takesNotes', false,
      'availability', Map.of(
        'general', false,
        'personal', false,
        'quantity', true
      ),
      'price', Money('111.00'),
      'modifiers', List.of(
        Map.of(
          'name', 'Student union discount: LinTek',
          'delta', Money('-10.00')
        )
      )
    ),
    'https://backend.bitket.se/v1/ticket-types/4badfcb8-ed51-4ba7-9a5e-3898ef91af44/', Map.of(
      'url', 'https://backend.bitket.se/v1/ticket-types/4badfcb8-ed51-4ba7-9a5e-3898ef91af44/',
      'id', '4badfcb8-ed51-4ba7-9a5e-3898ef91af44',
      'event', 'https://backend.bitket.se/v1/events/effad9ec-a50c-4484-af54-3df8288689be/',
      'name', 'Christmas dinner + Entrance ticket',
      'description', 'A paragraph.\n\nAnd this is also a paragraph.',
      'conflictsWith', List.of(
        'https://backend.bitket.se/v1/ticket-types/c6b86cc6-4f04-4651-bd64-6d50640fc7c4/'
      ),
      'takesNotes', true,
      'availability', Map.of(
        'general', false,
        'personal', false,
        'quantity', true
      ),
      'price', Money('333.00'),
      'modifiers', List.of(
        Map.of(
          'name', 'Student union discount: LinTek',
          'delta', Money('-10.00')
        )
      )
    )
  ),
  'variations', Map.of(
    '_isPending', false,
    '_error', null
  ),
  'variationChoices', Map.of(
    '_isPending', false,
    '_error', null
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
                'conflictsWith', item.conflicts_with
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
              ))
            ), Map()))
        case api.actionErrorValues.FAILED:
          return state
            .setIn(['variationChoices', '_isPending'], false)
            .setIn(['variationChoices', '_error'], action.payload.message)
        default:
          return state
      }

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
