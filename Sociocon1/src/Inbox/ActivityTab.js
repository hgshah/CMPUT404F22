import React from 'react'
import "./styles/ActivityTab.css"
import FriendRequestsTab from './FriendRequestsTab'
import Comment from '../Homepage/Comment'
import { useState, useEffect } from 'react'
import axios from 'axios'
import Post from '../Homepage/Post'
import { Avatar, Button, TextField } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';

export default function ActivityTab() {
    // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    // https://blog.logrocket.com/modern-api-data-fetching-methods-react/
    // eg. http://127.0.0.1:8000/authors/b636feb1-f85f-438c-b3a4-ce63f93d1b1d/inbox

    let testObj = JSON.stringify({
        "type": "Like",
        "summary": " likes your comment",
        "author": {
            "id": "899c6088-9e1c-4f53-897f-2ca0dacf0587",
            "url": "http://127.0.0.1:8000/authors/899c6088-9e1c-4f53-897f-2ca0dacf0587",
            "host": "127.0.0.1:8000",
            "type": "author",
            "github": "",
            "displayName": "",
            "profileImage": ""
        },
        "object": "324324"
    });
    //console.log(testObj);

    let fetchHost = '127.0.0.1:8000';
    let fetchAuthorUUID = '899c6088-9e1c-4f53-897f-2ca0dacf0587';
    let fetchToken = '3e1eb44206e3a7179a32841298db21435aa14bec'; // user token here
    let fetchLimit = '?_limit=20'; // how tmuch to display per load

    let fetchURL = '';
    fetchURL = 'http://' + fetchHost;
    fetchURL = fetchURL + '/authors/';
    fetchURL = fetchURL + fetchAuthorUUID;
    fetchURL = fetchURL + '/inbox/';

    fetchURL = 'http://127.0.0.1:8000/authors/899c6088-9e1c-4f53-897f-2ca0dacf0587/inbox'; //temp

    const [inboxData, setData] = useState([]);

    let currDate = Date();
    useEffect(() => {
        console.log(`New fetch at time: ${currDate}`);
        axios.get(fetchURL, {
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + fetchToken,
        }})
        .then((data) => {
            console.log(data);
            console.log(data.data);
            //setData(data.data);
            console.log(data.data.items);
            setData(data.data.items);
            //setData(testObj); //temp, array is empty from inbox uri 
        })
    }, []);
    
    console.log(`Date: ${currDate} | Data: ${inboxData}`);

    for (const element of inboxData) {
        // console.log(element);
        // console.log(element.type);
        const actDiv = document.getElementById('activityList');

        if (element.type == 'post') {
            const actPara = document.createElement('div');
            let postContent = '';
            //let postObj = {element.author.displayName}
            // let postBody = Post(
            //     purl=element.url, 
            //     title=element.title, 
            //     description=element.description, 
            //     displayName=element.author.displayName, 
            //     image="", 
            //     avatar="", 
            //     visibility="public");
            let thing = <Post purl = {element.url} title = {element.title} description = {element.description} displayName = {element.author.displayName}  image = "" avatar = "" visibility = "public"/>;

            postContent += `Post title: ${element.title} \n`;
            postContent += `Desc: ${element.description} '\n'`;
            actPara.innerHTML = `
                <div style="color:green; border: 1px solid black;">
                <p> ${thing} </p> 
                <p> ${postContent} </p>
                <a href=''>link</a>
                </div>`;
            actDiv.appendChild(actPara);
            
    
        } else if (element.type == 'comment') {
            const actPara = document.createElement('div');
            actPara.innerText = 'new comment added ' + String(element.title);
            actPara.innerText = element.comment;
            actDiv.appendChild(actPara);


        } else if (element.type == 'like') {
            const actPara = document.createElement('p');
            actPara.innerText = 'new like added ' + String(element.title);
            actDiv.appendChild(actPara);


        } else {
            const actPara = document.createElement('p');
            actPara.innerText = 'you goofed (activities tab';
            actDiv.appendChild(actPara);
        }
    }

    // inboxData.forEach(item => {
    //     for (let key in item) {
    //         console.log(`${key} and ${item[key]}`);
    //     }
    // });
    //let parsedData = JSON.parse(inboxData);
    //console.log(`${parsedData}, ${parsedData.type}`)

    /* inbox structure
    {
        "type": "inbox",
        "author": {
            "type": "author",
            "id": "b636feb1-f85f-438c-b3a4-ce63f93d1b1d",
            "url": "http://127.0.0.1:8000/authors/b636feb1-f85f-438c-b3a4-ce63f93d1b1d",
            "host": "127.0.0.1:8000",
            "displayName": "",
            "github": "",
            "profileImage": ""
        },
        "items": [...]
    }
    */
    return (
        <div className='ActivityTab'>
            <hr></hr>
            <ul id='activityList'> 
            </ul>
        </div>
    )
}
