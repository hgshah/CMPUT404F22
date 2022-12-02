import React from 'react'
import "./styles/ActivityTab.css"
import FriendRequestsTab from './FriendRequestsTab'
import Comment from '../Homepage/Comment'
import { useState, useEffect } from 'react'
import axios from 'axios'
import Post from '../Homepage/Post'
import { Avatar, Button, TextField } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';

export default function ActivityTab() {
    const authorid = localStorage.getItem("authorid")
    const token = localStorage.getItem("token")
    const[p_inbox, setInbox] = useState([]); 
    useEffect(() => {
        async function getAllInbox(){
            try {
                    const p_inbox = await axios.get(
                        "https://socioecon.herokuapp.com/authors/" + authorid + "/inbox ",
                    
                        {headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token}},
                        
                        )
                        const ipost = []
                        for(let i = 0; i<p_inbox.data.items.length; i++){
                            
                           ipost.push(p_inbox.data.items[i])
                        }
                    console.log(ipost)
                    setInbox(ipost)
            }
            
            catch(error){
                console.log(error)
            }
            
        }
        getAllInbox()
    }, [])
    return (
        <div className='ActivityTab'>
            <div>
            {
                        p_inbox.map((iposts) => {
                            return (
                              
                                <p>
                                  
                                  <Post  title = {iposts.title} description = {iposts.description} displayName = {iposts.author.displayName}  image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g"  visibility = {iposts.visibility}/>
                                    {/* {posts.title} <br></br>
                                    {posts.description} */}
                                    
                                    {/* <Buttson onClick = {() =>DeletePostInfo(posts.id)}  className = "postdel_button">Delete</Button> */}
                                </p>
                            )
                        })
                    }
            </div>
        </div>
    )
}
