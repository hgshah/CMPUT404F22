// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0

import React, {useState, useEffect} from 'react'
import "./Feed.css"
import Postbox from './Postbox'
import { Avatar, Button, TextField} from '@mui/material';
import Post from './Post'
import profilepic from "../MyProfile/profilepic.jpeg";
import Inbox from "../Inbox/Inbox";
import axios from 'axios'
import Comment from './Comment'
import Test from '../Test';
import Profile from "../MyProfile/Profile";
import Login from '../Login';
import Home from './Home'
import {useNavigate, useParams} from 'react-router-dom'
function Feed({}) {
    //const [posts, setPosts] = useState([]);
    const[p_post, setPost] = useState([]); 
    const[p_comment, setComment] = useState([]); 
    const authorid = localStorage.getItem("authorid")
    const token = localStorage.getItem("token")
    const preferredName = localStorage.getItem("preferredName")
    const ibase64 = localStorage.getItem("image")
    // useEffect(() =>{
    //         setPosts()
    // }, [])
    useEffect(() => {
      async function getAllPosts(){
          try {
                  const p_post = await axios.get("https://socioecon.herokuapp.com/posts/public/")
                  console.log(p_post.data)
                  setPost(p_post.data)
          }
          
          catch(error){
              console.log(error)
          }
          
      }
      getAllPosts()
  }, [])



  const navigate = useNavigate()
    // link: https://www.youtube.com/watch?v=aRYkCe6JcGM
    // author: https://www.youtube.com/c/GreatAdib
    // license: https://creativecommons.org/
    // const DeletePostInfo = async (id) => {
    //     String(id)
    //     const nid = String(id).slice(-36)
    //     await axios({
    //             method:'DELETE',
    //             url: 'http://localhost:8000/authors/1384c9c1-1e2d-4b7f-868b-4f3c499fe3cd/posts/' + nid + '/',
            
    //     }).then((response) =>{
    //         console.log(response.data)
    //         navigate.push('/')
    //     })
    // }
  //const navigate = useNavigate()
  return (
    <div className='feed'>
        <div className="feed_header">
           <h2>Home              
            </h2>
            <h3>
              user:{preferredName} 
            </h3>
          
        </div>
        
      {/* header*/}
      <Postbox authorid = {authorid} />
      
      {
                        p_post.map((posts) => {
                            return (
                              
                                <h2 >
                                  
                                   <Post post_authorid = {posts.author.id} purl = {posts.url} title = {posts.title} description = {posts.description} displayName = {posts.author.preferredName}  image = {posts.content} avatar = {profilepic} visibility = {posts.visibility}/>
                                    {/* {posts.title} <br></br>
                                    {posts.description} */}
                                    
                                    {/* <Buttson onClick = {() =>DeletePostInfo(posts.id)}  className = "postdel_button">Delete</Button> */}
                                </h2>
                            )
                        })
                    }

      

      {/* Post*/}
      
 


      {/* header*/}
    </div>
  )
}

export default Feed
