import React from 'react'
import { Nav, Navbar as BootstrapNavbar, NavDropdown, NavItem } from 'react-bootstrap'
import { connect } from 'react-redux'
import { IndexLink } from 'react-router'
import { LinkContainer } from 'react-router-bootstrap'

import * as actions from '../actions'
import * as selectors from '../selectors'

const mapStateToProps = (state, props) => ({
  events: selectors.getAllEvents(state),
  user: selectors.getCurrentUser(state)
})

const mapDispatchToProps = (dispatch, props) => ({
  logOut: () => dispatch(actions.logOut())
})

const Navbar = connect(mapStateToProps, mapDispatchToProps)((props) => (
  <BootstrapNavbar inverse fixedTop>
    <BootstrapNavbar.Header>
      <BootstrapNavbar.Brand>
        <IndexLink to="/">
          <span className="bitket-brand">Bitket</span>
        </IndexLink>
      </BootstrapNavbar.Brand>
      <BootstrapNavbar.Toggle />
    </BootstrapNavbar.Header>
    <BootstrapNavbar.Collapse>
      <Nav>
        <NavDropdown title="Events" id="eventsMenu">
          {props.events.isEmpty() ? (
            <NavItem disabled>No events releasing tickets.</NavItem>
          ) : (props.events.map((event) => (
            <LinkContainer to={`/${event.get('slug')}/`}>
              <NavItem>{event.get('name')}</NavItem>
            </LinkContainer>
          )))}
        </NavDropdown>
      </Nav>
      <Nav pullRight>
        <NavDropdown title={props.user ? props.user.name : "Not logged in"} id="userMenu" disabled={!props.user}>
          <NavItem onClick={props.logOut}>Log out</NavItem>
        </NavDropdown>
      </Nav>
    </BootstrapNavbar.Collapse>
  </BootstrapNavbar>
))

export default Navbar
