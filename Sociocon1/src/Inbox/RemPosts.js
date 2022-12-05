import React from 'react'
import "./styles/RemPosts.css"
import { useState, useEffect } from 'react'
import axios from 'axios'
import InboxPosts from './InboxPosts'
import { TextField } from '@mui/material'
export default function RemPosts() {
    const [remid, setRemid] = useState('')
    const [rp_inbox, setRPInbox] = useState([])
    const token = localStorage.getItem("token")
    const rempostid = localStorage.getItem("rempostid")

    useEffect(() => {
        async function getAllInbox(){
            try {
                    const p_inbox = await axios.get(
                        "https://socioecon.herokuapp.com/authors/" + rempostid + "/posts ",
                    
                        {headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token}},
                        
                        )
                        const ipost = []
                        for(let i = 0; i<p_inbox.data.items.length; i++){
                            if(p_inbox.data.items[i].visibility ==="PUBLIC"){
                                ipost.push(p_inbox.data.items[i])
                            }
                            
                           
                        }
                    console.log(ipost)
                    setRPInbox(ipost)
            }
            
            catch(error){
                console.log(error)
            }
            
        }
        getAllInbox()
    }, [])
   

  return (
    <div className='RemPosts'>
        
        
        <div className='footer'>
        {
                        rp_inbox.map((iposts) => {
                            return (
                            
                                <p>
                                  
                                  <InboxPosts purl = {iposts.url} title = {iposts.title} description = {iposts.description} displayName = {iposts.author.displayName}  image = {iposts.content}  visibility = {iposts.visibility}/>
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

