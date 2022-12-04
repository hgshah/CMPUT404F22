// link: https://github.com/azharsaleem18/react-projects/blob/main/2-instagram-app/instagram/src/components/Comments.js
// author: https://github.com/azharsaleem18
// license: https://www.apache.org/licenses/LICENSE-2.0
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
import profilepic from "../MyProfile/profilepic.jpeg";
function Comment({comment}) {
  return (
    <div className='Comments_get'>
      <List sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>

      </List>

    </div>

  
  )
}

export default Comment
