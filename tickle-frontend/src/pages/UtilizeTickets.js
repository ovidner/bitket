import React from 'react'
import { Alert, Button, Col, ControlLabel, FormControl, FormGroup, Row, Well } from 'react-bootstrap'
import { connect } from 'react-redux'

import * as actions from '../actions'
import { Page } from '../components'
import * as selectors from '../selectors'

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
    ticketSearches
  }
}

const mapDispatchToProps = (dispatch, props) => ({
  search: (query) => dispatch(actions.searchTickets(query)),
  utilizeTicketOwnership: (ticketOwnershipUrl) => (domEvent) => dispatch(actions.utilizeTicketOwnership(ticketOwnershipUrl))
})

const UtilizeTickets = connect(mapStateToProps, mapDispatchToProps)(class extends React.Component {
  constructor(props) {
    super(props)

    this.search = this.search.bind(this)
    this.setSearchQuery = this.setSearchQuery.bind(this)

    this.state = {
      searchQuery: ''
    }
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
        <Row>
          <Col xs={12}>
            <form onSubmit={this.search}>
              <FormGroup>
                <ControlLabel>Search term</ControlLabel>
                <FormControl type="text" value={this.state.searchQuery} onChange={this.setSearchQuery}/>
              </FormGroup>
              <Button type="submit" bsStyle="primary" block>Search</Button>
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
                              <Button block disabled style={{height: '6em'}} bsStyle="success" bsSize="lg" onClick={this.props.utilizeTicketOwnership(ticketOwnership.get('url'))}>Utilized</Button>
                            ) : (
                              <Button block disabled={!ticketOwnership.get('isCurrent')} style={{height: '6em'}} bsStyle="success" bsSize="lg" onClick={this.props.utilizeTicketOwnership(ticketOwnership.get('url'))}>Utilize</Button>
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
      </Page>
    )
  }
})

export default UtilizeTickets
