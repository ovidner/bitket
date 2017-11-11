import 'es6-shim'

import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import { IndexRoute, Redirect, Route, Router, browserHistory } from 'react-router'
import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'
import WebFont from 'webfontloader'

import * as components from './components'
import * as errorReporting from './errorReporting'
import { errorReportingMiddleware, loggerMiddleware } from './middleware'
import * as pages from './pages'
import reducer, { initialState } from './reducers'
import * as settings from './settings'
import * as utils from './utils'

import './index.css'

// Initialize the error handler in an early stage
errorReporting.init()

WebFont.load({
  typekit: {
    id: settings.typekitId
  }
})

const middleware = [
  // errorReportingMiddleware should always come first in the middleware chain
  errorReportingMiddleware,
  thunkMiddleware
]
if (process.env.NODE_ENV !== 'production') {
  middleware.push(loggerMiddleware)
}

const store = createStore(
  reducer,
  utils.mergePersistedState(initialState),
  applyMiddleware(...middleware)
)

const router = (
  <Router history={browserHistory}>
    <Route path="/" component={components.App}>
      <IndexRoute component={pages.Home}/>
      <Route path="log-in/:authProvider/" component={pages.CompleteLogIn}/>
      <Route path="profile/" component={pages.Profile}/>
      <Route path="utilize/" component={pages.UtilizeTickets}/>
      <Route path=":eventSlug/" component={pages.Event}/>
    </Route>
    <Redirect from="/*" to="/*/"/>
  </Router>
)

const render = () => ReactDOM.render(
  <Provider store={store}>
    {router}
  </Provider>,
  document.getElementById('root')
)

// Automatically dispatches auth token refreshes and persists state
utils.autoRefreshAuthToken(store)
utils.autoPersistState(store)
utils.autoFetchUserDependentData(store)

render()
store.subscribe(render)
