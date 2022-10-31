// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0

import React, {useState, useEffect} from 'react'
import "./Feed.css"
import Postbox from './Postbox'
import Post from './Post'
import profilepic from "./profilepic.jpeg";
import Inbox from "./Inbox";
import Test from './Test';
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
      {/* <Test/> */}
      <Post displayName = "Harsh Shah" title = {posts} description={posts} image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar = {profilepic} visibility = "public" />
      {/* <Post displayName = "Elon Musk" text = {postMessage} image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar ="https://nypost.com/wp-content/uploads/sites/2/2022/05/elon-musk-1.jpg?quality=75&strip=all" visibility = "public" />
      <Post displayName = "Virat_kohli" text = {postMessage} image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar = "https://upload.wikimedia.org/wikipedia/commons/7/7e/Virat_Kohli.jpg" visibility = "public" />
      <Post displayName = "Mr@Bean" text = {postMessage} image = "https://media4.giphy.com/media/vfsAZnqDvoHzUpMPY4/giphy.gif?cid=ecf05e478e7oied3gzz2a9dc79boelr3sh93cvcn5ghfntm0&rid=giphy.gif&ct=g" avatar = "https://m.media-amazon.com/images/M/MV5BMTg3NDUzOTc3MV5BMl5BanBnXkFtZTcwNjcxMDkxNw@@._V1_.jpg" visibility = "public" /> */}


      {/* header*/}
    </div>
  )
}

export default Feed
