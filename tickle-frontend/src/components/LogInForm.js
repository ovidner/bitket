import React from 'react'
import { Button, Col, FormGroup, Row } from 'react-bootstrap'
import Icon from 'react-fontawesome'
import { withRouter } from 'react-router'

import { authProviders } from '../settings'
import { getRedirectUri } from '../utils'

const LogInForm = (props) => {
  const state = encodeURIComponent(window.location.pathname)

  const logIn = (providerId) => (domEvent) => {
    const redirectUri = encodeURIComponent(getRedirectUri(window.location.origin, providerId))
    const nextUri = encodeURIComponent(props.nextUrl || window.location.pathname)
    window.location = `${authProviders[providerId].authUrl}?response_type=code&redirect_uri=${redirectUri}&client_id=${authProviders[providerId].clientId}&${authProviders[providerId].scopeParam}=${authProviders[providerId].scope}&state=${nextUri}`
  }

  return (
    <div>
        <p className="lead">
          To see your personal price and to purchase tickets, identify yourself
          by logging in. If you don't already have an account, it will be
          created automatically.
        </p>
        <p>
          By logging in, you accept that Bitket stores your name and email
          address (and on occurrence local student identifier as well as student
          union membership).
        </p>
        <FormGroup>
          <Button onClick={logIn('liu')} bsStyle="info" bsSize="lg" block>
            Log in with LiU ID
          </Button>
        </FormGroup>
        <p>
          Please note that student union discounts can be utilized only when
          logging in with LiU ID.
        </p>
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
    </div>
  )
}

export default LogInForm
