import React from 'react'
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Divider from '@mui/material/Divider';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';
import profilepic from "./profilepic.jpeg";
function Comment() {
  return (
    <List sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
    <ListItem alignItems="flex-start">
      <ListItemAvatar>
        <Avatar alt="Remy Sharp" src={profilepic} />
      </ListItemAvatar>
      <ListItemText
        primary="Harsh Shah"
        secondary={
          <React.Fragment>
            <Typography
              sx={{ display: 'inline' }}
              component="span"
              variant="body2"
              color="text.primary"
            >
              Haha this GIF is hilarious
            </Typography>
            {/* {" —"} */}
          </React.Fragment>
        }
      />
    </ListItem>

    <Divider variant="inset" component="li" />
    <ListItem alignItems="flex-start">
      <ListItemAvatar>
        <Avatar alt="Cindy Baker" src="https://as1.ftcdn.net/v2/jpg/04/06/23/12/1000_F_406231299_870DsmnqtSrS39CB35UC5wfQcxDS80Y6.jpg" />
      </ListItemAvatar>
      <ListItemText
        primary="nancys_art"
        secondary={
          <React.Fragment>
            <Typography
              sx={{ display: 'inline' }}
              component="span"
              variant="body2"
              color="text.primary"
            >
              Congratulations! on your first post!
            </Typography>
           
          </React.Fragment>
        }
      />
    </ListItem>
  </List>
  
  )
}

export default Comment
