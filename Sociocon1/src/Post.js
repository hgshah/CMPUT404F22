
import React from 'react'
import "./Post.css";
import { Avatar} from '@mui/material';
import profilepic from "./profilepic.jpeg";
import CommentIcon from '@mui/icons-material/ModeComment';
import ShareIcon from '@mui/icons-material/Share';
import LikeIcon from '@mui/icons-material/FavoriteBorder';
import { Link } from 'react-router-dom';
function Post({displayName, text, image, avatar, visibility}) {
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
                    
                        <CommentIcon fontSize = "small" />
                        <LikeIcon fontSize = "small" />
                        <ShareIcon fontSize = "small" />  
                   
                </div>
            </div>
        </div>
      
    </div>
  )
}

export default Post
