// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0

import React, {useState, useEffect} from 'react'
import "./Feed.css"
import Postbox from './Postbox'
import { Avatar, Button, TextField} from '@mui/material';
import Post from './Post'
import profilepic from "./profilepic.jpeg";
import Inbox from "./Inbox";
import axios from 'axios'
import Test from './Test';
import Profile from "./Profile";
import {useNavigate, useParams} from 'react-router-dom'
function Feed() {
    //const [posts, setPosts] = useState([]);
    const[p_post, setPost] = useState([]); 
    // useEffect(() =>{
    //         setPosts()
    // }, [])
    useEffect(() => {
      async function getAllPosts(){
          try {
                  const p_post = await axios.get("http://localhost:8000/posts/public/")
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
    
    const DeletePostInfo = async (id) => {
        String(id)
        const nid = String(id).slice(-36)
        await axios({
                method:'DELETE',
                url: 'http://localhost:8000/authors/1384c9c1-1e2d-4b7f-868b-4f3c499fe3cd/posts/' + nid + '/',
            
        }).then((response) =>{
            console.log(response.data)
            navigate.push('/')
        })
    }
  //const navigate = useNavigate()
  return (
    <div className='feed'>
        <div className="feed_header">
           <h2>Home </h2>
        </div>
        
      {/* header*/}
      <Postbox />
      {
                        p_post.map((posts) => {
                            return (
                                <h2 >
                                   <Post title = {posts.title} description = {posts.description} displayName = "Harsh Shah"  image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar = {profilepic} visibility = "public"/>
                                    {/* {posts.title} <br></br>
                                    {posts.description} */}
                                    <Button onClick = {() =>DeletePostInfo(posts.id)}  className = "postdel_button">Delete</Button>
                                </h2>
                            )
                        })
                    }
      {/* Post*/}
      {/* <Test/> */}
      {/* <Post displayName = "Harsh Shah"  image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar = {profilepic} visibility = "public" /> */}
      {/* <Post displayName = "Elon Musk" text = {postMessage} image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar ="https://nypost.com/wp-content/uploads/sites/2/2022/05/elon-musk-1.jpg?quality=75&strip=all" visibility = "public" />
      <Post displayName = "Virat_kohli" text = {postMessage} image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar = "https://upload.wikimedia.org/wikipedia/commons/7/7e/Virat_Kohli.jpg" visibility = "public" />
      <Post displayName = "Mr@Bean" text = {postMessage} image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar = "https://m.media-amazon.com/images/M/MV5BMTg3NDUzOTc3MV5BMl5BanBnXkFtZTcwNjcxMDkxNw@@._V1_.jpg" visibility = "public" /> */}


      {/* header*/}
    </div>
  )
}

export default Feed
