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
    </div>
  )
}

export default Profile
