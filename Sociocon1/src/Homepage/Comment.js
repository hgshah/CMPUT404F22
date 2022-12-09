// link: https://github.com/azharsaleem18/react-projects/blob/main/2-instagram-app/instagram/src/components/Comments.js
// author: https://github.com/azharsaleem18
// license: https://www.apache.org/licenses/LICENSE-2.0
// this page allows me to get comments on any posts, I am setting 4 different get comments based on how its been formated based on each teams
import React from 'react'
import List from '@mui/material/List';
import  {useState, useEffect} from 'react'
import ListItem from '@mui/material/ListItem';
import Divider from '@mui/material/Divider';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import Post from './Post'
import axios from 'axios'
import Typography from '@mui/material/Typography';

import { grey } from '@mui/material/colors';
function Comment({pcurl}) {
  const [pcomment, setPostComment] = useState('');
  const [cname, setPostName] = useState('');
  const token = localStorage.getItem("token")
  const hosturl = localStorage.getItem("hosturl")
//   const Show_Comments = async () => {
        
//     await axios({
//             method: "get",
//             withCredentials: true ,
//             headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token},
//             url: pcurl + '/comments' ,
        
//     }).then((response) =>{
//        const newcom = []
        
//         newcom.push({...response.data.items[0].comment})
//         const updatecom = Object.values(newcom[0]).join('')
//         setPostComment(updatecom)


//     })
// }
useEffect(() => {
  async function getAllComments(){
      try {
              
                const p_comments = await axios.get(
                  pcurl + '/comments',

                    {headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token}},
                    
                    )
                    const icpost = []
                    const icpostname = []
                    for(let i = 0; i<1; i++){
                        
                       icpost.push(p_comments.data.items[i].comment)
                       icpostname.push(p_comments.data.items[i].author.preferredName)
                    }
                console.log(icpost)
                console.log(icpostname)
                setPostComment(icpost)
                setPostName(icpostname)
              
              
      }
      
      catch(error){
          console.log(error)
      }
      
  }
  getAllComments()
}, [])

useEffect(() => {
  async function getAllComments(){
      try {
              
                const p_comments = await axios.get(
                  pcurl + '/comments',
                
                    {headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token}},
                    
                    )
                    const icpost = []
                    const icpostname = []
                    for(let i = 0; i<1; i++){
                        
                       icpost.push(p_comments.data.comments[i].comment)
                       icpostname.push(p_comments.data.comments[i].author.displayName)
                    }
                console.log(icpost)
                console.log(icpostname)
                setPostComment(icpost)
                setPostName(icpostname)
              
              
              
      }
      
      catch(error){
          console.log(error)
      }
      
  }
  getAllComments()
}, [])
useEffect(() => {
  async function getAllComments(){
      try {
              
                const p_comments = await axios.get(
                  pcurl + '/comments',
                
                    {headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token}},
                    
                    )
                    const icpost = []
                    const icpostname = []
                    for(let i = 0; i<1; i++){
                        
                       icpost.push(p_comments.data[i].comment)
                       icpostname.push(p_comments.data[i].author.username)
                    }
                console.log(icpost)
                console.log(icpostname)
                setPostComment(icpost)
                setPostName(icpostname)
              
              
      }
      
      catch(error){
          console.log(error)
      }
      
  }
  getAllComments()
}, [])
useEffect(() => {
  async function getAllComments(){
      try {
             
                const p_comments = await axios.get(
                  pcurl + '/comments',
                
                    {headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token}},
                    
                    )
                    const icpost = []
                    const icpostname = []
                    for(let i = 0; i<1; i++){
                       
                       icpost.push(p_comments.data[i].comment)
                       icpostname.push(p_comments.data[i].author.display_name)
                    }
                console.log(icpost)
                console.log(icpostname)
                setPostComment(icpost)
                setPostName(icpostname)
              
              
      }
      
      catch(error){
          console.log(error)
      }
      
  }
  getAllComments()
}, [])
  return (
    <div className='comment'>
      <List sx={{ width: '100%', maxWidth: 360, bgcolor: 'white', border: "" }}>
        <ListItem alignItems="flex-start">
        <ListItemText
          primary={cname}
          secondary={pcomment}
        />
      </ListItem>
      <Divider variant="outset" component="li" /> 
      </List>

    </div>

  
  )
}

export default Comment
