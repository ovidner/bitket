import React from 'react'
import { Row, Col, Well, Alert } from 'react-bootstrap'
import Markdown from 'react-markdown'
import { withRouter } from 'react-router'
import { connect } from 'react-redux'
import * as settings from '../settings'
import { StripeProvider, Elements } from 'react-stripe-elements'

import { Page, LogInForm, SelectTickets, PaymentForm } from '../components'
import * as selectors from '../selectors'

const mapStateToProps = (state, props) => ({
  authIsPending: selectors.authIsPending(state),
  event: selectors.getEventFromSlug(state, props.params.eventSlug),
  isLoggedIn: selectors.isLoggedIn(state),
  getTotalAmountForEvent: (eventUrl) => selectors.getTotalAmountForEvent(state, eventUrl),
  accessCodesMeta: selectors.getAllAccessCodes(state, true)
})

const mapDispatchToProps = (dispatch) => ({

})

class _Event extends React.Component {
  render() {
    return this.props.event ? (
      <Page>
        <h1>{this.props.event.get('name')}</h1>
        <Markdown source={this.props.event.get('description')}/>
        <Row>
          <Col md={8}>
            <h2>Tickets</h2>
            <hr/>
            {this.props.accessCodesMeta.get('_error') ? (
              <Alert bsStyle="danger">
                There was an error trying to redeem your access code. It may be
                incomplete or already used by someone else. Make sure that your
                code or link has been copied properly.
              </Alert>
            ) : null}
            {this.props.isLoggedIn ? null : (
              <Alert bsStyle="warning">
                Viewing base prices. Log in <span className="hidden-xs hidden-sm">to the right</span><span className="hidden-md hidden-lg">below</span> to see your personal prices.
              </Alert>
            )}
            <SelectTickets eventUrl={this.props.event.get('url')}/>
          </Col>
          <Col md={4}>
            <h2>Payment</h2>
            <hr/>
            <p className="lead">
              Total amount: {this.props.getTotalAmountForEvent(this.props.event.get('url')).toRepr()} SEK
            </p>

            <hr />

            {this.props.isLoggedIn ? (
              <div>
                <StripeProvider apiKey={settings.stripePublicKey}>
                  <Elements locale='en'>
                    <PaymentForm eventUrl={this.props.event.get('url')}/>
                  </Elements>
                </StripeProvider>
              </div>
            ) : (
              <div>
                <Well>
                  <p className="lead">
                    To see your personal price and to purchase tickets, identify yourself
                    by logging in. If you don't already have an account, it will be
                    created automatically.
                  </p>
                  <p>
                    Please note that student union discounts can be utilized only when
                    logging in with LiU ID.
                  </p>
                  <LogInForm/>
                </Well>
              </div>
            )}
          </Col>
        </Row>

      </Page>
    ) : (null)
  }
}

const Event = withRouter(connect(mapStateToProps, mapDispatchToProps)(_Event))

export default Event
