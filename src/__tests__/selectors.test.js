import { List, Map } from 'immutable'

import { Money } from '../dataTypes'
import * as selectors from '../selectors'

describe('isNotMeta', () => {
  it('works as a Immutable.Map filter function, excluding keys starting with _', () => {
    expect(Map.of(
      '_excluded1', null,
      'included1', null,
      '_excluded2', null,
      'included2', null
    ).filter(selectors.isNotMeta)).toEqual(Map.of(
      'included1', null,
      'included2', null
    ))
  })
})

describe('getSelectedVariationChoicesOfTicketType', () => {
  it('returns an Immutable.Map with the URLs of all selected variation choices belonging to the supplied ticket type', () => {
    const state = Map.of(
      'ticketTypes', Map.of(
        'https://backend/ticket-types/1/', Map.of(
          'url', 'https://backend/ticket-types/1/'
        ),
        'https://backend/ticket-types/2/', Map.of(
          'url', 'https://backend/ticket-types/2/'
        )
      ),
      'variations', Map.of(
        'https://backend/ticket-type-variations/1/', Map.of(
          'url', 'https://backend/ticket-type-variations/1/',
          'ticketType', 'https://backend/ticket-types/1/'
        ),
        'https://backend/ticket-type-variations/2/', Map.of(
          'url', 'https://backend/ticket-type-variations/2/',
          'ticketType', 'https://backend/ticket-types/1/'
        ),
        'https://backend/ticket-type-variations/3/', Map.of(
          'url', 'https://backend/ticket-type-variations/3/',
          'ticketType', 'https://backend/ticket-types/2/'
        )
      ),
      'variationChoices', Map.of(
        'https://backend/ticket-type-variation-choices/1/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/1/',
          'variation', 'https://backend/ticket-type-variations/1/'
        ),
        'https://backend/ticket-type-variation-choices/2/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/2/',
          'variation', 'https://backend/ticket-type-variations/1/'
        ),
        'https://backend/ticket-type-variation-choices/3/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/3/',
          'variation', 'https://backend/ticket-type-variations/2/'
        ),
        'https://backend/ticket-type-variation-choices/4/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/4/',
          'variation', 'https://backend/ticket-type-variations/2/'
        ),
        'https://backend/ticket-type-variation-choices/5/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/5/',
          'variation', 'https://backend/ticket-type-variations/3/'
        ),
        'https://backend/ticket-type-variation-choices/6/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/6/',
          'variation', 'https://backend/ticket-type-variations/3/'
        )
      ),
      'selections', Map.of(
        'variationChoices', Map.of(
          'https://backend/ticket-type-variations/1/', 'https://backend/ticket-type-variation-choices/1/',
          'https://backend/ticket-type-variations/2/', 'https://backend/ticket-type-variation-choices/3/',
          'https://backend/ticket-type-variations/3/', 'https://backend/ticket-type-variation-choices/5/'
        )
      )
    )

    expect(selectors.getSelectedVariationChoicesOfTicketType(state, 'https://backend/ticket-types/1/'))
      .toEqual(Map.of(
        'https://backend/ticket-type-variations/1/', 'https://backend/ticket-type-variation-choices/1/',
        'https://backend/ticket-type-variations/2/', 'https://backend/ticket-type-variation-choices/3/'
      ))

    expect(selectors.getSelectedVariationChoicesOfTicketType(state, 'https://backend/ticket-types/2/'))
      .toEqual(Map.of(
        'https://backend/ticket-type-variations/3/', 'https://backend/ticket-type-variation-choices/5/'
      ))
  })
})

describe('getTicketTypePrice', () => {
  it('returns a Money object with the price for a ticket type', () => {
    const state = Map.of(
      'ticketTypes', Map.of(
        'https://backend/ticket-types/1/', Map.of(
          'url', 'https://backend/ticket-types/1/',
          'price', Money('1'),
          'modifiers', List.of(
            Map.of(
              'name', 'Discount',
              'delta', Money('2')
            )
          )
        ),
        'https://backend/ticket-types/2/', Map.of(
          'url', 'https://backend/ticket-types/2/',
          'price', Money('4'),
          'modifiers', List.of(
            Map.of(
              'name', 'Discount',
              'delta', Money('-8')
            )
          )
        )
      ),
      'variations', Map.of(
        'https://backend/ticket-type-variations/1/', Map.of(
          'url', 'https://backend/ticket-type-variations/1/',
          'ticketType', 'https://backend/ticket-types/1/'
        ),
        'https://backend/ticket-type-variations/2/', Map.of(
          'url', 'https://backend/ticket-type-variations/2/',
          'ticketType', 'https://backend/ticket-types/1/'
        ),
        'https://backend/ticket-type-variations/3/', Map.of(
          'url', 'https://backend/ticket-type-variations/3/',
          'ticketType', 'https://backend/ticket-types/2/'
        )
      ),
      'variationChoices', Map.of(
        'https://backend/ticket-type-variation-choices/1/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/1/',
          'variation', 'https://backend/ticket-type-variations/1/',
          'delta', Money('-16')
        ),
        'https://backend/ticket-type-variation-choices/2/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/2/',
          'variation', 'https://backend/ticket-type-variations/1/',
          'delta', Money('32')
        ),
        'https://backend/ticket-type-variation-choices/3/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/3/',
          'variation', 'https://backend/ticket-type-variations/2/',
          'delta', Money('64')
        ),
        'https://backend/ticket-type-variation-choices/4/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/4/',
          'variation', 'https://backend/ticket-type-variations/2/',
          'delta', Money('128')
        ),
        'https://backend/ticket-type-variation-choices/5/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/5/',
          'variation', 'https://backend/ticket-type-variations/3/',
          'delta', Money('256')
        ),
        'https://backend/ticket-type-variation-choices/6/', Map.of(
          'url', 'https://backend/ticket-type-variation-choices/6/',
          'variation', 'https://backend/ticket-type-variations/3/',
          'delta', Money('512')
        )
      ),
      'selections', Map.of(
        'variationChoices', Map.of(
          'https://backend/ticket-type-variations/1/', 'https://backend/ticket-type-variation-choices/1/',
          'https://backend/ticket-type-variations/2/', 'https://backend/ticket-type-variation-choices/3/',
          'https://backend/ticket-type-variations/3/', 'https://backend/ticket-type-variation-choices/5/'
        )
      )
    )

    expect(selectors.getPriceOfTicketType(state, 'https://backend/ticket-types/1/'))
      .toEqual(Money('51'))

    expect(selectors.getPriceOfTicketType(state, 'https://backend/ticket-types/2/'))
      .toEqual(Money('252'))
  })
})
