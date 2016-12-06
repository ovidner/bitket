import React from 'react'

import { LogInForm } from '../../components'
import * as steps from './'

const LogIn = (props) => (
  <div>
    {console.log('login', props)}
    <LogInForm nextUrl={`/${props.params.eventSlug}/${steps.meta.SELECT_TICKETS.url}/`}/>
  </div>
)

export default LogIn
