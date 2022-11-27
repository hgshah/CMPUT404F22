// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0
import { Button } from '@mui/material'
import React, {useEffect, useState} from 'react'
import axios from 'axios'
import "./Postbox.css"
import { Avatar} from '@mui/material';
import {useNavigate} from 'react-router-dom'
import profilepic from "../profilepic.jpeg"


function Postbox ({}) {
    const [title, setPostTitle] = useState('');
    const [description, setPostBody] = useState('');
    const [visibility, setPostVisibility] = useState('');
    const [postImage, setPostImage] = useState('');
    const [image, setImage] = useState('');
    const navigate = useNavigate()
    const authorid = localStorage.getItem("authorid")
    // const handleClick = () => {
    //     //  "message" stores input field value
    //     setPostMessage(postMessage);

    // };

    // link: https://stackoverflow.com/questions/38443227/how-to-get-input-text-value-on-click-in-reac
    // author: https://stackoverflow.com/
    // license:  https://creativecommons.org/licenses/by-sa/4.0/
    const[value, setValue] = useState(""); 
  
    // link: https://www.youtube.com/watch?v=xtQ74HKTOwY
    // author: https://www.youtube.com/c/GreatAdib
    //license: https://creativecommons.org/
    const AddPostInfo = async () => {

        if(visibility === "Friends"){
            console.log({visibility})
            let formField = new FormData()
            formField.append("title", title)
            formField.append("description", description)
            formField.append("visibility", visibility)
            await axios({
                method: 'post',

                // url: 'http://localhost:8000/authors/1384c9c1-1e2d-4b7f-868b-4f3c499fe3cd/posts/',
                // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                
                // url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts/',
                url: 'http://127.0.0.1:8000/authors/' + authorid + '/posts/',

                data: formField
            }).then((res) =>{
                console.log(res.data)
                
            })
            
        } else {
                let formField = new FormData()
            formField.append("title", title)
            formField.append("description", description)
            formField.append("visibility", visibility)
            await axios({
                method: 'post',

                // url: 'http://localhost:8000/authors/1384c9c1-1e2d-4b7f-868b-4f3c499fe3cd/posts/',
                // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                
                // url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts/',
                url: 'http://127.0.0.1:8000/authors/' + authorid + '/posts/',

                data: formField
            }).then((res) =>{
                console.log(res.data)
                
        })

        }
        
    }


    
  return (
    <div className='postbox'>
        <form> 
            
            <div className="postbox_input">
                <Avatar sr  c = {profilepic} />
                
    
                <input 
                onChange={e => setPostTitle(e.target.value)} 
                value={title} 
                placeholder='Enter post title' 
                type = "text"
                name = "title"
                />
                <input 
                onChange={e => setPostBody(e.target.value)}
                value={description} 
                placeholder='Enter post body' 
                type = "text"
                name = "description"
                />
                <label for="set-visibility"></label>
                {/* // Link: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select 
                       author: https://developer.mozilla.org/en-US/
                       License: https://creativecommons.org/licenses/by-sa/4.0/*/}
                <select value={visibility} onChange={e => setPostVisibility(e.target.value)} name="visibility" id="visibility">
                    <option  value="" >choose an option--</option>
                    <option  value="public">Public</option>
                    <option value = "friends">Friends</option>
                </select>
                
            </div>
            <input value={postImage} onchange = {e => setPostImage(e.target.value)} className="postbox_inputimage" placeholder='Enter a image url' type = "text" /> <br></br>
            {/* // link: https://www.youtube.com/watch?v=xtQ74HKTOwY */}
            <input 
                onChange={e => setImage(e.target.files)}
                src={image} 
                type = "file"
                name = "post image"
                />
            {/* // link: https://stackoverflow.com/questions/38443227/how-to-get-input-text-value-on-click-in-reac
                // author: https://stackoverflow.com/
                // license:  https://creativecommons.org/licenses/by-sa/4.0/ */}
            <Button onClick = {AddPostInfo}  className = "postbox_button" >Post</Button>
            
        </form>
      
    </div>
   
  )
  
}

export default Postbox
