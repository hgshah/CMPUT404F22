import React from 'react'
import Sidebar from './Sidebar'
import News from './News'
//link :https://www.youtube.com/watch?v=ygV99J2Ehjs

function Profile() {
  return (
    
    <div className='profile'>
      <Sidebar/>
      <h6> This is profile page</h6>
      <input value = "First Name" />
      <input value = "Last Name" />
      
    </div>
  )
}

export default Profile
