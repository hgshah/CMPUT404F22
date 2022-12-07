// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0
import React from 'react'
import {useState, useEffect} from 'react';
import "./Post.css";
import List from '@mui/material/List';
import Comment from './Comment';
import {useNavigate, useParams} from 'react-router-dom'
import { Avatar, Button, TextField} from '@mui/material';
// import profilepic from "../MyProfile/profilepic.jpeg";
import CommentIcon from '@mui/icons-material/ModeComment';
import ShareIcon from '@mui/icons-material/Share';
import SendIcon from '@mui/icons-material/Send';
import ReactDom from 'react-dom'
import ReactMarkdown from 'react-markdown'
import DeleteIcon from '@mui/icons-material/Delete';
import LikeIcon from '@mui/icons-material/FavoriteBorder';
import EditIcon from '@mui/icons-material/Edit';
import { Link } from 'react-router-dom';
import { Send } from '@mui/icons-material';
import axios from 'axios'
import Login from '../Login';
import EditPost from './EditPost';
function Post({displayName, title, description, text, image, avatar, visibility,contenttype, purl, post_authorid, comm, published}) {
    const[value, setValue] = useState(""); 
    const authorid = localStorage.getItem("authorid")
    const token = localStorage.getItem("token")
    // const [userName, setUserName] = useState('');
    const[followButtonText, newFollowButtonText] = useState("Follow");
    const[following, setFollowing] = useState(false);
    const [showForm, setShowForm] = useState(false);
    const [updatetitle, setPostTitle] = useState('')
    const [updatebody, setPostBody] = useState('')
    const [updatevisibility, setPostVisibility] = useState('')
    const [comment, setPostComment] = useState('');
    const [ContentType, setPostContentType] = useState('');
    const [like, setPostLike] = useState(1);
    const [likeactive, setPostLikeactive] = useState(false);
    const [comments, setComments] = useState([])
    const [likes, setLikes] = useState([])
    //const[p_post, setPost] = useState([]); 
    // link : https://www.youtube.com/watch?v=a8KruvMkEtY
    // author: https://www.youtube.com/@ahmedelgammudi
    // license: https://creativecommons.org/
   
    function handle() {
        alert("cant share right now")
    }
    const AddComment = async () => {
        let formField = new FormData()
        formField.append("comment", comment)
        formField.append("contentType", "text/plain")
        console.log(formField)
        await axios({
            method: 'post',
            withCredentials: true ,
            headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token},
            url: purl + '/comments' ,
            data: formField
        }).then((response) =>{
            console.log(response.data)
            
        })
    }

    const UpdatePost = async () => {
        let formField = new FormData()
        formField.append("title", updatetitle)
        formField.append("description", updatebody)
        await axios({
            method: 'post',
            withCredentials: true ,
            headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token},
            // url: 'http://localhost:8000/authors/1384c9c1-1e2d-4b7f-868b-4f3c499fe3cd/posts/',
            // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
            // url: 'http://127.0.0.1:8000/authors/9a3123af-c9fa-42ba-a8d4-ca620e56fdb6',
            
            url: purl + '/',

            data: formField
        }).then((response) =>{
            console.log(response.data)
            
        })
    }
    
   
    const navigate = useNavigate()
    
    const DeletePostInfo = async () => {
        // String(id)
        // const nid = String(id).slice(-36)
       
        await axios({
                method:'delete',
                withCredentials: true ,
                headers: { "Authorization": "Token " + token},
                // url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts' + nid + '/',
                url: purl
                
        }).then((response) =>{
            console.log(response.data)
            console.log(purl)
            
        })
    }

    const PostInfo_Likes = async () => {
        
        Show_Likes()

        let formField12 = new FormData()
        formField12.append("type","like")
        formField12.append("object",purl)
        await axios({
                method:'post',
                withCredentials: true ,
                headers: {'Content-Type': 'application/json' , "Authorization": "Token " + token},
                // url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts' + nid + '/',
                url: 'https://socioecon.herokuapp.com/authors/' + authorid + '/inbox',
                data: formField12
            
        }).then((response) =>{
            console.log(response.data)
            console.log(purl)
           
        })
        
    }

    const follow_clicked = async() => {
        if (followButtonText == "Follow") {
            //send the request
            newFollowButtonText("Following");
        } else {
            //unsend the reqeust when following is click
            newFollowButtonText("Follow")
        }

        //show the friend request is sent
        setFollowing(!following);
        console.log(post_authorid)
        await axios({
            method:'post',
            withCredentials: true,
            headers: {'Content-Type':'application/json', "Authorization": "Token " + token},
            url: 'https://socioecon.herokuapp.com/authors/' + post_authorid + '/followers/',
            // data: formField_follow
        }).then((response) => {
            console.log(response.data)
            
        })
    }
    function edit () {
        
        alert("working?")
          
    }

    const Share_Post = async () => {

        

        let formField_share = new FormData()
        formField_share.append("object",purl)
        
        await axios({
                method:'put',
                withCredentials: true ,
                headers: {'Content-Type': 'application/json', "Authorization": "Token " + token},
                // url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts' + nid + '/',
                url: purl + '/share',
                data: {"object": purl}
            
        }).then((response) =>{
            console.log(response.data)
            console.log(purl)
            
        })
    }

    const Show_Comments = async () => {
        
        await axios({
                method: "get",
                withCredentials: true ,
                headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token},
                url: purl + '/comments' ,
            
        }).then((response) =>{
           const newcom = []
            
            newcom.push({...response.data.items[0].comment})
            const updatecom = Object.values(newcom[0]).join('')
            setComments(updatecom)


        })
    }
    const Show_Likes = async () => {
        
        await axios({
                method: "get",
                withCredentials: true ,
                headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token},
                url: purl + '/likes' ,
            
        }).then((response) =>{
            
            setLikes(response.data.length)
        //    const newlike = []
            
        //     newlike.push({...response.data.items[0].comment})
        //     const updatecom = Object.values(newcom[0]).join('')
        //     setComments(updatecom)


        })
    }

    useEffect(() => {
        async function updateFollowBtn() {

        // if(newFollowButtonText === "Follow") {
            await axios.get('https://socioecon.herokuapp.com/authors/' + post_authorid + '/followers/' + authorid, {
                headers: {"Content-Type":"application/json", "Authorization": "Token " + token}
            }).then((response) => {
                    setFollowing(!following);
                    newFollowButtonText("Following")
            })
        // } else {
        //     await axios.delete('https://socioecon.herokuapp.com/authors/')
        // }
    }
    updateFollowBtn()
    }, []) //something here newFollowButtonText



  return (
    <div className='post'>
        <div className = "post_avatar">
            <Avatar src = {avatar}/>
            
        </div>
        <div className='post_body'>
            <h5>
                  {published}
            </h5>
           
            <div className='post_header'>
            
            <React.Fragment>
                    {
                        showForm ? (
                        <form>
                            <div>
                            <input onChange={e => setPostTitle(e.target.value)} 
                                value={updatetitle} 
                                placeholder='Enter Title' 
                                type = 'text'
                                className='post_input'
                                variant = 'outlined'
                                label = "add title"
                                size = "small"
                             />  
                            </div>  
                            <div>
                              
                            <input onChange={e => setPostBody(e.target.value)} 
                                value={updatebody} 
                                placeholder='Enter Body' 
                                type = 'text'
                                className='post_input'
                                variant = 'outlined'
                                label = "add body"
                                size = "small"
                             />
                            </div>
                            <div>
                              
                              <select name="contenttype" id="contenttype">
                                    <option value="">choose an option--</option>
                                    <option value = {updatevisibility} onChange={e => setPostContentType(e.target.value)} >public</option>
                                    <option value = {updatevisibility} onChange={e => setPostContentType(e.target.value)} >friends</option>
                                </select>
                                <button onClick = {UpdatePost}>Update</button>
                                <button onClick = {() => setShowForm(false)} > Cancel</button>
                            </div>
                        </form>) 
                        : (<Button onClick = {() => setShowForm(true)}  variant='contained' size = "small" endIcon= {<EditIcon/>} >Edit</Button>)
                    }
                     
             </React.Fragment>
                
                <div className='header_text'>
                
                    <h2>
                        {displayName} {" "} <span></span>
                        
                        
                        
                        <span className='follow_span'> 
                            <Button 
                            className='follow_btn' 
                            onClick={follow_clicked}
                            style={{backgroundColor: following ? "rgb(211, 211, 211)" : "rgb(159, 185, 31)"}} >
                                {/* {following ? "Following" : "Follow"} */}
                                {followButtonText}
                            </Button>
                            {/* hardcode */}
                            {/* <input 
                            onChange={e => setUserName(e.target.value)}
                            value={userName} 
                            placeholder='Enter post body' 
                            type = "text"
                            name = "description"
                            /> */}
                        </span>
                    </h2>
                    
                </div>
                <div className='visibility'>
                    <h4>
                         {visibility} 
                    </h4>
                </div>
                <div className = "post_headerdis">
                    
                    {/* <p>{text}</p> */}
                    <h5>
                    {title} 
                    
                    </h5>
                    
                    <ReactMarkdown>{description}</ReactMarkdown>
                    
                    


                </div>
                
                 <img width = "300px" className='post_content' src = {image} alt = " "/> 

                
                 <form>
                    <span>
                        <Button onClick={PostInfo_Likes} variant='contained' size = "small" endIcon= {<LikeIcon/>} >  {likes}  </Button>  &nbsp;&nbsp;&nbsp;
                        <Button onClick = {Share_Post} variant='contained' size = "small" endIcon= {<ShareIcon/>} >Share</Button> &nbsp;&nbsp;&nbsp;
                        <Button onClick = {Show_Comments} variant='contained' size = "small" endIcon= {<CommentIcon/>} > See Comments</Button> 
                        
                    </span>

                    </form>
                    <div className='post_comments'>
                        <p> <Comment pcurl = {purl}/> </p> 
                    </div>
                    
                    
                    
                   
                    
                <div className='post_footer'>
                 

                {/* /* // link: https://stackoverflow.com/questions/38443227/how-to-get-input-text-value-on-click-in-reac
                // author: https://stackoverflow.com/
                // license:  https://creativecommons.org/licenses/by-sa/4.0/ */}
                        {/* <input type = "text" value={value} onChange={(e) => {setValue(e.target.value)}} placeholder = "Write a comment" /> */}
                        {/* <LikeIcon fontSize = "small" />
                        <ShareIcon fontSize = "small" /> */}
                     <div className='post_comments'>
                        {/* <Comment/> */}
                        
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
                                    <option onChange={e => setPostContentType(e.target.value)} value={ContentType}>text/markdown</option>
                                    <option onChange={e => setPostContentType(e.target.value)} value={ContentType}>text/plain</option>
                                </select>
                            {/* <TextField label = "add comment"  size = "small" variant='outlined' className='post_input' placeholder='add comment' /> */}

                            <Button onClick = {AddComment} variant='contained' size = "small" endIcon= {<SendIcon/>}  >   </Button> 
                            
                        </form> 
                        <Button onClick = {DeletePostInfo} variant = 'contained' endIcon = {<DeleteIcon/>} className = "postdel_button" type = "submit"> Delete</Button>
                        
                    </div> 
                    {/* <div className='getcomments'>
                    <h4>
                         {comments} 
                    </h4>
                </div> */}
 
                       
                   
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
