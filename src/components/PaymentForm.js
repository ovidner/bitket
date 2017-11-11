import React from 'react'
import { injectStripe, CardElement } from 'react-stripe-elements'
import { Alert, Button, Col, ControlLabel, FormControl, FormGroup, Row, HelpBlock, Checkbox } from 'react-bootstrap'
import { connect } from 'react-redux'

import * as actions from '../actions'
import * as selectors from '../selectors'
import * as utils from '../utils'

const mapStateToProps = (state, props) => {
  const event = selectors.getEvent(state, props.eventUrl)
  return ({
    totalAmount:  selectors.getTotalAmountForEvent(state, props.eventUrl),
    user: selectors.getCurrentUser(state),
    organization: selectors.getOrganization(state, event.get('organization'))
  })
}

const mapDispatchToProps = (dispatch, props) => ({
  performPurchase: (stripeToken, nin) => dispatch(actions.performPurchase(props.eventUrl, stripeToken, nin))
})

class _PaymentForm extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      cardIsValid: false,
      nin: props.user.nin || '',
      noNin: false,
      stripeError: null,
      stripePending: null
    }
  }

  toggleNoNin() {
    return (domEvent) => this.setState({noNin: !this.state.noNin})
  }

  setNin() {
    return (domEvent) => this.setState({nin: domEvent.target.value})
  }

  ninIsValid() {
    return this.state.noNin || utils.ninIsValid(this.state.nin)
  }

  validate(stripeData) {
    this.setState({
      cardIsValid: stripeData.complete
    })
  }

  startPurchase() {
    return (domEvent) => {
      this.setState({stripeError: null})
      this.setState({stripePending: true})

      this.props.stripe.createToken()
        .then( ({token}) => {
          this.setState({stripeError: null})

          this.props.performPurchase(token.id, this.state.noNin ? null : this.state.nin)
          this.setState({stripePending: false})
        } )
        .catch( ({error}) => {
          console.log(error) // TODO Handle better, output the errors on bottom of page
          this.setState({stripeError: error})
          this.setState({stripePending: false})
        } )

      domEvent.preventDefault()
      return false
    }
  }

  render() {
    return (
      <form onSubmit={this.startPurchase()}>
        <h3>Personal details</h3>
        <Row>
          <Col sm={6} md={12}>
            <FormGroup>
              <ControlLabel>Name</ControlLabel>
              <FormControl type="text" disabled value={this.props.user.name}/>
            </FormGroup>
          </Col>
          <Col sm={6} md={12}>
            <FormGroup>
              <ControlLabel>E-mail address</ControlLabel>
              <FormControl type="email" disabled value={this.props.user.email}/>
              <HelpBlock>
                All correspondence (such as receipts and confirmations) will be sent
                to this address.
              </HelpBlock>
            </FormGroup>
          </Col>
        </Row>

        <FormGroup validationState={(this.state.nin && !this.ninIsValid()) ? 'error' : null}>
          <ControlLabel>National identity number</ControlLabel>
          <FormControl type="text" placeholder={this.state.noNin ? '—' : 'YYYYMMDDXXXX'} value={this.state.noNin ? '' : this.state.nin} onChange={this.setNin()} disabled={this.state.noNin}/>
          <HelpBlock>
            Swedish <em>personnummer</em>. Used to identify you at the event. Make sure this is correct!
          </HelpBlock>
          <Checkbox checked={this.state.noNin} onChange={this.toggleNoNin()}>
            I don't have a Swedish national identity number
          </Checkbox>
        </FormGroup>
        <h3>Card details</h3>
        <p>
          We accept VISA, MasterCard and American Express cards. The payment is
          secured
          by <a href="https://stripe.com/se">Stripe</a> and your
          card details are never accessible by Bitket
          or {this.props.organization ? this.props.organization.get('name') : 'the event organizer'}.
        </p>

        <CardElement onChange={this.validate.bind(this)} style={{base: {fontSize: '18px'}}} />

        {/*<Alert bsStyle="warning">
          <strong>Heads up, Nordea customers!</strong> Please make sure that you
          have activated your card for online purchases before proceeding. Read
          more and follow the instructions
          at <a href="http://www.nordea.se/privat/vardagstjanster/kort/Internetkop.html">Nordea's website</a>.
        </Alert> */}

        <h3>Terms <small>and other important information</small></h3>
        {this.props.organization ? (
          <div>
            <p>
              Your tickets will be delivered electronically to your profile on this
              website within a few seconds from your purchase.
            </p>
            <p>
              The purchase amount will be withdrawn immediately from the card
              supplied above.
            </p>
            <p>
              Your purchase from (and agreement with) {this.props.organization.get('name')} is protected
              by applicable Swedish law, which (in conjunction with Bitket's terms)
              has the following important implications:
            </p>
            <ul>
              <li>
                Once your tickets has been delivered to you, <strong>you cannot
                withdraw your purchase</strong> unless it is resold to another
                person.
              </li>
              <li>
                Your tickets are personal, meaning that <strong>you may have to identify
                yourself</strong> using valid passport, national identification card, driver's
                license or student identification card in order to utilize the tickets.
              </li>
            </ul>
            <p>
              Your counterpart in this agreement is:
            </p>
            <p>
              {this.props.organization.get('name')} (org. nr. {this.props.organization.get('organizationNumber')})<br/>
              {this.props.organization.get('address').split('\n', -1).map((item, key) => (
                <span key={key}>
              {item}
                  <br/>
            </span>
              ))}
              <a href={'mailto:' + this.props.organization.get('email')}>{this.props.organization.get('email')}</a>
            </p>
            <p>
              By paying, you agree to these terms.
            </p>
            {this.state.stripeError ? (
                <Alert bsStyle="danger">
                  {this.state.stripeError.message}
                </Alert>
              ) : null}
            <FormGroup>
              <Button type="submit" bsSize="lg" bsStyle="success" block
                      disabled={!(this.state.cardIsValid && this.ninIsValid()) || this.state.stripePending}>
                Pay {this.props.totalAmount.toRepr()} SEK
              </Button>
            </FormGroup>
          </div>
        ) : null}
      </form>
    )
  }
}

const PaymentForm = connect(mapStateToProps, mapDispatchToProps)(_PaymentForm)

export default injectStripe(PaymentForm);
