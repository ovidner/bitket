import React from 'react'
import { Col, Row } from 'react-bootstrap'

const Footer = (props) => (
  <footer style={{fontSize: '85%'}}>
    <hr />
    <Row>
      <Col sm={4}>
        <p className="text-muted">
          Developed and provided by <a href="http://www.vidner.se/"
                                       target="_blank">Vidner Solutions</a>
        </p>
      </Col>
      <Col sm={8} />
    </Row>
  </footer>
)

export default Footer
