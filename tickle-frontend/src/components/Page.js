import React from 'react'
import { Grid } from 'react-bootstrap'

const Page = (props) => (
  <div>
    <Grid>
      {props.children}
    </Grid>
  </div>
)

export default Page
