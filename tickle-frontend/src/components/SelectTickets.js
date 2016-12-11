import React from 'react'
import { Alert, Grid, ButtonGroup, Button, Row, Col, Popover, OverlayTrigger,
  FormGroup, Radio, ControlLabel, Panel, Table, FormControl } from 'react-bootstrap'
import Icon from 'react-fontawesome'
import Markdown from 'react-markdown'
import { connect } from 'react-redux'

import * as actions from '../actions'
import * as selectors from '../selectors'

const mapStateToProps = (state, props) => {
  const selectedTicketTypes = selectors.getSelectedTicketTypes(state)
  const selectedVariationChoices = selectors.getSelectedVariationChoices(state)

  return {
    selectedTicketTypes,
    accessCodes: selectors.getAllAccessCodes(state),
    tickets: selectors.getAllTickets(state),
    ticketTypes: selectors.getTicketTypesOfEvent(state, props.eventUrl),
    ticketTypeHasValidVariationChoiceSelections: (ticketTypeUrl) => selectors.ticketTypeHasValidVariationChoiceSelections(state, ticketTypeUrl),
    ticketTypeIsSelected: (ticketTypeUrl) => selectedTicketTypes.includes(ticketTypeUrl),
    variationChoiceIsSelected: (variationChoiceUrl) => selectedVariationChoices.includes(variationChoiceUrl),
    getPriceOfTicketType: (ticketTypeUrl) => selectors.getPriceOfTicketType(state, ticketTypeUrl),
    getSelectedConflictsOfTicketType: (ticketTypeUrl) => selectors.getSelectedConflictsOfTicketType(state, ticketTypeUrl),
    getVariationsOfTicketType: (ticketTypeUrl) => selectors.getVariationsOfTicketType(state, ticketTypeUrl),
    getVariationChoicesOfVariation: (variationUrl) => selectors.getVariationChoicesOfVariation(state, variationUrl),
  }
}

const mapDispatchToProps = (dispatch, props) => ({
  deselectTicketType: (ticketTypeUrl) => (domEvent) => dispatch(actions.deselectTicketType(ticketTypeUrl)),
  selectTicketType: (ticketTypeUrl) => (domEvent) => dispatch(actions.selectTicketType(ticketTypeUrl)),
  selectVariationChoice: (variationUrl, variationChoiceUrl) => (domEvent) => dispatch(actions.selectVariationChoice(variationUrl, variationChoiceUrl))
})

const PriceDelta = (props) => (
  <span>
    {(props.amount.s === 1) ? <span>+</span> : <span>&minus;</span>}
    &nbsp;
    {props.amount.abs().toRepr()}
  </span>
)

const SelectTickets = connect(mapStateToProps, mapDispatchToProps)((props) => (
  <div>
    <Row>
      {props.ticketTypes.sortBy(i => i.get('index')).map(ticketType => {
        const ownsTicket = props.tickets.some((ticket) => ticket.get('ticketType') === ticketType.get('url'))
        const ticketTypeHasAccessCode = props.accessCodes.some((accessCode) => accessCode.get('ticketType') === ticketType.get('url'))
        const variations = props.getVariationsOfTicketType(ticketType.get('url'))
        const selectedConflicts = props.getSelectedConflictsOfTicketType(ticketType.get('url'))
        const ticketTypeHasValidVariationChoiceSelection = props.ticketTypeHasValidVariationChoiceSelections(ticketType.get('url'))
        const ticketTypeIsSelected = props.ticketTypeIsSelected(ticketType.get('url'))
        const header = (
          <h3>
            {ticketType.get('name')}
            {ticketTypeIsSelected ? (
              <Icon className="pull-right" name="check-circle"/>
            ) : (
              null
            )}
          </h3>
        )

        const priceInformation = (ticketType) => (
          <Popover title="About the price"
                   id={'priceInformation_'.concat(ticketType.get('id'))}>
            <Table striped className="table table-condensed">
              <thead>
              <tr>
                <th>Description</th>
                <th className="text-right">Amount</th>
              </tr>
              </thead>
              <tbody>
              <tr>
                <th>Base price</th>
                <td
                  className="text-right">{ticketType.get('price').toRepr()}</td>
              </tr>
              {ticketType.get('modifiers').map((modifier, key) => (
                <tr key={key}>
                  <th>{modifier.get('condition')}</th>
                  <td className="text-right">
                    <PriceDelta amount={modifier.get('delta')}/>
                  </td>
                </tr>
              ))}
              {variations.map((variation, key) => {
                const selectedChoice = props.getVariationChoicesOfVariation(variation.get('url'))
                  .find((choice) => (
                    props.variationChoiceIsSelected(choice.get('url'))))
                return (selectedChoice && !selectedChoice.get('delta').eq(0)) ? (
                  <tr key={key}>
                    <th>
                      {variation.get('name')}: {selectedChoice.get('name')}
                    </th>
                    <td className="text-right">
                      <PriceDelta amount={selectedChoice.get('delta')}/>
                    </td>
                  </tr>
                ) : (null)
              })}
              </tbody>
              <tfoot>
              <tr className="info">
                <th>Your price</th>
                <td className="text-right">
                  =&nbsp;{props.getPriceOfTicketType(ticketType.get('url')).toRepr()}</td>
              </tr>
              </tfoot>
            </Table>
            <small>Prices in SEK.</small>
          </Popover>
        )

        return (
          <Col sm={6}>
            <Panel header={header}
                   bsStyle={ticketTypeIsSelected ? 'primary' : 'default'}>
              {/* DESCRIPTION */}
              <Markdown source={ticketType.get('description')}/>
              {/* VARIATIONS */}
              <Row>
                {variations.map((variation) => {
                  const choices = props.getVariationChoicesOfVariation(variation.get('url')).sortBy(i => i.get('index'))
                  return (
                    <Col xs={6}>
                      <FormGroup>
                        <ControlLabel
                          style={{marginBottom: 0}}>{variation.get('name')}</ControlLabel>
                        {choices.map((choice) => (
                          <Radio name={variation.get('url')}
                                 value={choice.get('url')}
                                 checked={props.variationChoiceIsSelected(choice.get('url'))}
                                 onChange={props.selectVariationChoice(variation.get('url'), choice.get('url'))}>
                            {choice.get('name')}
                            {choice.get('delta').eq(0) ? null : (
                              <small
                                className={(choice.get('delta').s === 1) ? 'text-danger' : 'text-success'}>
                                {' '}
                                {(choice.get('delta').s === 1) ?
                                  <span>+</span> : <span>&minus;</span>}
                                &nbsp;
                                {choice.get('delta').abs().toRepr()} SEK
                              </small>
                            )}
                          </Radio>
                        ))}
                      </FormGroup>
                    </Col>
                  )
                })}
              </Row>
              {/* NOTES */}
              {ticketType.get('takesNotes') ? (
                <FormGroup>
                  <ControlLabel>Notes</ControlLabel>
                  <FormControl componentClass="textarea"
                               placeholder="Notes"/>
                </FormGroup>
              ) : null}
              {/* PRICE AND AVAILABILITY */}
              <p className="lead" style={{marginBottom: '10px'}}>
                {props.getPriceOfTicketType(ticketType.get('url')).toRepr()}&nbsp;SEK
                {' '}
                <OverlayTrigger trigger="click" rootClose placement="bottom"
                                overlay={priceInformation(ticketType)}>
                  <Icon className="text-info" name="question-circle"/>
                </OverlayTrigger>
              </p>
              {ownsTicket ? (
                <Alert bsStyle="success">
                  You own this ticket.
                </Alert>
              ) : (
                <div>
                  {!(ticketType.getIn(['availability', 'general']) || ticketTypeHasAccessCode) ? (
                    <Alert bsStyle="danger">
                      This ticket type is not available for purchase at this time.
                      If you have an access link, you can try using it.
                    </Alert>
                  ) : null}
                  {!ticketType.getIn(['availability', 'totalQuantity']) ? (
                    <Alert bsStyle="danger">
                      This ticket type has been sold out.
                    </Alert>
                  ) : null}
                </div>
              )}

              {/* ACTIONS */}
              {ticketTypeIsSelected ? (
                <Button block bsStyle="primary"
                        onClick={props.deselectTicketType(ticketType.get('url'))}>
                  <Icon name="remove" fixedWidth/>
                  Deselect
                </Button>
              ) : (
                <Button block bsStyle="primary"
                        disabled={
                          ownsTicket ||
                          !selectedConflicts.isEmpty() ||
                          !ticketTypeHasValidVariationChoiceSelection ||
                          !ticketType.getIn(['availability', 'totalQuantity']) ||
                          !(ticketType.getIn(['availability', 'general']) || ticketTypeHasAccessCode)
                        }
                        onClick={props.selectTicketType(ticketType.get('url'))}>
                  <Icon name="check" fixedWidth/>
                  Select
                </Button>
              )}
              {selectedConflicts.isEmpty() ? null : (
                <small className="text-muted">
                  This ticket can't be selected together
                  with <em>{selectedConflicts.first().get('name')}</em>.
                </small>
              )}
            </Panel>
          </Col>
        )
      })}
    </Row>
  </div>
))

export default SelectTickets
