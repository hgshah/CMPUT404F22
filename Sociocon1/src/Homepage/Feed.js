// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0

import React, {useState, useEffect} from 'react'
import "./Feed.css"
import Postbox from './Postbox'
import { Avatar, Button, TextField} from '@mui/material';
import Post from './Post'
// import profilepic from "../MyProfile/Info.js";
import Inbox from "../Inbox/Inbox";
import axios from 'axios'
import Comment from './Comment'
import Test from '../Test';
import Profile from "../MyProfile/Profile";
import Login from '../Login';
import ReactDom from 'react-dom'
import { Card } from 'antd';
import ReactMarkdown from 'react-markdown'
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
    const [profilePic, setProfilePic] = useState("")
    // var user_pp = ""
    // useEffect(() =>{
    //         setPosts()
    // }, [])
    useEffect(() => {
      async function getAllPosts(){
          try {
                  const p_post = await axios.get("https://socioecon.herokuapp.com/posts/public/")
                  // console.log("P_post: ", p_post.data)
                  // console.log(p_post.data.title)
                  setPost(p_post.data)
          }
          
          catch(error){
              console.log(error)
          }
          
      }

      //get the profile pic
      // async function getProfilePic() {
      //   await axios.get('https://socioecon.herokuapp.com/posts/public/', {
      //           headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
      //       }).then((response) => {
      //           //if "" then put default pic
                
      //           // setProfilePic(response.data.profileImage)
      //           // var user_pp = response.data.profileImage
      //           // console.log("PP: ", user_pp)
      //           // console.log("INSIDE: ", profilePic)
      //           console.log("PP: ", response.data[0].author.profileImage)
      //           console.log("ALL: ", response.data)
      //       })
      // }
      // console.log("AFTER: ", profilePic)
      // console.log("PP: ", user_pp)

      getAllPosts()
      // getProfilePic()
  }, [])

  // console.log("PP: ", user_pp)

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
           <h1>Home              
            </h1>
            <h3>
              User: {preferredName} 
            </h3>
          
        </div>
        
      {/* header*/}
      <Postbox authorid = {authorid} />
      <h3> Public Posts</h3>
      
      {
                        p_post.map((posts) => {
                            return (
                                
                                <h2 >
                                  
                                   <Post  post_authorid = {posts.author.id} purl = {posts.url} title = {posts.title} description = {posts.description} displayName = {posts.author.preferredName}  image = {posts.content} avatar = {posts.author.profileImage} visibility = {posts.visibility}/>
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
