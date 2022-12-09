import React, { useState, Component, useEffect } from 'react'
import "./styles/FriendRequestsTab.css"
import { appBarClasses, Avatar, Button, TextField} from '@mui/material';
import ActivityTab from './ActivityTab';
import axios from "axios";
import { Navigate } from 'react-router-dom';
import {useNavigate, useParams} from 'react-router-dom'
import { CookieSharp } from '@mui/icons-material';
import Info from '../MyProfile/Info';

export default function FriendRequestsTab() {
  const [requests, setRequests] = useState([{}]);
  const [acceptedRequests, setAcceptedRequests] = useState([{}]);
  // const [followingBack, setFollowingBack] = useState(false);
  // const [accButtonText, setAccButtonText] = useState("Follow Back")
  const [realFriends, setRealFriends] = useState([{}])
  const navigate = useNavigate();
  const authorid = localStorage.getItem("authorid")
  const token = localStorage.getItem("token")
  const [notFolBack, setNotFolBack] = useState([{}]);
  // const noFollowBack = acceptedRequests
  // console.log("accepted req up: ", acceptedRequests)
  // console.log("real f up: ", realFriends)

  // console.log("before no follow back: ", acceptedRequests)
  // console.log("ACCEPTED: ", acceptedRequests)
  // console.log("RF: ", realFriends)
  // for (var notFBack of acceptedRequests) {
  //   for (var realF of realFriends) {
  //     if (notFBack.id === realF.id) {
  //       console.log("In loop: ", notFBack)
  //       console.log("SPLICE REMOVES: " ,acceptedRequests.splice(notFBack, 1))
  //     }
  //   }
    // console.log("in no follow back: ", acceptedRequests)
  // }
  // console.log("not following back: ", acceptedRequests)

  // const getNotFollowingBack = () => {
  //   const result = [...acceptedRequests]
  //   console.log("RESULT: ", result)
  //   console.log("RF: ", realFriends)
  //   for (var notFBack of result) {
  //     for (var realF of realFriends) {
  //       if (notFBack.id === realF.id) {
  //         console.log("In loop: ", notFBack)
  //         console.log("SPLICE REMOVES: " ,result.splice(notFBack, 1))
  //       }
  //     }
  //     // console.log("in no follow back: ", acceptedRequests)
  //   }
  //   console.log("FINAL RESULT: ", result)
  //   return result
  // }

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
    // console.log("declined " + id)
    await axios.delete('https://socioecon.herokuapp.com/follows/'+ id + '/', {
      headers: {"Authorization": "Token " + token}
    }).then((response) => {
      // console.log(response.data)
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
    // if (accButtonText === "Follow Back") {
      await axios.post('https://socioecon.herokuapp.com/authors/' + auth_id + '/followers/', 
      {withCredentials:true}, 
      {headers: {'Content-Type':'application/json', "Authorization": "Token " + token}}
      ).then((response) => {
        // console.log(followingBack)
        // setFollowingBack(!followingBack);
        // setAccButtonText("Un-Befriend")
        // console.log(followingBack)
        // console.log(response.data)
    })
  }

  const unbefriendClicked = async(rf_id) => {
    await axios.delete('https://socioecon.herokuapp.com/authors/'+ rf_id + '/followers/' + authorid, 
    {headers: {"Authorization": "Token " + token}
      }).then((response) => {
        // console.log(followingBack)
        // setFollowingBack(!followingBack);
        // setAccButtonText('Follow Back')
        // console.log(followingBack)
        console.log(response.data)
      }).catch((error) => {
        console("ERROR followBackClicked else: ", error.data)
      })
  }

  //show all pending friend requests
  useEffect(() => {
    async function getAllRequests() {
      const arr = [];
      return await axios.get('https://socioecon.herokuapp.com/follows/incoming/', {
        headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
      })
      // .then((response) => {
      //   for (let follow of response.data.items) {
      //     arr.push(follow)
      //     // console.log(response.data.items)
      //     // console.log("FOLLOW: ", follow)
      //   }
      //   setRequests(arr)
      //   // console.log(setRequests)
      //   // console.log(arr)
      // })
    }
  // }, []) //check what goes here TOO MANY GET REQUESTS WITH requests, cant leave blank mininmum requests

  // useEffect(() => {
    // update button to show "Follow Back" or "Un befriend"
     //get real friends of authorid
      // await axios.get('https://socioecon.herokuapp.com/authors/' + authorid + '/real-friends/', {
    // console.log("HERE")
    async function updateAcceptedBtns(follower_id) {
      //logged in user is a follower of follower_id
      await axios.get('https://socioecon.herokuapp.com/authors/' + follower_id + '/followers/' + authorid, {
        headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
      }).then((response) => {
        // console.log("HERE2")
        // setFollowingBack(!followingBack)
        // setAccButtonText("Un-Befriend")
        // console.log("show button text1: ", followingBack)
        // console.log("acc btn text: ", accButtonText)
      }).catch((error) => {
        // console.log("updateAcceptedBtns error: ", error.response)
        // console.log("following back: should be false", followingBack)
        // console.log("show button text: ", accButtonText)
      })
    }

    // show all accepted friend requests
    async function getAcceptedRequests() {
      const accepted = [];
      return await axios.get('https://socioecon.herokuapp.com/authors/' + authorid + '/followers/', {
        headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
      })
      
      // .then((response) => {
      //   for (var acc_follower of response.data.items) {
      //     accepted.push(acc_follower);
      //     // console.log(acc_follower.id)
      //     // console.log(response.data.items)
      //     // updateAcceptedBtns(acc_follower.id);

      //     // setFollowingBack(!followingBack)
      //     // setAccButtonText("Follow Back")
      //   }
      //   setAcceptedRequests(accepted);
      //   // updateAcceptedBtns(acc_follower.id);
      // }).catch((error) => {
      //   console("ERROR showing all accepted requests: ", error.data)
      // })
    }

    async function getRealFriends() {
      const rf_arr = []
      return await axios.get('https://socioecon.herokuapp.com/authors/' + authorid + '/real-friends/', {
        headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
      })
      // .then((response) => {
      //   for (var rf of response.data.items) {
      //     rf_arr.push(rf)
      //     // console.log("RF: ", rf.id)
      //     // setFollowingBack(!followingBack)
      //     // setAccButtonText("Un-Befriend")
      //   }
      //   setRealFriends(rf_arr)
      // })
    }

    const getNotFollowingBack = (ar, rf) => {
      const result = [...ar]
      // console.log("RESULT: ", result)
      // console.log("RF: ", rf)
      for (var notFBack in result) {
        for (var realF in rf) {
          if (result[notFBack].id === rf[realF].id) {
            // console.log("In loop: ", notFBack.id)
            console.log("SPLICE REMOVES: " ,result.splice(notFBack, 1))
          }
        }
        // console.log("in no follow back: ", acceptedRequests)
      }
      // console.log("FINAL RESULT: ", result)
      return result
    }

    Promise.all([getAllRequests(), getAcceptedRequests(), getRealFriends()]).then((values) => {
      console.log("VALUES: ", values)
      setRequests(values[0].data.items)
      setAcceptedRequests(values[1].data.items)
      setRealFriends(values[2].data.items)
      setNotFolBack(getNotFollowingBack(values[1].data.items, values[2].data.items))
    })

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
          {notFolBack.map((acc) =>(
            <div key={acc.preferredName}>
              {/* {console.log(acc)} */}
              <p className='accepted_list'>
                {acc.preferredName} is following you
                <span className='accepted_btn'>
                  <Button 
                  className='follow_back_btn' 
                  onClick={() => followBackClicked(acc.id)}
                  // style={{backgroundColor: accButtonText === "Un-Befriend" ? "red" : "rgb(159, 185, 31)"}}>
                  style={{backgroundColor: "rgb(159, 185, 31)"}}>
                    {/* {followingBack ? "Un-Befriend" : "Follow Back"} */}
                    {/* {accButtonText} */}
                    Follow Back
                  </Button>
                </span>
              </p>
            </div>
          ))}

          {realFriends.map((real) => (
            <div key={real.preferredName}>
              <p className='rf_list'>
                {real.preferredName} is your real friend
                <span className='rf_btn'>
                  <Button
                  className='unbefriend_btn'
                  onClick={() => unbefriendClicked(real.id)}
                  style={{backgroundColor: "red"}}>
                    Un-Befriend
                  </Button>
                </span>
              </p>
            </div>
          ))}
      </div>
  )
}