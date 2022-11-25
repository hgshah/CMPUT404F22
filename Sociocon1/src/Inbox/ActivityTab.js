import React from 'react'
import "./styles/ActivityTab.css"
import FriendRequestsTab from './FriendRequestsTab'
import Comment from '../Homepage/Comment'
import { useState, useEffect } from 'react'

export default function ActivityTab() {
    //https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    //https://blog.logrocket.com/modern-api-data-fetching-methods-react/
    //eg. http://127.0.0.1:8000/authors/b636feb1-f85f-438c-b3a4-ce63f93d1b1d/inbox

    let host;
    let authorUUID;
    let fetchLimit = '?_limit=20';
    // remove hardcoded strings later
    let fetchURL = 'http://127.0.0.1:8000/authors/899c6088-9e1c-4f53-897f-2ca0dacf0587/inbox';
    let fetchToken = '3e1eb44206e3a7179a32841298db21435aa14bec';

    const [inboxData, setData] = useState('3');

    let currDate = Date();
    useEffect(() => {
        fetch(fetchURL, {
            method: 'GET',
            mode: 'cors',
            redirect: 'follow',
            headers: new Headers({
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + fetchToken,
            })})
            .then((response) => {
                console.log(`Response: ${response} at time ${currDate}`);
                console.log(response.json());
            })
            .then((data) => {
                console.log(data)
                setData(data);
                console.log(data.json());
                let newD;
                console.log(`Data: ${newD}`);
            })
            .catch((err) => {
                console.log(err);
            });
    }, []);
    
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
                {data &&
                    data.map(({type, items}) => (
                        <h1>{type}</h1>
                        //<h2>{items}</h2>
                    ))}
            </p> */}

        </div>
    )
}
