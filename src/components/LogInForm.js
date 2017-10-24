import React from 'react'
import { Button, FormGroup } from 'react-bootstrap'

import { authProviders } from '../settings'
import { getRedirectUri } from '../utils'

const LogInForm = (props) => {
  const logIn = (providerId) => (domEvent) => {
    const redirectUri = encodeURIComponent(getRedirectUri(window.location.origin, providerId))
    const nextUri = encodeURIComponent(props.nextUrl || window.location.pathname + window.location.search)
    const scope = encodeURIComponent(authProviders[providerId].scope)
    const clientId = encodeURIComponent(authProviders[providerId].clientId)
    window.location = `${authProviders[providerId].authUrl}?response_type=code&redirect_uri=${redirectUri}&client_id=${clientId}&${authProviders[providerId].scopeParam}=${scope}&state=${nextUri}`
  }

  return (
    <div>
      <FormGroup>
        <Button onClick={logIn('liu')} bsStyle="info" bsSize="lg" block>
          Log in with LiU ID
        </Button>
      </FormGroup>
      <hr/>
      <FormGroup>
        <Button onClick={logIn('facebook')} bsStyle="primary" bsSize="lg" block>
          Log in with Facebook
        </Button>
      </FormGroup>
      <FormGroup>
        <Button onClick={logIn('google')} bsStyle="danger" bsSize="lg" block>
          Log in with Google
        </Button>
      </FormGroup>
      <p>
        By logging in, you accept that Bitket stores your name and email
        address (and on occurrence local student identifier as well as student
        union membership).
      </p>
    </div>
  )
}

export default LogInForm
