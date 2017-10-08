import React from 'react'
import { Alert, Button, Col, ControlLabel, FormControl, FormGroup, Row, Well } from 'react-bootstrap'
import { findDOMNode } from 'react-dom'
import { connect } from 'react-redux'

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
    currentUser: selectors.getCurrentUser(state)
  }
}

const mapDispatchToProps = (dispatch, props) => ({
  search: (query) => dispatch(actions.searchTickets(query)),
  utilizeTicketOwnership: (ticketOwnershipId) => (domEvent) => dispatch(actions.utilizeTicketOwnership(ticketOwnershipId))
})

const UtilizeTickets = connect(mapStateToProps, mapDispatchToProps)(class extends React.Component {
  constructor(props) {
    super(props)

    this.createRefToInputField = this.createRefToInputField.bind(this)
    this.handleKeyDown = this.handleKeyDown.bind(this)
    this.search = this.search.bind(this)
    this.setSearchQuery = this.setSearchQuery.bind(this)

    this.state = {
      searchQuery: ''
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
  }

  componentWillUnmount() {
    window.removeEventListener('keydown', this.handleKeyDown)
  }

  setSearchQuery(domEvent) {
    this.setState({searchQuery: domEvent.target.value})
  }

  search(domEvent) {
    this.props.search(this.state.searchQuery)
    this.setState({searchQuery: ''})
    domEvent.preventDefault()
    return false
  }

  render() {
    return (
      <Page>
        {this.props.currentUser ? (
            <Row>
              <Col xs={12}>
                <form onSubmit={this.search}>
                  <FormGroup>
                    <ControlLabel>Search term</ControlLabel>
                    <FormControl type="text" value={this.state.searchQuery} onChange={this.setSearchQuery} ref={this.createRefToInputField}/>
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
              </Col>
            </Row>
        ) : (
          <LogInForm/>
        )}
      </Page>
    )
  }
})

export default UtilizeTickets
