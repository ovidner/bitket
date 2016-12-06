import { Map } from 'immutable'

import { fetchAction } from '../api'
import { initialState } from '../reducers'

const mockResponseFactory = (url, status, statusText, response) => (
  new window.Response(response, {
    status: status,
    statusText: statusText,
    headers: {
      'Content-Type': 'application/json'
    },
    url: url
  })
)

describe('fetchAction', () => {
  const payload = {foo: 'bar'}
  const actionType = 'ACTION_TYPE'
  const url = 'https://www.host.com/url/'
  const getState = jest.fn().mockImplementation(() => initialState)

  it('dispatches start and success actions on successful fetch', () => {
    window.fetch = jest.fn().mockImplementation(() => (
      Promise.resolve(mockResponseFactory(url, 200, null, JSON.stringify(payload)))
    ))

    const dispatch = jest.fn()

    return fetchAction({
      actionType: actionType,
      url: url
    })(dispatch, getState).then(() => {
      expect(dispatch.mock.calls.length).toBe(2)
      expect(dispatch.mock.calls[0]).toEqual([{
        type: actionType,
        error: null,
        meta: {
          url: url
        }
      }])
      expect(dispatch.mock.calls[1]).toEqual([{
        type: actionType,
        error: false,
        payload: payload,
        meta: {
          url: url
        }
      }])
    })
  })

  it('dispatches start and failure actions on failed fetch', () => {
    window.fetch = jest.fn().mockImplementation(() => (
      Promise.resolve(mockResponseFactory(url, 400, 'Client error', JSON.stringify(payload)))
    ))

    const dispatch = jest.fn()

    return fetchAction({
      actionType: actionType,
      url: url
    })(dispatch, getState).then(() => {
      expect(dispatch.mock.calls.length).toBe(2)
      expect(dispatch.mock.calls[0]).toEqual([{
        type: actionType,
        error: null,
        meta: {
          url: url
        }
      }])
      expect(dispatch.mock.calls[1]).toEqual([{
        type: actionType,
        error: true,
        payload: new Error('Client error'),
        meta: {
          url: url
        }
      }])
    })
  })

  it('dispatches start and failure actions on communication error', () => {
    window.fetch = jest.fn().mockImplementation(() => (
      Promise.reject(new TypeError('Network request failed'))
    ))

    const dispatch = jest.fn()

    return fetchAction({
      actionType: actionType,
      url: url
    })(dispatch, getState).then(() => {
      expect(dispatch.mock.calls.length).toBe(2)
      expect(dispatch.mock.calls[0]).toEqual([{
        type: actionType,
        error: null,
        meta: {
          url: url
        }
      }])
      expect(dispatch.mock.calls[1]).toEqual([{
        type: actionType,
        error: true,
        payload: new Error('Network request failed'),
        meta: {
          url: url
        }
      }])
    })
  })
})
