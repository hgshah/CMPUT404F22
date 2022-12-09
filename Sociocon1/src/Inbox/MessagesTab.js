// this page shows list of authors we want to search from any team and look at thier post
import React from 'react'
import "./styles/MessagesTab.css"
import {useState, useEffect} from 'react';
import axios from 'axios'
import { render } from '@testing-library/react';
import  ReactDOM from 'react-dom';
import { Alert, TextField, Button } from '@mui/material';
import { lightGreen } from '@mui/material/colors';
import { Card } from 'antd';

export default function MessagesTab() {
  const [authorlist, setAuthorList] = useState([])
  const [post, setPost] = useState([])
  const [remid, setRemid] = useState('')
  const [remauthid, setAuthorid] = useState('')
  const [rempost, setRempost] = useState([])
  const authorid = localStorage.getItem("authorid")
  const token = localStorage.getItem("token")  
  const [ teamname,setTeamname] = useState('')
  const Show_AuthorList = async () => {
        
    await axios({
            method: "get",
            withCredentials: true ,
            headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token},
            url: 'https://socioecon.herokuapp.com/authors/' ,
        
    }).then((response) =>{
      let array = []
      let array2 = []
      let ne = []
      console.log(response.data)
      for(let i = 0; i<response.data.items.length; i++){
       if(teamname==="team10" && response.data.items[i].host ==="socioecon.herokuapp.com"){
         localStorage.setItem("hosturl",response.data.items[i].host)
          array.push(response.data.items[i])
          array2.push(response.data.items[i].id)
       }
       else if (teamname==="team14" && response.data.items[i].host ==="social-distribution-14degrees.herokuapp.com"){
          localStorage.setItem("hosturl",response.data.items[i].host)
          array.push(response.data.items[i])
          array2.push(response.data.items[i].id)
       }
       else if(teamname==="team7" && response.data.items[i].host ==="cmput404-social.herokuapp.com") {
          localStorage.setItem("hosturl",response.data.items[i].host)
          array.push(response.data.items[i])
          array2.push(response.data.items[i].id)
       }
       else if(teamname==="team12" && response.data.items[i].host ==="true-friends-404.herokuapp.com") {
        localStorage.setItem("hosturl",response.data.items[i].host)
        array.push(response.data.items[i])
        array2.push(response.data.items[i].id)
     }
       
      }
      
      
      setAuthorList(array)
      
      setRempost(array2)
      
      


    })
}



const Show_PostList = async (rem) => {
        
  await axios({
          method: "get",
          withCredentials: true ,
          headers: { 'Content-Type': 'application/json', "Authorization": "Token " + token},
          url: 'https://socioecon.herokuapp.com/authors/' + rem + '/posts' ,
      
  }).then((response) =>{
      const remlist = []
      for(let i = 0; i<=response.data.items.length; i++){

        // console.log("name: ", response.data.items[i].author.preferredName)
        // console.log("post title: ",response.data.items[i].title)
        // console.log("post descp: ", response.data.items[i].description)
        
      }
      
          


  })
}
function handle() {
  alert("checking posts")
}


  return (
    <div className='MessagesTab'>
     
    
        <select value={teamname} onChange={e => setTeamname(e.target.value)} name="teamname" id="teamname">
                    <option  value="" >choose team</option>
                    <option  value="team7">team7</option>
                    <option value = "team12">team12</option>
                    <option value = "team14">team14</option>  
                    <option value = "team10">team10</option>  
                </select> <br/>
                <Button onClick={Show_AuthorList} className="get_btn" >Get </Button> <br/>
        <input 
                        onChange={e => setRemid(e.target.value)} 
                        value={remid} 
                        placeholder='Enter authorid' 
                        type = "text"
                        name = "rempost"
                />
                <Button onClick = {localStorage.setItem("rempostid", remid)} className="search_btn" > Search </Button>
        
        
        {
            authorlist.map((dat) => { 
              return(
                  
                  <Card> 
                    
                        {dat.preferredName}<br/> <input value = {dat.id}/>
                    
                  </Card>
                // <RPost title = {dat.preferredName} description = {dat.id}/>
              )
            }
             
        
        )}
       
        
        {/* <input value = {authorlist} /> */}
        
    </div>
  )

  
}
