import React from 'react'
import { Alert, Button, Col, ControlLabel, FormControl, FormGroup, HelpBlock, Row, Well } from 'react-bootstrap'
import { findDOMNode } from 'react-dom'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'

import * as actions from '../actions'
import { LogInForm, Page } from '../components'
import * as selectors from '../selectors'

const keys = /^[a-z0-9]$/
// keyIdentifier represents a *key* and not a *character*. Therefore these are
// Unicode IDs for numbers and uppercase letters.
const keyIdentifiers = /^U\+00(3[0-9]|4[1-9A-F]|5[0-9A])$/

const mapStateToProps = (state, props) => {
  const rawTicketSearches = selectors.getAllTicketSearches(state)
  const ticketOwnerships = selectors.getAllTicketOwnerships(state)
  const users = selectors.getAllUsers(state)
  const tickets = selectors.getAllTickets(state)

  console.log('tickets', tickets.toJS())

  const ticketSearches = rawTicketSearches
    .map((ticketSearch) => ticketSearch.set('results',
      ticketSearch.get('results').map(
        (resultUrl) => {
          const ticketOwnership = ticketOwnerships.get(resultUrl)

          return ticketOwnership
            .set('user', users.get(ticketOwnership.get('user')))
            //.set('ticket', tickets.get(ticketOwnership.get('ticket')))
        }
      )))
  console.log('ticketSearches', ticketSearches.toJS())
  return {
    ticketSearches,
    event: selectors.getEventFromSlug(state, props.params.eventSlug),
    serviceAuthToken: selectors.getServiceAuthToken(state),
    currentUser: selectors.getCurrentUser(state)
  }
}

const mapDispatchToProps = (dispatch, props) => ({
  search: (eventId, query) => dispatch(actions.searchTickets(eventId, query)),
  setServiceAuthToken: (token) => dispatch(actions.setServiceAuthToken(token)),
  utilizeTicketOwnership: (ticketOwnershipId) => (domEvent) => dispatch(actions.utilizeTicketOwnership(ticketOwnershipId))
})

const UtilizeTickets = withRouter(connect(mapStateToProps, mapDispatchToProps)(class extends React.Component {
  constructor(props) {
    super(props)

    this.createRefToInputField = this.createRefToInputField.bind(this)
    this.handleKeyDown = this.handleKeyDown.bind(this)
    this.performSearch = this.performSearch.bind(this)
    this.search = this.search.bind(this)
    this.setSearchQuery = this.setSearchQuery.bind(this)
    this.setSearchQueryValue = this.setSearchQueryValue.bind(this)
    this.setServiceAuthToken = this.setServiceAuthToken.bind(this)

    this.state = {
      searchQuery: '',
      serviceAuthToken: '',
    }
  }

  handleKeyDown(domEvent) {
    if (
      (
        // If this field is active already, we ignore this event.
        window.document.activeElement !== this.inputField
      ) && (
        // If any modifier key is used, we ignore this event.
        !(domEvent.altKey || domEvent.ctrlKey || domEvent.metaKey || domEvent.shiftKey)
      ) && (
        // Some browsers haven't managed to take step into the modern ages and
        // still use the non-standardized way of keyIdentifiers, so we must
        // check for both.
        // (It's Safari.) ((Even IE 9 does it right.)) (((Yuck.)))
        keys.test(domEvent.key) || keyIdentifiers.test(domEvent.keyIdentifier)
      )
    ) {
      this.inputField.focus()
    }
  }

  createRefToInputField(ref) {
    this.inputField = findDOMNode(ref)
  }

  componentDidMount() {
    window.addEventListener('keydown', this.handleKeyDown)
    window._bitketUtilizeSetSearchQuery = this.setSearchQueryValue
    window._bitketUtilizeSearch = this.performSearch
  }

  componentWillUnmount() {
    window.removeEventListener('keydown', this.handleKeyDown)
    window._bitketUtilizeSetSearchQuery = undefined
    window._bitketUtilizeSearch = undefined
  }

  setSearchQuery(domEvent) {
    this.setSearchQueryValue(domEvent.target.value)
  }

  setSearchQueryValue(value) {
    this.setState({searchQuery: value})
  }

  setServiceAuthToken(domEvent) {
    this.props.setServiceAuthToken(this.state.serviceAuthToken)
  }

  search(domEvent) {
    this.performSearch()
    domEvent.preventDefault()
    return false
  }

  performSearch() {
    this.props.search(this.props.event.get('id'), this.state.searchQuery)
    this.setState({searchQuery: ''})
  }

  render() {
    return (
      <Page>
        {this.props.serviceAuthToken ? (
            <Row>
              <Col xs={12}>
                <form onSubmit={this.search}>
                  <FormGroup>
                    <ControlLabel>Search term</ControlLabel>
                    <FormControl type="text" value={this.state.searchQuery} onChange={this.setSearchQuery} ref={this.createRefToInputField}/>
                    <HelpBlock>
                      Name, email, national identity number, LiU ID, LiU card number, ticket ID, ticket code or QR code. At most 10 search hits will be returned.
                    </HelpBlock>
                  </FormGroup>
                  <Button type="submit" bsStyle="primary" block disabled={this.state.searchQuery.length < 3}>Search</Button>
                </form>
              </Col>
              <Col xs={12}>
                {this.props.ticketSearches.map((ticketSearch, key) => (
                  <div key={key}>
                    <h3>{ticketSearch.get('query')}</h3>
                    {ticketSearch.get('results') ? (
                        ticketSearch.get('results').map((ticketOwnership, key) => {
                          console.log('ticketOwnership', ticketOwnership.toJS())
                          return (
                            <Well key={key}>
                              <Row>
                                <Col sm={4}>
                                  <FormGroup>
                                    <ControlLabel>Name</ControlLabel>
                                    <p>{ticketOwnership.getIn(['user', 'name'])}</p>
                                  </FormGroup>
                                  <FormGroup>
                                    <ControlLabel>National identity number</ControlLabel>
                                    <p>{ticketOwnership.getIn(['user', 'nin'])}</p>
                                  </FormGroup>
                                  <FormGroup>
                                    <ControlLabel>E-mail address</ControlLabel>
                                    <p>{ticketOwnership.getIn(['user', 'email'])}</p>
                                  </FormGroup>
                                </Col>
                                <Col sm={4}>
                                  <FormGroup>
                                    <ControlLabel>ID</ControlLabel>
                                    <p><code>{ticketOwnership.get('id')}</code></p>
                                  </FormGroup>
                                  <FormGroup>
                                    <ControlLabel>Code</ControlLabel>
                                    <p><code>{ticketOwnership.get('code')}</code></p>
                                  </FormGroup>
                                </Col>
                                <Col sm={4}>
                                  {ticketOwnership.getIn(['ticket', 'utilized']) ? (
                                      <Button block disabled style={{height: '6em'}} bsStyle="success" bsSize="lg">Utilized</Button>
                                    ) : (
                                      <Button block disabled={!ticketOwnership.get('isCurrent')} style={{height: '6em'}} bsStyle="success" bsSize="lg" onClick={this.props.utilizeTicketOwnership(ticketOwnership.get('id'))}>Utilize</Button>
                                    )}
                                  {ticketOwnership.get('isCurrent') ? null : (
                                      <Alert bsStyle="danger">
                                        This ticket ownership has been resold.
                                      </Alert>
                                    )}
                                </Col>
                              </Row>
                            </Well>
                          )
                        })
                      ) : (
                        <p>No results.</p>
                      )}
                  </div>
                ))}
                <hr/>
                <p>
                  <small className='text-muted'>Event: {this.props.event ? this.props.event.get('name') : '-'}</small><br/>
                  <small className='text-muted'>Service auth token: {this.props.serviceAuthToken.slice(0, 8)}&hellip;</small>
                </p>
              </Col>
            </Row>
        ) : (
          <form onSubmit={this.setServiceAuthToken}>
            <FormGroup>
              <ControlLabel>Service auth token</ControlLabel>
              <FormControl type="text" value={this.state.serviceAuthToken} onChange={(domEvent) => this.setState({serviceAuthToken: domEvent.target.value})} />
            </FormGroup>
            <Button type="submit" bsStyle="primary" block>Set</Button>
          </form>
        )}
      </Page>
    )
  }
}))

export default UtilizeTickets
