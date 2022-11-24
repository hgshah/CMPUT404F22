import React from 'react'
import "./styles/ActivityTab.css"
import FriendRequestsTab from './FriendRequestsTab'
import Comment from '../Homepage/Comment'
import { useState, useEffect } from 'react'

export default function ActivityTab() {
    //eg. http://127.0.0.1:8000/authors/b636feb1-f85f-438c-b3a4-ce63f93d1b1d/inbox

    let host;
    let authorUUID;
    let fetchLimit = '?_limit=20'
    let fetchURL = 'http://127.0.0.1:8000/authors/b636feb1-f85f-438c-b3a4-ce63f93d1b1d/inbox';

    let [data, setData] = useState(null);

    let fetchData;
    useEffect(() => {
        fetch(fetchURL)
            .then((response) => console.log(response))
            .then((data) => {
                console.log(data);
                fetchData = data;
                setData = data;
            })
            .catch((err) => {
                console.log(err);
            });
    }, []);
    
    /*
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

            <p>
                {data &&
                    data.map(({type, items}) => (
                        <h1>{type}</h1>
                        //<h2>{items}</h2>
                    ))}
            </p>

        </div>
    )
}
