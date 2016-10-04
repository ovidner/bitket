import React from 'react'

import { Footer, Navbar } from './'

const Layout = (props) => (
  <div>
    <Navbar />
    {props.children}
    <Footer />
  </div>
)

export default Layout
