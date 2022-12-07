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
import { Card } from 'antd';
import Postbox from './Homepage/Postbox';
import { Construction, DataSaverOffTwoTone, LocalConvenienceStoreOutlined, ReceiptLongOutlined } from '@mui/icons-material';
// link: https://contactmentor.com/login-form-react-js-code/
// author: https://contactmentor.com/
//license: https://contactmentor.com/
//link :https://bobbyhadz.com/blog/react-onclick-redirect
//author: https://bobbyhadz.com/
// license: https://bobbyhadz.com/terms-and-conditions
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
      "username": "super",
      "password": "super",
      "is_staff": true,
      "is_superuser": true
    },
    {
      "username": "amanda6",
      "password": "amanda6",
      "is_staff": true,
      "is_superuser": true
    },
    {
      "username": "team12_user",
      "password": "team12_user",
      "is_staff": true,
      "is_superuser": true
    },
    {
      "username": "hsmalhi",
      "password": "hsmalhi",
      "is_staff": true,
      "is_superuser": true
    },
    {
      "username": "manuba",
      "password": "manuba",
      "is_staff": true,
      "is_superuser": true
    },
    {
      "username": "junhong1",
      "password": "junhong1",
      "is_staff": true,
      "is_superuser": true
    },
    {
      "username": "hgshah",
      "password": "hgshah",
      "is_staff": true,
      "is_superuser": true
    },
    {
      "username": "actor",
      "password": "actor"
    },
    {
      "username": "target",
      "password": "target"
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
    localStorage.setItem("displayedName", uname.value)
     await axios({
            method:'post',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            // url: 'http://127.0.0.1:8000/authors/fdb67522-b0e6-45bb-8896-73972c2147ed/posts' + nid + '/',
            url: 'https://socioecon.herokuapp.com/tokens/',
            data: formField_token,
        
    }).then((login_info) =>{
        
        
         const info_token_send = [];
         const info_token =[];
         const info_authorid = [];
         const info_preferredName = []
         info_token_send.push({...login_info.data})
         info_token.push({...login_info.data.token})
         info_authorid.push({...login_info.data.author.id})
         info_preferredName.push({...login_info.data.author.preferredName})
         const newinfo_token = Object.values(info_token[0]).join('')
         const newinfo_authorid = Object.values(info_authorid[0]).join('')
        // console.log(newinfo_token)
        // console.log(newinfo_authorid)
        setAuthorid(info_token_send)
        //link :https://www.youtube.com/watch?v=HTSAJna3X8c
        //author: https://www.youtube.com/@codingcomics
        //license: https://creativecommons.org/
        console.log(info_token_send)
        localStorage.setItem("authorid", Object.values(info_authorid[0]).join(''))
        localStorage.setItem("token", Object.values(info_token[0]).join(''))
        localStorage.setItem("preferredName", Object.values(info_preferredName[0]).join(''))
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


  const renderErrorMessage = (name) =>
  name === errorMessages.name && (
    <div className="error">{errorMessages.message}</div>
  );

  return (
    <div className="form">
      <h2> LOGIN </h2> 
      <form >
        <div className="input-container">
          <Card>
            <div>
              <label>Username </label>
              <input type="text" name="uname" required />  <br/>
              {renderErrorMessage("uname")} <br></br>
            </div>
            <div>
              <br></br>
              <label>Password </label>
              <input type="password" name="pass" required /> <br/> 
              {renderErrorMessage("pass")}  <br></br>
            </div>
           
          </Card>
          
        </div>
        <div className="input-container">
          <Button style={{ backgroundColor: "white" }} onClick = {handleSubmit} > Submit </Button>
              
            
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
