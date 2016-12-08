import React from 'react'
import { Button, Modal, ProgressBar } from 'react-bootstrap'
import { connect } from 'react-redux'

import * as actions from '../actions'
import { sumMoney } from '../dataTypes'
import * as selectors from '../selectors'

const mapStateToProps = (state, props) => ({
  purchase: selectors.getPurchase(state),
  getTicketType: (ticketTypeUrl) => selectors.getTicketType(state, ticketTypeUrl)
})

const mapDispatchToProps = (dispatch, props) => ({
  dismissPurchase: () => dispatch(actions.dismissPurchase())
})

class _PurchaseModal extends React.Component {
  render() {
    const messageList = () => (
      <ul>
        {this.props.purchase.get('_error') ? (
          <li>{this.props.purchase.get('_error')}</li>
        ) : null}
        {this.props.purchase.get('messages').map((message) => (
          <li>{message.get('text')}</li>
        ))}
      </ul>
    )

    return (
      <Modal show={this.props.purchase.get('_isOpen')}
             backdrop={this.props.purchase.get('_isPending') ? 'static' : true}
             onHide={this.props.dismissPurchase}>
        <Modal.Body>
          {this.props.purchase.get('_isPending') ? (
            <div>
              <h1 className="h3" style={{textAlign: 'center'}}>Processing your purchase...</h1>
              <ProgressBar now={100} active/>
              <p>
                This may take up to a minute during extreme load. Do not reload the
                page or press the back button.
              </p>
            </div>
          ) : (
            <div>
              <h3>Done!</h3>
              {this.props.purchase.get('tickets').isEmpty() ? (
                <div>
                  <p>
                    You received no tickets, due to the following:
                  </p>
                  {messageList()}
                </div>
              ) : (
                <div>
                  <p>
                    You received the following tickets:
                  </p>
                  <ul>
                    {this.props.purchase.get('tickets').map((ticket) => {
                      const ticketType = this.props.getTicketType(ticket.get('ticketType'))
                      return (
                        <li>{ticketType.get('name')}</li>
                      )
                    })}
                  </ul>
                </div>
              )}
              {this.props.purchase.get('transactions').isEmpty() ? (
                <p>
                  No money has been withdrawn from your card.
                </p>
              ) : (
                <p>
                  {sumMoney(...this.props.purchase.get('transactions').map(t => t.get('amount'))).toRepr()} SEK has been withdrawn from your card.
                </p>
              )}
            </div>
          )}
        </Modal.Body>
        {this.props.purchase.get('_isPending') ? null : (
          <Modal.Footer>
            <Button bsStyle="primary" onClick={this.props.dismissPurchase} block>Close</Button>
          </Modal.Footer>
        )}

      </Modal>
    )
  }
}

const PurchaseModal = connect(mapStateToProps, mapDispatchToProps)(_PurchaseModal)

export default PurchaseModal
