import React from 'react'
import { Jumbotron } from 'react-bootstrap'

import { Page } from '../components'

const Home = (props) => (
  <Page>
    <Jumbotron style={{marginTop: '1em'}}>
      <h1>Smart tickets for smart people</h1>
      <p>
        Bitket is the convenient way to sell and distribute tickets to student events.
      </p>
    </Jumbotron>
    <p>
      Bitket is still under heavy development. Please forgive us if you hit any
      rough edges!
    </p>
    <h2>Event organizer?</h2>
    <p>
      Contact us at <a href="mailto:hello@bitket.se">hello@bitket.se</a> if
      you're interested in using Bitket for your event.
    </p>
  </Page>
)

export default Home
