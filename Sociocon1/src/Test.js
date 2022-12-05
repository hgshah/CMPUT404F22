import React from 'react'
import axios from 'axios'
import {useState, useEffect} from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Divider from '@mui/material/Divider';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';

function Test() {
    const[value, setValue] = useState(""); 
    const[p_post, setPost] = useState([]); 
    function handle() {
        alert(value)
    }
    useEffect(() => {
        async function getAllPosts(){
            try {
                    const p_post = await axios.get("http://localhost:8000/posts/public/")
                    console.log(p_post.data)
                    setPost(p_post.data)
            }
            catch(error){
                console.log(error)
            }
        }
        getAllPosts()
    }, [])
  return (
    <div>
    <List sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
        <ListItem alignItems="flex-start">
        <ListItemAvatar>
           
        </ListItemAvatar>
        <ListItemText
            primary="Harsh Shah"
            secondary = 
            {
                p_post.map((posts) => {
                    return (
                        <h2 key={posts.id}>
                            {posts.title} <br></br>
                            {posts.description}
                        </h2>
                    )
                })
            }
        />
    </ListItem>
    </List>
    </div>
  )
}

export default Test
