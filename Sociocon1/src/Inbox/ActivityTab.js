import React from 'react'
import "./styles/ActivityTab.css"
import FriendRequestsTab from './FriendRequestsTab'
import Comment from '../Homepage/Comment'
import { useState, useEffect } from 'react'
import axios from 'axios'

export default function ActivityTab() {
    //https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    //https://blog.logrocket.com/modern-api-data-fetching-methods-react/
    //eg. http://127.0.0.1:8000/authors/b636feb1-f85f-438c-b3a4-ce63f93d1b1d/inbox

    // useEffect(async () => {
    //     await fetch(fetchURL, {
    //         method: 'GET',
    //         mode: 'cors',
    //         redirect: 'follow',
    //         headers: new Headers({
    //                 'Content-Type': 'application/json',
    //                 'Authorization': 'Token ' + fetchToken,
    //         })})
    //         .then((response) => {
    //             console.log(`Response: ${response} at time ${currDate}`);
    //             console.log(response.json());
    //             console.log(response.items);
    //         })
    //         .then((data) => {
    //             console.log(data)
    //             setData(data);
    //             console.log(data.json());
    //             let newD;
    //             console.log(`Data: ${newD}`);
    //         })
    //         .catch((err) => {
    //             console.log(err);
    //         });
    // }, []);

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
    console.log(testObj);

    let fetchHost = '127.0.0.1:8000';
    let fetchAuthorUUID = '899c6088-9e1c-4f53-897f-2ca0dacf0587';
    let fetchToken = '3e1eb44206e3a7179a32841298db21435aa14bec'; //user token here
    let fetchLimit = '?_limit=20';

    let fetchURL = '';
    fetchURL = 'http://' + fetchHost;
    fetchURL = fetchURL + '/authors/';
    fetchURL = fetchURL + fetchAuthorUUID;
    fetchURL = fetchURL + '/inbox/';
    fetchURL = 'http://127.0.0.1:8000/authors/899c6088-9e1c-4f53-897f-2ca0dacf0587/inbox';

    const [inboxData, setData] = useState([]);

    let currDate = Date();
    useEffect(() => {
        axios.get(fetchURL, {
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + fetchToken,
        }})
        .then((data) => {
            console.log(data);
            console.log(data.data);
            //setData(data.data);
            console.log(data.data.items)
            setData(data.data.items);
            setData(testObj); //temp
        })
    }, []);
    
    console.log(`Date: ${currDate} | Data: ${inboxData}`);
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
            <p>test</p>

            <hr></hr>

            <span>{inboxData}</span>
            
            {/* <ul>
                {inboxData.map((inboxData) => {
                    return(
                        <li>{inboxData.type}</li>
                    )
                })}

            </ul> */}


            {/* <p>
                {inboxData &&
                    inboxData.map(({items}) => (
                        <h1>{type}</h1>
                        //<h2>{items}</h2>
                    ))}
            </p> */}

        </div>
    )
}
