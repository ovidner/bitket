import React from 'react'
import * as Bootstrap from 'react-bootstrap'
import { IndexLink } from 'react-router'
import { IndexLinkContainer, LinkContainer } from 'react-router-bootstrap'

const Navbar = (props) => (
  <Bootstrap.Navbar inverse fixedTop>
    <Bootstrap.Navbar.Header>
      <Bootstrap.Navbar.Brand>
        <IndexLink to="/">
          tickle
        </IndexLink>
      </Bootstrap.Navbar.Brand>
      <Bootstrap.Navbar.Toggle />
    </Bootstrap.Navbar.Header>
    <Bootstrap.Navbar.Collapse>
      <Bootstrap.Nav>
        <Bootstrap.NavDropdown title="Ticket releases" id="ticketReleasesMenu">
          <Bootstrap.MenuItem onClick={props.logOut}>Log out</Bootstrap.MenuItem>
        </Bootstrap.NavDropdown>
        <LinkContainer to="/lookup-register/" disabled={!props.isLoggedIn}>
          <Bootstrap.NavItem>Look up and register</Bootstrap.NavItem>
        </LinkContainer>
      </Bootstrap.Nav>
      <Bootstrap.Nav pullRight>

      </Bootstrap.Nav>
    </Bootstrap.Navbar.Collapse>
  </Bootstrap.Navbar>
)

export default Navbar
