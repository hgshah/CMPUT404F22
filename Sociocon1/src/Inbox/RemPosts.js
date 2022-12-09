import React from 'react'
import "./styles/RemPosts.css"
import { useState, useEffect } from 'react'
import axios from 'axios'
import InboxPosts from './InboxPosts'
import { TextField } from '@mui/material'
export default function RemPosts() {
    const [remid, setRemid] = useState('')
    const [rp_inbox, setRPInbox] = useState([])
    const [p_host, setPhost] = useState([])
    const token = localStorage.getItem("token")
    const rempostid = localStorage.getItem("rempostid")

    useEffect(() => {
        async function getHost(){
            try {
                    const p_host = await axios.get(
                        "https://socioecon.herokuapp.com/authors/" + rempostid ,
                    
                        {headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token}},
                        
                        )
                        const iposthost = []
                        
                        
                            
                           
                        
                    
                    localStorage.setItem("hosturl", p_host.data.host)
                    setPhost(p_host.data.host)
            }
            
            catch(error){
                console.log(error)
            }
            
        }
        getHost()
    }, [])
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
                                  
                                  <InboxPosts purl = {iposts.url} commenturl = { "https://socioecon.herokuapp.com/authors/" + rempostid + "/posts/" + iposts.id} title = {iposts.title} description = {iposts.description} displayName = {iposts.author.displayName}  image = {iposts.content} avatar = {iposts.author.profileImage} visibility = {iposts.visibility}/>
                                    
                                    
                                    {/* <Buttson onClick = {() =>DeletePostInfo(posts.id)}  className = "postdel_button">Delete</Button> */}
                                </p>
                            )
                        })
                    }
       
        </div>
        
       
    </div>
  )
}

