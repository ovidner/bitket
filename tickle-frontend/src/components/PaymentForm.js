import React from 'react'
import { Alert, Button, Col, ControlLabel, FormControl, FormGroup, Row, HelpBlock, Checkbox } from 'react-bootstrap'
import Icon from 'react-fontawesome'
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
      cardNumber: '',
      cardExpMonth: '',
      cardExpYear: '',
      cardCode: '',
      nin: props.user.nin || '',
      noNin: false,
      stripeError: null,
      stripePending: null
    }
  }

  toggleNoNin() {
    return (domEvent) => this.setState({noNin: !this.state.noNin})
  }

  setCardNumber() {
    return (domEvent) => this.setState(
      // Replaces all spaces with blank strings
      {cardNumber: domEvent.target.value.replace(/\D/g, '')})
  }

  setCardExpMonth() {
    return (domEvent) => this.setState(
      {cardExpMonth: domEvent.target.value.replace(/\D/g, '').slice(0, 2)})
  }

  setCardExpYear() {
  return (domEvent) => this.setState(
    {cardExpYear: domEvent.target.value.replace(/\D/g, '').slice(0, 4)})
  }

  setCardCode() {
    return (domEvent) => this.setState(
      {cardCode: domEvent.target.value.replace(/\D/g, '').slice(0, 4)})
  }

  setNin() {
    return (domEvent) => this.setState({nin: domEvent.target.value})
  }

  cardCodeIsValid() {
    return window.Stripe.card.validateCVC(this.state.cardCode)
  }

  cardExpIsValid() {
    return window.Stripe.card.validateExpiry(
      this.state.cardExpMonth, this.state.cardExpYear)
  }

  cardNumberIsValid() {
    return window.Stripe.card.validateCardNumber(this.state.cardNumber)
  }

  ninIsValid() {
    return this.state.noNin || utils.ninIsValid(this.state.nin)
  }

  stripeResponseHandler(status, response) {
    if (response.error) {
      this.setState({stripeError: response.error})
      this.setState({stripePending: false})
    } else {
      this.setState({stripeError: null})

      this.props.performPurchase(response.id, this.state.noNin ? null : this.state.nin)
      this.setState({stripePending: false})
    }
  }

  startPurchase() {
    return (domEvent) => {
      this.setState({stripeError: null})
      this.setState({stripePending: true})

      window.Stripe.createToken({
        number: this.state.cardNumber,
        cvc: this.state.cardCode,
        exp_month: this.state.cardExpMonth,
        exp_year: this.state.cardExpYear
      }, this.stripeResponseHandler.bind(this))

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
          by <a href="https://stripe.com/se" target="_blank">Stripe</a> and your
          card details are never accessible by Bitket
          or {this.props.organization ? this.props.organization.get('name') : 'the event organizer'}.
        </p>
        <FormGroup validationState={(this.state.cardNumber && !this.cardNumberIsValid()) ? 'error' : null}>
          <ControlLabel>Card number</ControlLabel>
          <FormControl type="text" placeholder="●●●● ●●●● ●●●● ●●●●" value={this.state.cardNumber.replace(/\d{4}/g, '$& ').trim()} onChange={this.setCardNumber()}/>
        </FormGroup>
        <Row>
          <Col xs={3}>
            <FormGroup validationState={(this.state.cardExpMonth && this.state.cardExpYear && !this.cardExpIsValid()) ? 'error' : null}>
              <ControlLabel>Month</ControlLabel>
              <FormControl type="text" placeholder="MM" value={this.state.cardExpMonth} onChange={this.setCardExpMonth()}/>
            </FormGroup>
          </Col>
          <Col xs={3}>
            <FormGroup validationState={(this.state.cardExpMonth && this.state.cardExpYear && !this.cardExpIsValid()) ? 'error' : null}>
              <ControlLabel>Year</ControlLabel>
              <FormControl type="text" placeholder="YY" value={this.state.cardExpYear} onChange={this.setCardExpYear()}/>
            </FormGroup>
          </Col>
          <Col xs={6}>
            <FormGroup validationState={(this.state.cardCode && !this.cardCodeIsValid()) ? 'error' : null}>
              <ControlLabel>Security code</ControlLabel>
              <FormControl type="text" placeholder="●●●" value={this.state.cardCode} onChange={this.setCardCode()}/>
            </FormGroup>
          </Col>
        </Row>
        <Alert bsStyle="warning">
          <strong>Heads up, Nordea customers!</strong> Please make sure that you
          have activated your card for online purchases before proceeding. Read
          more and follow the instructions
          at <a href="http://www.nordea.se/privat/vardagstjanster/kort/Internetkop.html" target="_blank">Nordea's website</a>.
        </Alert>
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
                      disabled={!(this.cardCodeIsValid() && this.cardExpIsValid() && this.cardNumberIsValid() && this.ninIsValid()) || this.state.stripePending}>
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

export default PaymentForm
