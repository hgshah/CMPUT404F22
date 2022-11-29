import React from 'react'
import "./styles/MessagesTab.css"
import {useState, useEffect} from 'react';
import axios from 'axios'
import RPost from './RPost';
import { render } from '@testing-library/react';
import  ReactDOM from 'react-dom';
import { Alert } from '@mui/material';
export default function MessagesTab() {
  const [authorlist, setAuthorList] = useState([])
  const [post, setPost] = useState([])
  const [rempost, setRempost] = useState([])
  const authorid = localStorage.getItem("authorid")
  const token = localStorage.getItem("token")  
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
      for(let i = 0; i<34; i++){
       
       array.push(response.data.items[i])
       array2.push(response.data.items[i].id)
       
       
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
      for(let i = 0; i<40; i++){
        console.log("name: ", response.data.items[i].author.preferredName)
        console.log("post title: ",response.data.items[i].title)
        console.log("post descp: ", response.data.items[i].description)
        
      }
      
          


  })
}
function handle() {
  alert("checking posts")
}

  return (
    <div className='MessagesTab'>
     
        <button onClick={Show_AuthorList} >Get</button>
        
        
        {
            authorlist.map((dat) => { 
              return(
                  
                  <p> {dat.preferredName}<button onClick= {Show_PostList(dat.id)}> check posts</button></p>
                // <RPost title = {dat.preferredName} description = {dat.id}/>
              )
            }
             
        
        )}
       
        
        {/* <input value = {authorlist} /> */}
        
        
    </div>
  )

  
}
