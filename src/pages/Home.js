import React from 'react'
import { Row, Col, Alert, Panel, Button } from 'react-bootstrap'
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

              <Button bsStyle="primary" style={{marginBottom: 10}}>View more...</Button>
            </Panel>
          </Col>
        </LinkContainer>
      )))}
    </Row>
  </Page>
))

export default Home
