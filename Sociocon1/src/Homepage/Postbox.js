// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0
import { Button, TextField } from '@mui/material'
import React, {useEffect, useState} from 'react'
import axios from 'axios'
import "./Postbox.css"
import { Avatar} from '@mui/material';
import {useNavigate} from 'react-router-dom'
import profilepic from "../MyProfile/profilepic.jpeg"
import { upload } from '@testing-library/user-event/dist/upload';


function Postbox ({}) {
    const [title, setPostTitle] = useState('');
    const [description, setPostBody] = useState('');
    const [visibility, setPostVisibility] = useState('');
    // const [postImage, setPostImage] = useState('');
    const [pimage, setPimage] = useState('');
    const [commonMark, setCommonMark] = useState('');
    const [base, setBase] = useState('');
    const navigate = useNavigate()
    const authorid = localStorage.getItem("authorid")
    const ibase64 = localStorage.getItem("image")
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
// link: https://stackoverflow.com/questions/29108779/how-to-get-selected-value-of-a-dropdown-menu-in-reactjs
// author:
// license:
        if(visibility === "Friends"){
            if (commonMark === "text/markdown" || commonMark === "text/plain"){
                localStorage.removeItem("image")
                let formField = new FormData()
                formField.append("title", title)
                formField.append("visibility", visibility)
                formField.append("contentType", commonMark)
                formField.append("content", description)
                await axios({
                    method: 'post',
                    
                    // url: 'http://localhost:8000/authors/1384c9c1-1e2d-4b7f-868b-4f3c499fe3cd/posts/',
                    // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                    // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                    
                    // url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts/',
                    url: 'https://socioecon.herokuapp.com/authors/' + authorid + '/posts/',
    
                    data: formField
                }).then((res) =>{
                    console.log(res.data)
                    
            })
            }
            else {
                    
                    let formField = new FormData()
                    formField.append("title", title)
                    formField.append("description", description)
                    formField.append("visibility", visibility)
                    formField.append("contentType", commonMark)
                    formField.append("content", ibase64)
                    await axios({
                        method: 'post',
                        
                        // url: 'http://localhost:8000/authors/1384c9c1-1e2d-4b7f-868b-4f3c499fe3cd/posts/',
                        // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                        // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                        
                        // url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts/',
                        url: 'https://socioecon.herokuapp.com/authors/' + authorid + '/posts/',

                        data: formField
                    }).then((res) =>{
                        console.log(res.data)
                        
                })
            }

            
        } 
        
        else {

            if (commonMark === "text/markdown" || commonMark==="text/plain"){
                localStorage.removeItem("image")
                let formField = new FormData()
                formField.append("title", title)
                formField.append("visibility", visibility)
                formField.append("contentType", commonMark)
                formField.append("content", description)
                await axios({
                    method: 'post',
                    
                    // url: 'http://localhost:8000/authors/1384c9c1-1e2d-4b7f-868b-4f3c499fe3cd/posts/',
                    // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                    // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                    
                    // url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts/',
                    url: 'https://socioecon.herokuapp.com/authors/' + authorid + '/posts/',
    
                    data: formField
                }).then((res) =>{
                    console.log(res.data)
                    
            })
            }
            else {
                    
                    let formField = new FormData()
                    formField.append("title", title)
                    formField.append("description", description)
                    formField.append("visibility", visibility)
                    formField.append("contentType", commonMark)
                    formField.append("content", ibase64)
                    await axios({
                        method: 'post',
                        
                        // url: 'http://localhost:8000/authors/1384c9c1-1e2d-4b7f-868b-4f3c499fe3cd/posts/',
                        // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                        // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
                        
                        // url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts/',
                        url: 'https://socioecon.herokuapp.com/authors/' + authorid + '/posts/',

                        data: formField
                    }).then((res) =>{
                        console.log(res.data)
                        
                })
            }

                

        }
        
    }
    let pb64
    //link:https://www.youtube.com/watch?v=qmr9NCYjueM
    // author: https://www.youtube.com/@Nhonohyolmo
    // license: https://creativecommons.org/
    const uploadImage =async (e) => {
         //console.log(e.target.files)
         const pimage = e.target.files[0]
         const base64 =await toB64(pimage)
         pb64 =await toB64(pimage)
         //console.log(base64)
         if (pimage === null){
            localStorage.removeItem("image")
         }else{
            localStorage.setItem("image", base64)
         }
         
         setPimage(base64)
         
    }   
  
    const toB64 = (pimage) => {
            return new Promise ((resolve,reject)=>{
                const filereader = new FileReader();
                filereader.readAsDataURL(pimage)
                filereader.onload = (()=>{
                    resolve(filereader.result)
                })
                filereader.onerror = ((error)=>{
                    reject(error)   
                })

            })
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
            <div className='postbody'>
            <TextField 
                onChange={e => setPostBody(e.target.value)}
                value={description} 
                placeholder='Enter post body' 
                type = "text"
                name = "description"
                
                /> <br></br>
                <label for="set-contentType"></label>
                {/* // Link: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select 
                       author: https://developer.mozilla.org/en-US/
                       License: https://creativecommons.org/licenses/by-sa/4.0/*/}
                <select value={commonMark} onChange={e => setCommonMark(e.target.value)} name="contentType" id="ContentType">
                    <option  value="" >choose contentType--</option>
                    <option  value="text/plain">text/plain</option>
                    <option value = "text/markdown">text/markdown</option>
                    <option value = "image/png;base64">image/png;base64</option>
                    <option value = "image/jpeg;base64">image/jpeg;base64</option>
                </select>
                
            </div>

            {/* <input value={postImage} onchange = {e => setPostImage(e.target.value)} className="postbox_inputimage" placeholder='Enter a image url' type = "text" /> <br></br> */}
            {/* // link: https://www.youtube.com/watch?v=xtQ74HKTOwY */}
            <input 
                onChange={e => uploadImage(e)}
                type = "file"
                name = "post image"
                />
             <img src = {pimage} height = "200px"/>   
            {/* // link: https://stackoverflow.com/questions/38443227/how-to-get-input-text-value-on-click-in-reac
                // author: https://stackoverflow.com/
                // license:  https://creativecommons.org/licenses/by-sa/4.0/ */}
            <Button onClick = {AddPostInfo}  className = "postbox_button" >Post</Button>
            
        </form>
      
    </div>
   
  )
  
}

export default Postbox
