import React, { useState, Component, useEffect } from 'react'
import "./styles/FriendRequestsTab.css"
import { appBarClasses, Avatar, Button, TextField} from '@mui/material';
import ActivityTab from './ActivityTab';
import axios from "axios";
import { Navigate } from 'react-router-dom';
import {useNavigate, useParams} from 'react-router-dom'

export default function FriendRequestsTab() {
  // const [requests, setRequests] = useState([
  //   {url: "bobs_url", id: "bob"},
  //   {url: "tims_url", id: "tim"},
  // ])
  const [requests, setRequests] = useState([{}])
  const [idFollower, setIdFollower] = useState([]);
  const navigate = useNavigate()

  //add to friends list, remove from requests
  const accept_clicked = (id) => {
    
    const updatedRequests = requests.filter(
      (req) => req.id !== id
    );
    setRequests(updatedRequests);
    
  }

  //remove from requests
  const decline_clicked = (id) => {
    const updatedRequests = requests.filter(
      (req) => req.id !== id
    );
    setRequests(updatedRequests);
  }

  useEffect(() => {
    // const [followReqs, setFollowReqs] = useState([{}])
    const arr = [];
    axios.get('http://127.0.0.1:8000/follows/incoming/', {
      headers: {"Content-Type":"application/json", 'Authorization':'Token ab1a951ce6f7d34dbfd8b7698276372c0ea29db1'},
    }).then((data) => {
      for (let follow of data.data.items) {
        // setRequests(follow)
        arr.push(follow)
        console.log(follow)
      }
      setRequests(arr)
      console.log(data)
    })
    // console.log("hello")
  }, [])

  return (
    <div className='FriendRequestsTab'>
      {/* {friendRequestList()} */}
        {requests.map((req) => (
          <div key={req.id}>
            <p className='request_list'>
              {req.id} has sent you a friend request
              <span className='request_btns'>
                <Button className='accept_btn' onClick={() => accept_clicked(req.id)}>
                  Accept
              </Button>
                <Button className='decline_btn' onClick={() => decline_clicked(req.id)}>
                  Decline
                </Button>
              </span>
            </p>
          </div>
        ))
        }
    </div>
  )
}