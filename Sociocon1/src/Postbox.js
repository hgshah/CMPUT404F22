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
                
                <input onChange={e => setPostMessage(e.target.value)} value={postMessage} placeholder='Enter post title' type = "text"/>
                <input onChange={e => setPostMessage(e.target.value)} value={postMessage} placeholder='Enter post body' type = "text"/>
                <label for="set-visibility"></label>

                <select name="visibility" id="visibility">
                    <option value="">choose an option--</option>
                    <option value="Public">Public</option>
                    <option value="Friends">Friends</option>
                </select>
                
            </div>
            <input value={postImage} onchange = {e => setPostImage(e.target.value)} className="postbox_inputimage" placeholder='Enter a image url' type = "text" /> <br></br>
            
            <Button onClick = {handleClick} type = "submit" className = "postbox_button">Post</Button>
            
        </form>
      
    </div>
   
  )
  
}

export default Postbox
