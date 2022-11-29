import React, { useState, Component, useEffect } from 'react'
import "./styles/FriendRequestsTab.css"
import { appBarClasses, Avatar, Button, TextField} from '@mui/material';
import ActivityTab from './ActivityTab';
import axios from "axios";
import { Navigate } from 'react-router-dom';
import {useNavigate, useParams} from 'react-router-dom'
import { CookieSharp } from '@mui/icons-material';

export default function FriendRequestsTab() {
  const [requests, setRequests] = useState([{}]);
  const [acceptedRequests, setAcceptedRequests] = useState([{}]);
  const [followingBack, setFollowingBack] = useState(false);
  const [accButtonText, setAccButtonText] = useState("Follow Back")
  const navigate = useNavigate();
  const authorid = localStorage.getItem("authorid")
  const token = localStorage.getItem("token")

  //add to friends list, remove from requests
  const accept_clicked = async(id) => {

    let formField = new FormData();
    formField.append("hasAccepted",true)

    await axios.put('https://socioecon.herokuapp.com/follows/'+ id + '/', formField,
    {headers: {"Content-Type":"application/json", "Authorization": "Token " + token}},
    
    ).then((response) => {
      // console.log(response.data)
      const updatedRequests = requests.filter(
        (req) => req.id !== id
      );
      setRequests(updatedRequests);
    })
    // const updatedRequests = requests.filter(
    //   (req) => req.id !== id
    // );
    // setRequests(updatedRequests);
    
  }

  //remove from requests
  const decline_clicked = async(id) => {
    console.log("declined " + id)
    await axios.delete('https://socioecon.herokuapp.com/follows/'+ id + '/', {
      headers: {"Authorization": "Token " + token}
    }).then((response) => {
      console.log(response.data)
    })
    const updatedRequests = requests.filter(
      (req) => req.id !== id
    );
    setRequests(updatedRequests);
  }

  const followBackClicked = async(auth_id) => {
    //if user is not yet following back
    // console.log("un be friend " + auth_id)
    // if(!followingBack) {
    if (accButtonText === "Follow Back") {
      await axios.post('https://socioecon.herokuapp.com/authors/' + auth_id + '/followers/', {
      withCredentials:true}, 
      {headers: {'Content-Type':'application/json', "Authorization": "Token " + token}}
      ).then((response) => {
        console.log(followingBack)
        setFollowingBack(!followingBack);
        setAccButtonText("Un-Befriend")
        console.log(followingBack)
        console.log(response.data)
    })
    //if user is already following back
    } else {
      //auth id = id of user that is losing the follower, the nnext id is of the user that is un be-friending
      await axios.delete('https://socioecon.herokuapp.com/authors/'+ auth_id + '/followers/' + authorid, {
        headers: {"Authorization": "Token " + token}
      }).then((response) => {
        console.log(followingBack)
        setFollowingBack(!followingBack);
        setAccButtonText('Follow Back')
        console.log(followingBack)
        console.log(response.data)
      })
    }
  }

  //show all pending friend requests
  useEffect(() => {
    async function getAllRequests() {
      const arr = [];
      await axios.get('https://socioecon.herokuapp.com/follows/incoming/', {
        headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
      }).then((response) => {
        for (let follow of response.data.items) {
          arr.push(follow)
          // console.log(response.data.items)
          // console.log(follow)
        }
        setRequests(arr)
        // console.log(setRequests)
        // console.log(arr)
      })
    }
    getAllRequests()
  }, []) //check what goes here TOO MANY GET REQUESTS WITH requests, cant leave blank mininmum requests

  useEffect(() => {
    // update button to show "Follow Back" or "Un befriend"
    async function updateAcceptedBtns(follower_id) {
      //logged in user is a follower of follower_id
      await axios.get('https://socioecon.herokuapp.com/authors/' + follower_id + '/followers/' + authorid, {
        //get real friends of authorid
      // await axios.get('https://socioecon.herokuapp.com/authors/' + authorid + '/real-friends/', {
        headers: {"Content-Type":"application/json", "Authorization": "Token " + token}
      }).then((response) => {
          setFollowingBack(!followingBack)
          setAccButtonText("Un-Befriend")
      })
    }

    // show all accepted friend requests
    async function getAcceptedRequests() {
      const accepted = [];
      await axios.get('https://socioecon.herokuapp.com/authors/' + authorid + '/followers/', {
        headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
      }).then((response) => {
        for (var acc_follower of response.data.items) {
          accepted.push(acc_follower);
          // console.log(acc_follower.id)
          // console.log(response.data.items)
          updateAcceptedBtns(acc_follower.id);
        }
        setAcceptedRequests(accepted);
        // updateAcceptedBtns(acc_follower.id);
      })
    }

    getAcceptedRequests();
  }, []) //accepted requests but send too many get

  // useEffect(() => {
  //   async function get
  // })

  return (
      <div className='FriendRequestsTab'>
        
          {requests.map((req) => (
            <div key={req.summary}>
              {/* {console.log(req)} */}
              <p className='request_list'>
                {req.summary}
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
          {acceptedRequests.map((acc) =>(
            <div key={acc.preferredName}>
              {console.log(acc)}
              <p className='accepted_list'>
                {acc.preferredName} is following you
                <span className='accepted_btn'>
                  <Button 
                  className='follow_back_btn' 
                  onClick={() => followBackClicked(acc.id)}
                  style={{backgroundColor: accButtonText === "Un-Befriend" ? "red" : "rgb(159, 185, 31)"}}>
                    {/* {followingBack ? "Un-Befriend" : "Follow Back"} */}
                    {accButtonText}
                  </Button>
                </span>
              </p>
            </div>
          ))}
      </div>
  )
}