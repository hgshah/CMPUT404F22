// link: https://media4.giphy.com/media/YtWAe6foXLTvLRD7TN/giphy.gif?cid=ecf05e47xnt2xhr84pndkckk3a9appmnoori4lf4i0gesgcp&rid=giphy.gif&ct=g
// author: https://giphy.com/
// license: https://giphy.com/
// link:https://th.bing.com/th/id/R.c5f4201f6a464e5005217fdb1b06fb7e?rik=9bTsj8CpBmZIMw&pid=ImgRaw&r=0"
// author: https://th.bing.com/th/id/R.c5f4201f6a464e5005217fdb1b06fb7e?rik=9bTsj8CpBmZIMw&pid=ImgRaw&r=0"
// license: https://th.bing.com/th/id/R.c5f4201f6a464e5005217fdb1b06fb7e?rik=9bTsj8CpBmZIMw&pid=ImgRaw&r=0"
import React from 'react';
import "./News.css";
function News() {
  return (
    <div className='news'>
      <div className='news_outer'>
      
      <h3> Check the weather updates</h3>
      
      <img width = "300px" src = "https://media4.giphy.com/media/YtWAe6foXLTvLRD7TN/giphy.gif?cid=ecf05e47xnt2xhr84pndkckk3a9appmnoori4lf4i0gesgcp&rid=giphy.gif&ct=g"/>
      <h3> Todays quote! </h3>
      <p> Life is amazing, value it !</p>
      <img width = "300px" src = "https://th.bing.com/th/id/R.c5f4201f6a464e5005217fdb1b06fb7e?rik=9bTsj8CpBmZIMw&pid=ImgRaw&r=0"/>
      
        <h3>How you feeling today?</h3>
       Sad?  <input  type = 'radio' value='excited'></input> <br></br>
       Happy?  <input type = 'radio' value='happy'></input> <br></br>
       

      </div>
    </div>
  )
}

export default News
