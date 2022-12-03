import React from 'react'
import Sidebar from './Sidebar'
import News from './News'
import Postbox from './Homepage/Postbox'
//link :https://www.youtube.com/watch?v=ygV99J2Ehjs

function Profile() {
  return (
    
    <div>
      <Sidebar/>
      <div className='profile'>
        <div className='profileHeader'>
          <h1>Profile</h1>
        </div>

      </div>
      
      {/* <h6> This is profile page</h6>
      <input value = "First Name" />
      <input value = "Last Name" /> */}
      
    </div>
  )
}

export default Profile
