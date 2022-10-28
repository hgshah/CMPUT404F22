// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0
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
    // link: https://stackoverflow.com/questions/38443227/how-to-get-input-text-value-on-click-in-reac
    // author: https://stackoverflow.com/
    // license:  https://creativecommons.org/licenses/by-sa/4.0/
    const[value, setValue] = useState("");
    function handle() {
        alert("post has been created")
    }
    const sendPost = (e) => {
        e.preventDefault();
        };
  return (
    <div className='postbox'>
        <form> 
            
            <div className="postbox_input">
                <Avatar sr  c = {profilepic} />
                
                <input onChange={e => setValue(e.target.value)} value={value} placeholder='Enter post title' type = "text"/>
                <input onChange={e => setPostMessage(e.target.value)} value={postMessage} placeholder='Enter post body' type = "text"/>
                <label for="set-visibility"></label>
                {/* // Link: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select
                       author: https://developer.mozilla.org/en-US/
                       License: https://creativecommons.org/licenses/by-sa/4.0/*/}
                <select name="visibility" id="visibility">
                    <option value="">choose an option--</option>
                    <option value="Public">Public</option>
                    <option value="Friends">Friends</option>
                </select>
                
            </div>
            <input value={postImage} onchange = {e => setPostImage(e.target.value)} className="postbox_inputimage" placeholder='Enter a image url' type = "text" /> <br></br>
            {/* // link: https://stackoverflow.com/questions/38443227/how-to-get-input-text-value-on-click-in-reac
                // author: https://stackoverflow.com/
                // license:  https://creativecommons.org/licenses/by-sa/4.0/ */}
            <Button onClick = {handle} type = "submit" className = "postbox_button">Post</Button>
            
        </form>
      
    </div>
   
  )
  
}

export default Postbox
