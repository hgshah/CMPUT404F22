// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0
import React from 'react'
import {useState} from 'react';
import "./Post.css";
import { Avatar} from '@mui/material';
import profilepic from "./profilepic.jpeg";
import CommentIcon from '@mui/icons-material/ModeComment';
import ShareIcon from '@mui/icons-material/Share';
import SendIcon from '@mui/icons-material/Send';
import LikeIcon from '@mui/icons-material/FavoriteBorder';
import { Link } from 'react-router-dom';
function Post({displayName, text, image, avatar, visibility}) {
    const[value, setValue] = useState(""); 
    function handle() {
        alert(value)
    }

  return (
    <div className='post'>
        <div className = "post_avatar">
            <Avatar src = {avatar}/>
        </div>
        <div className='post_body'>
            <div className='post_header'>
                <div className='header_text'>
                    <h3>
                        {displayName} {" "} <span></span>
                    </h3>
                    
                </div>
                <div className='visibility'>
                    <h4>
                         {visibility} 
                    </h4>
                </div>
                <div className = "post_headerdis">
                    <p>{text}</p>
    
                </div>
                 <img className='post_content' src = {image} alt = " "/> 
                <div className='post_footer'>
                {/* /* // link: https://stackoverflow.com/questions/38443227/how-to-get-input-text-value-on-click-in-reac
                // author: https://stackoverflow.com/
                // license:  https://creativecommons.org/licenses/by-sa/4.0/ */}
                        <input type = "text" value={value} onChange={(e) => {setValue(e.target.value)}} placeholder = "Write a comment" />
                        <LikeIcon fontSize = "small" />
                        <ShareIcon fontSize = "small" />
                       
                   
                </div>
                <div className='submit'>
                    <button onClick={handle} id="post"> Submit</button> 
                </div>
            </div>
        </div>
      
    </div>
  )
}

export default Post
