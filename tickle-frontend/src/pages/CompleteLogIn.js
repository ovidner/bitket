import React from 'react'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'

import { fetchAuthToken } from '../actions'
import { Page } from '../components'

const mapStateToProps = (state) => ({

})

const mapDispatchToProps = (dispatch) => ({
  fetchAuthToken: (provider, code) => dispatch(fetchAuthToken(provider, code))
})

class CompleteLogIn extends React.Component {
  componentDidMount() {
    const authProvider = this.props.params.authProvider
    const code = this.props.location.query.code
    const next = this.props.location.query.state

    this.props.fetchAuthToken(authProvider, code)

    this.props.router.push(next ? next : '/')
  }

  render() {
    return (
      <Page>
        <p>Complete log in</p>
      </Page>
    )
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(CompleteLogIn))
