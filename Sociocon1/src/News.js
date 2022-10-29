import React from 'react';
import "./News.css";
import {TestFetcher} from "./page/TestFetcher"

function News() {
    return (
    <div className='news'>
      <h2> News</h2>
      <h2> Coming soon in next part!</h2>
        {
            /*
            Hello! let me inject my TestFetcher!
            Do not delete. We'll use this as reference!
            */
            // TestFetcher()
        }
    </div>
  )
}

export default News
