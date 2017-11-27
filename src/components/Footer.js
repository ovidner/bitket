import React from 'react'
import { Grid, Col } from 'react-bootstrap'

const Footer = (props) => (
  <footer className="sticky-footer">
    <Grid>
      <Col md={4}>
        <p className="text-muted">
          Developed and provided by Vidner Solutions.
        </p>
      </Col>

      <Col md={8}/>
    </Grid>
  </footer>
)

export default Footer
