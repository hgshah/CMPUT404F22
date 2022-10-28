import React, {useState, useEffect} from 'react'
import "./Feed.css"
import Postbox from './Postbox'
import Post from './Post'
import profilepic from "./profilepic.jpeg";
import Inbox from "./Inbox";
import Profile from "./Profile";

function Feed() {
    const [posts, setPosts] = useState([]);
    useEffect(() =>{
            setPosts()
    }, [])
  return (
    <div className='feed'>
        <div className="feed_header">
           <h2>Home </h2>
        </div>
        
      {/* header*/}
      <Postbox />

      {/* Post*/}
      <Post displayName = "Harsh Shah" text = {postMessage} image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar = {profilepic} visibility = "public" />
      <Post displayName = "Harsh Shah" text = {postMessage} image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar = {profilepic} visibility = "public" />
      <Post displayName = "Harsh Shah" text = {postMessage} image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar = {profilepic} visibility = "public" />
      <Post displayName = "Harsh Shah" text = {postMessage} image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar = {profilepic} visibility = "public" />


      {/* header*/}
    </div>
  )
}

export default Feed
