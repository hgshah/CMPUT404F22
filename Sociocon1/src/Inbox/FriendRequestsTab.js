import React, { useState, Component, useEffect } from 'react'
import "./FriendRequestsTab.css"
import { appBarClasses, Avatar, Button, TextField} from '@mui/material';
import ActivityTab from './ActivityTab';
import axios from "axios";

export default function FriendRequestsTab() {
  const [requests, setRequests] = useState([
    {url: "bobs_url", id: "bob"},
    {url: "tims_url", id: "tim"},
  ])
  const [idFollower, setIdFollower] = useState([]);

  // useEffect(() => {
  //   handleFollowRequests();
  // }, []);

  // const handleFollowRequests = async() => {
  //   response = await axios.get(process.env.REACT_APP_HOST + 'authors/{uuid}/followers/')
  //   console.log(response)
  //   const idFollower = [];
  //   for (let follower of response.data.items) {
  //     idFollower.push()
  //   }
  // }

  // componentDidMount() {
  //   this.refreshList();
  // }

  // refreshList = () => {
  //   axios
  //     .get("/api/todos/")
  //     .then((res) => this.setState({ todoList: res.data }))
  //     .catch((err) => console.log(err));
  // };

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

  return (
    <div className='FriendRequestsTab'>
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