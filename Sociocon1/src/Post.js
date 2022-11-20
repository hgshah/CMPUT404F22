// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0
import React from 'react'
import {useState, useEffect} from 'react';
import "./Post.css";
import Comment from './Comment';
import {useNavigate, useParams} from 'react-router-dom'
import { Avatar, Button, TextField} from '@mui/material';
import profilepic from "./profilepic.jpeg";
import CommentIcon from '@mui/icons-material/ModeComment';
import ShareIcon from '@mui/icons-material/Share';
import SendIcon from '@mui/icons-material/Send';
import DeleteIcon from '@mui/icons-material/Delete';
import LikeIcon from '@mui/icons-material/FavoriteBorder';
import EditIcon from '@mui/icons-material/Edit';
import { Link } from 'react-router-dom';
import { Send } from '@mui/icons-material';
import axios from 'axios'

function Post({displayName, title, description, text, image, avatar, visibility}) {
    const[value, setValue] = useState(""); 
    const [comment, setPostComment] = useState('');
    const [ContentType, setPostContentType] = useState('');
    //const[p_post, setPost] = useState([]); 
    function handle() {
        alert(value)
    }
    const AddComment = async () => {
        let formField = new FormData()
        formField.append("comments", comment)
        formField.append("contentType", ContentType)
        await axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts/85c7c95e-dd41-44d2-ae0e-f0cb143fc908/comments',
            data: formField
        }).then((response) =>{
            console.log(response.data)
            navigate.push('/')
        })
    }
    // useEffect(() => {
    //     async function getAllPosts(){
    //         try {
    //                 const p_post = await axios.get("http://localhost:8000/posts/public/")
    //                 console.log(p_post.data)
    //                 setPost(p_post.data)
    //         }
    //         catch(error){
    //             console.log(error)
    //         }
    //     }
    //     getAllPosts()
    // }, [])
    const navigate = useNavigate()
    
    const DeletePostInfo = async (id) => {
        String(id)
        const nid = String(id).slice(-36)
        await axios({
                method:'DELETE',
                url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts/' + nid + '/',
            
        }).then((response) =>{
            console.log(response.data)
            navigate.push('/')
        })
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
                        
                        <EditIcon fontSize='small' /> 
                        
                        
                    </h3>
                    
                </div>
                <div className='visibility'>
                    <h4>
                         {visibility} 
                    </h4>
                </div>
                <div className = "post_headerdis">
                    
                    {/* <p>{text}</p> */}
                    {title} <br></br>
                    {description}

                </div>
                
                 <img className='post_content' src = {image} alt = " "/> 
                 <form>
                    <span>
                        <Button variant='contained' size = "small" endIcon= {<LikeIcon/>} type = "submit" >   </Button>  &nbsp;&nbsp;&nbsp;
                        <Button variant='contained' size = "small" endIcon= {<ShareIcon/>} type = "submit" >   </Button>
                    </span>

                    </form>

                <div className='post_footer'>
                

                {/* /* // link: https://stackoverflow.com/questions/38443227/how-to-get-input-text-value-on-click-in-reac
                // author: https://stackoverflow.com/
                // license:  https://creativecommons.org/licenses/by-sa/4.0/ */}
                        {/* <input type = "text" value={value} onChange={(e) => {setValue(e.target.value)}} placeholder = "Write a comment" /> */}
                        {/* <LikeIcon fontSize = "small" />
                        <ShareIcon fontSize = "small" /> */}
                     <div className='post_comments'>
                        <Comment/>
                        <form>
                            <input 
                                onChange={e => setPostComment(e.target.value)} 
                                value={comment} 
                                placeholder='Enter comment' 
                                type = 'text'
                                className='post_input'
                                variant = 'outlined'
                                label = "add comment"
                                size = "small"
                            />
                            <label for="set-contenttype"></label>
                                {/* // Link: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select 
                                    author: https://developer.mozilla.org/en-US/
                                    License: https://creativecommons.org/licenses/by-sa/4.0/*/}
                                <select name="contenttype" id="contenttype">
                                    <option value="">choose an option--</option>
                                    <option value={comment}>CommonMark</option>
                                    <option value={comment}>PlainText</option>
                                </select>
                            {/* <TextField label = "add comment"  size = "small" variant='outlined' className='post_input' placeholder='add comment' /> */}
                            <Button onClick = {AddComment} variant='contained' size = "small" endIcon= {<SendIcon/>} type = "submit" >   </Button> 
                            
                        </form> 
                        <Button onclick = {DeletePostInfo} variant = 'contained' endIcon = {<DeleteIcon/>} className = "postdel_button"></Button>
                    </div> 
 
                       
                   
                </div>
                {/* <div className='submit'>
                    <button onClick={handle} id="post"> Submit</button> 
                </div> */}
            </div>
        </div>
      
    </div>
  )
}

export default Post
