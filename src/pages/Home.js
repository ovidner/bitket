import React from 'react'
import { Row, Col, Alert, Panel } from 'react-bootstrap'
import Markdown from 'react-markdown'
import { Page } from '../components'
import { LinkContainer } from 'react-router-bootstrap'

import { connect } from 'react-redux'
import * as selectors from '../selectors'

const mapStateToProps = (state, props) => ({
  events: selectors.getAllEvents(state),
  user: selectors.getCurrentUser(state)
})

const Home = connect(mapStateToProps)((props) => (
  <Page>
    <Row style={{ marginTop: 30 }}>
      {props.events.isEmpty() ? (
        <Alert bsStyle="warning">No events releasing tickets. Please check back later.</Alert>
      ) : (props.events.map((event) => (
        <LinkContainer to={`/${event.get('slug')}/`}>
          <Col sm={6}>
            <Panel bsStyle="default">
              <h3>{event.get('name')}</h3>

              <hr />

              <Markdown source={event.get('description')}/>

              <strong>View more...</strong>
            </Panel>
          </Col>
        </LinkContainer>
      )))}
    </Row>

    <h2>Event organizer?</h2>
    <p>
      Contact us at <a href="mailto:hello@bitket.se">hello@bitket.se</a> if
      you're interested in using Bitket for your event.
    </p>
  </Page>
))

export default Home
