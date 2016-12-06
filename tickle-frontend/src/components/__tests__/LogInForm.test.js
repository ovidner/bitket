import React from 'react'
import ReactDOM from 'react-dom'

import { LogInForm } from '../'

it('renders without crashing', () => {
  const div = document.createElement('div')
  ReactDOM.render(<LogInForm />, div)
})
