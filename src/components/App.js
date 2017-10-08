import React from 'react'
import { Grid } from 'react-bootstrap'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'


import * as actions from '../actions'
import * as selectors from '../selectors'
import { Footer, Navbar, PurchaseModal } from './'

const mapStateToProps = (state, props) => ({
  eventsMeta: selectors.getAllEvents(state, true).toJS(),
  organizationsMeta: selectors.getAllEvents(state, true).toJS(),
  variationsMeta: selectors.getAllVariations(state, true).toJS(),
  variationChoicesMeta: selectors.getAllVariationChoices(state, true).toJS()
})

const mapDispatchToProps = (dispatch, props) => ({
  addAccessCode: (accessCode) => dispatch(actions.addAccessCode(accessCode)),
  fetchEvents: () => dispatch(actions.fetchEvents()),
  fetchOrganizations: () => dispatch(actions.fetchOrganizations()),
  fetchVariations: () => dispatch(actions.fetchVariations()),
  fetchVariationChoices: () => dispatch(actions.fetchVariationChoices())
})

class App extends React.Component {
  componentWillMount() {
    this.props.fetchEvents()
    this.props.fetchOrganizations()
    this.props.fetchVariations()
    this.props.fetchVariationChoices()

    const accessCode = this.props.location.query.accessCode
    if (accessCode) {
      this.props.addAccessCode(accessCode)
    }
  }

  render() {
    return (
      <div>
        <Navbar />
        {(
          this.props.eventsMeta._error || this.props.eventsMeta._isPending ||
          this.props.organizationsMeta._error || this.props.organizationsMeta._isPending ||
          this.props.variationsMeta._error || this.props.variationsMeta._isPending ||
          this.props.variationChoicesMeta._error || this.props.variationChoicesMeta._isPending
        ) ? (
          <Grid>
            <p>Loading...</p>
          </Grid>
        ) : (
          this.props.children
        )}
        <Footer/>
        <PurchaseModal/>
      </div>
    )
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(App))
