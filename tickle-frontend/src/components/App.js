import React from 'react'
import {IndexRoute, Route, Router, browserHistory} from 'react-router'

import * as components from './'
import * as pages from '../pages'

import './App.css'

const App = (props) => (
  <Router history={browserHistory}>
    <Route path="/" component={components.Layout}>
      <IndexRoute component={pages.Home} />
      <Route path="events/:organizationSlug/:eventSlug/" component={pages.Home} />
      <Route path="log-in/:authProvider/">
        <IndexRoute />
        <Route path="callback/" />
      </Route>
    </Route>
  </Router>
)

export default App
