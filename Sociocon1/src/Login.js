import React from 'react'
import Sidebar from './Sidebar'
import {useState, useEffect} from 'react';
import {useNavigate, useParams} from 'react-router-dom'
import axios from 'axios'
import "./Login.css"
import { Avatar, Button, getAccordionDetailsUtilityClass, TextField} from '@mui/material';
import Post from './Homepage/Post';
import Feed from './Homepage/Feed';
import Home from './Homepage/Home'
import Postbox from './Homepage/Postbox';
import { Construction, DataSaverOffTwoTone, LocalConvenienceStoreOutlined, ReceiptLongOutlined } from '@mui/icons-material';
// link: https://contactmentor.com/login-form-react-js-code/
//link :https://bobbyhadz.com/blog/react-onclick-redirect
function Login() {
  const [errorMessages, setErrorMessages] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [token1, setToken] = useState('')
  const [authorid1, setAuthorid] = useState([])
  const navigateHome = () => {

    // 👇️ navigate to /
    navigate('/home');
  };
  
  const navigate = useNavigate();
  // User Login info
  const database = [
    {
      username: "hgshah",
      password: "hgshah",

    },
    {
      username: "hgshah1",
      password: "hgshah1",

    },
    {
      username: "amanda",
      password: "amanda",

    },
    {
      username: "allan",
      password: "allan",

    },
    {
      username: "john",
      password: "john",

    },
    {
      username: "harkirat",
      password: "harkirat",
    }
  ];

  const errors = {
    uname: "invalid username",
    pass: "invalid password"
  };

  


  const PostToken = async () => {
    var { uname, pass } = document.forms[0];
    

    // Find user login info
    // const userData = database.find((user) => user.username === uname.value && user.pass === pass.value);

    let formField_token = new FormData()
    formField_token.append("username",uname.value)
    formField_token.append("password", pass.value)
    
     await axios({
            method:'post',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            // url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts' + nid + '/',
            url: 'http://127.0.0.1:8000/tokens/',
            data: formField_token,
        
    }).then((login_info) =>{
        
        
         const info_token_send = [];
         const info_token =[];
         const info_authorid = [];
         info_token_send.push({...login_info.data})
         info_token.push({...login_info.data.token})
         info_authorid.push({...login_info.data.author.id})
         const newinfo_token = Object.values(info_token[0]).join('')
         const newinfo_authorid = Object.values(info_authorid[0]).join('')
        // console.log(newinfo_token)
        // console.log(newinfo_authorid)
        setAuthorid(info_token_send)
        
        localStorage.setItem("authorid", Object.values(info_authorid[0]).join(''))
        localStorage.setItem("token", Object.values(info_token[0]).join(''))
        
    })
    
}
  



  const handleSubmit = (event) => {
    //Prevent page reload
    event.preventDefault();

    var { uname, pass } = document.forms[0];
    
    
    // Find user login info
    const userData = database.find((user) => user.username === uname.value);
    
    // Compare user info
    if (userData) {
      if (userData.password !== pass.value) {
        // Invalid password
        setErrorMessages({ name: "pass", message: errors.pass });
      } else {
        
        setIsSubmitted(true);
        
        PostToken();
        navigateHome();
        
        
      }
    } else {
      // Username not found
      setErrorMessages({ name: "uname", message: errors.uname });
    }
    
  };


  // Generate JSX code for error message
  // const renderErrorMessage = (name) =>
  //   name === errorMessages.name && (
  //     <div className="error">{errorMessages.message}</div>
  //   );

  // JSX code for login form
  // const renderForm = (
  //   <div className="form">
  //     <form onSubmit={handleSubmit}>
  //       <div className="input-container">
  //         <label>Username </label>
  //         <input type="text" name="uname" required />
  //         {renderErrorMessage("uname")}
  //       </div>
  //       <div className="input-container">
  //         <label>Password </label>
  //         <input type="password" name="pass" required />
  //         {renderErrorMessage("pass")}
  //       </div>
  //       <div className="button-container">
  //           <input type="submit" />
  //       </div>
  //     </form>
  //   </div>
  // );
//   <div className="app">
//   <div className="login-form">
//     <div className="title">Sign In</div>
//     <div>
     
//             {
//                 authorid1.map((autho) => {
//                     return <p> {autho.author.id}</p>
//                 })
//             }
      
//     </div>
//     {isSubmitted ? <div></div> : renderForm}
    
//   </div>

  
       
// </div>

  return (
    <div className="form">
      <form >
        <div className="input-container">
          <label>Username </label>
          <input type="text" name="uname" required />
          
        </div>
        <div className="input-container">
            <label>Password </label>
            <input type="password" name="pass" required />
            <button onClick = {handleSubmit} > Submit </button>
            {isSubmitted}
            
                {
                    authorid1.map((autho) => {
                        return <p>  {autho.author.id} 
                                
                        </p>
                    })
                }
        </div>
      </form>
    </div>

  );
}
export default Login
