import React from 'react'
import Sidebar from '../Sidebar'
import Info from './Info'
import News from '../News'
import Postbox from '../Homepage/Postbox'
import "./Profile.css"
//link :https://www.youtube.com/watch?v=ygV99J2Ehjs

function Profile() {
  return (
    
    <div className='profile'>
      <Sidebar/>
      <Info/>
      <News/>
      
      {/* <h6> This is profile page</h6>
      <input value = "First Name" />
      <input value = "Last Name" /> */}
      
    </div>
  )
}

export default Profile
