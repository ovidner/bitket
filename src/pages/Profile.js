import React from 'react'
import { Alert, Button, Col, ControlLabel, FormControl, FormGroup, OverlayTrigger, Panel, Popover, Row } from 'react-bootstrap'
import Icon from 'react-fontawesome'
import { connect } from 'react-redux'

import { LogInForm, Page } from '../components'
import * as selectors from '../selectors'

const mapStateToProps = (state, props) => ({
  user: selectors.getCurrentUser(state),
  tickets: selectors.getAllTicketOwnerships(state),
  getEvent: (eventUrl) => selectors.getEvent(state, eventUrl),
  getTicketType: (ticketTypeUrl) => selectors.getTicketType(state, ticketTypeUrl)
})

const mapDispatchToProps = (dispatch, props) => ({

})

const ResellPopover = (props) => (
  <Popover id={`resell_${props.id}`} title="Resell ticket">
    <p>
      This ticket can be resold to another person, by sharing the resell link below.
      The buyer can then use the link to pay for the ticket and to transfer the
      ownership. Last, the price you have payed for the ticket will be refunded
      to the card used to make the purchase.
    </p>
    <FormGroup>
      <ControlLabel>Resell link</ControlLabel>
      <FormControl value={`${window.location.origin}/resell/${props.resellToken}/`} readOnly/>
    </FormGroup>
    <Alert bsStyle="warning">
      <em>Anyone</em> with the resell link above can purchase your ticket <em>at
      any time</em>, until the ticket has been utilized. Do not share it with
      anyone unless you really want to sell your ticket.
    </Alert>
  </Popover>
)

const Profile = connect(mapStateToProps, mapDispatchToProps)(
  class extends React.Component {
    render() {
      return (
        <Page>
          {this.props.user ? (
            <div>
              <h1>{this.props.user.name} <small>{this.props.user.email}</small></h1>
              <Row>
                <Col md={8}>
                  <h2>Your tickets</h2>
                  <Row>
                  {this.props.tickets.isEmpty() ? (
                    <Col xs={12}>
                      You own no tickets. Not what you expected? Please reload
                      the page or log out and try the login method you used to
                      buy your ticket.
                    </Col>
                  ) : (
                    this.props.tickets.map(ticket => {
                      const ticketType = this.props.getTicketType(ticket.getIn(['ticket', 'ticketType']))
                      const event = this.props.getEvent(ticketType.get('event'))

                      return ticketType ? (
                        <Col sm={6}>
                          <Panel header={<h3>{ticketType.get('name')}</h3>} bsStyle="primary">
                            <FormGroup>
                              <ControlLabel>Event</ControlLabel>
                              <p>{event.get('name')}</p>
                            </FormGroup>
                            <FormGroup>
                              <ControlLabel>Purchase price</ControlLabel>
                              <p>{ticket.get('price').toRepr()} SEK</p>
                            </FormGroup>
                            <FormGroup>
                              <ControlLabel>Entrance code</ControlLabel>
                              <img src={ticket.get('qr')} alt={ticket.get('id')} style={{marginBottom: '0.5em', width: '100%'}} className="img-thumbnail"/><br/>
                              <small>
                                <code>{ticket.get('id')}</code><br/>
                                <code>{ticket.get('code').replace(/\w{2}/g, '$& ')}</code>
                              </small>
                            </FormGroup>
                          </Panel>
                        </Col>
                      ) : null
                    })
                  )}
                  </Row>
                </Col>
                <Col md={4}>

                </Col>
              </Row>
            </div>
          ) : (
            <div>
              <p/>
              <Alert bsStyle="info">
                You must log in to view your profile.
              </Alert>
              <LogInForm/>
            </div>
          )}

        </Page>
      )
    }
  }
)

export default Profile
