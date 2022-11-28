import React from 'react'
import "./styles/MessagesTab.css"
import {useState, useEffect} from 'react';
import axios from 'axios'
import RPost from './RPost';
import { render } from '@testing-library/react';
import  ReactDOM from 'react-dom';
export default function MessagesTab() {
  const [authorlist, setAuthorList] = useState([])
  const [post, setPost] = useState([])
  const [rempost, setRempost] = useState([])
  const authorid = localStorage.getItem("authorid")
  const token = localStorage.getItem("token")  
  const autid = localStorage.getItem("id")
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
       array2.push(response.data.items[i])
        
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
      for(let i = 0; i<100; i++){
        console.log(response.data.items[i].author.preferredName,response.data.items[i].title, response.data.items[i].title )
      }
      
          


  })
}

  return (
    <div className='MessagesTab'>
     
        <button onClick={Show_AuthorList} >Get</button>
        {
            authorlist.map((dat) => { 
              return(
                  console.log(dat.preferredName)
                // <RPost title = {dat.preferredName} description = {dat.id}/>
              )
            }
             
        
        )}
        {
            rempost.map((datt) => { 
              return(
                  Show_PostList(datt.id)
                // <RPost title = {dat.preferredName} description = {dat.id}/>
              )
            }
             
        
        )}
        
        {/* <input value = {authorlist} /> */}
        
        
    </div>
  )

  
}
