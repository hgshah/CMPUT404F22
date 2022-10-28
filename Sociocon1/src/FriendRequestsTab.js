import React from 'react'
import "./FriendRequestsTab.css"

export default function FriendRequestsTab() {
  return (
    <div className='FriendRequestsTab'>
        <p>Bob has sent you a friend request</p>
        <div style={{display: "flex"}}>
          <button style={{marginLeft: "auto"}}>Accept</button>
          <button>Decline</button>
        </div>
    </div>
  )
}
