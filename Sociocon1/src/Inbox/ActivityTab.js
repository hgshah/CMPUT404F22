import React from 'react'
import "./styles/ActivityTab.css"
import FriendRequestsTab from './FriendRequestsTab'
import Comment from '../Homepage/Comment'

export default function ActivityTab() {
    let fetchURL = "http://127.0.0.1:8000/authors"

    fetch(fetchURL)
      .then((response) => console.log(response))
      .then((data) => console.log(data))

    return (
        <div className='ActivityTab'>
        {/* <p>Your inbox is empty. </p> */}
        
        </div>
    )
}