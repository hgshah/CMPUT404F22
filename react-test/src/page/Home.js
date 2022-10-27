import React from 'react'
import { useState } from "react";
import "./Home.css";
import {TestFetcher} from "./TestFetcher";

const Home = () => {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [author, setAuthor] = useState('mario');
  const handleSubmit = (e) => {
    e.preventDefault();
    const blog = { title, body, author };
  }

  TestFetcher();

  return (
    <div>
      
      <h1> Home Page </h1>
      <form onSubmit={handleSubmit}>
        <label>Post Title:</label>
        <input 
          type="text" 
          required 
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        /> <br></br> 
        <label>Post body:</label>
        <textarea
          required
          value={body}
          onChange={(e) => setBody(e.target.value)}
        ></textarea> <br></br>
        <label>Post author:</label>
        <select
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
        >
          <option value="Harsh">Harsh</option>
          <option value="Nancy">Nancy</option> <br></br>
        </select> <br></br>
        <button>Add Post</button>
      </form>
    </div>
  )
}
export default Home
