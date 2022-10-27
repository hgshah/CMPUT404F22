import { Button } from '@mui/material'
import React, {useState} from 'react'
import "./Postbox.css"
import { Avatar} from '@mui/material';
import profilepic from "./profilepic.jpeg"
function Postbox() {
    const [postMessage, setPostMessage] = useState('');
    const [postImage, setPostImage] = useState('');
    const handleClick = () => {
        //  "message" stores input field value
        setPostMessage(postMessage);
    };
    const sendPost = (e) => {
        e.preventDefault();
        };
  return (
    <div className='postbox'>
        <form> 
            
            <div className="postbox_input">
                <Avatar src = {profilepic} />
                
                <input onChange={e => setPostMessage(e.target.value)} value={postMessage} placeholder='Enter a new public post' type = "text"/>
                
            </div>
            <input value={postImage} onchange = {e => setPostImage(e.target.value)} className="postbox_inputimage" placeholder='Enter a image url' type = "text" /> <br></br>

            <Button onClick = {handleClick} type = "submit" className = "postbox_button">Post</Button>
            
        </form>
      
    </div>
   
  )
  
}

export default Postbox
