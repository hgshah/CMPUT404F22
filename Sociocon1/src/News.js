import React from 'react';
import "./News.css";
function News() {
  return (
    <div className='news'>
      <div className='news_outer'>
      <h2 className='news_header'> News</h2>
      <h4> Check the weather updates</h4>
      
      <img width = "300px" src = "https://media4.giphy.com/media/YtWAe6foXLTvLRD7TN/giphy.gif?cid=ecf05e47xnt2xhr84pndkckk3a9appmnoori4lf4i0gesgcp&rid=giphy.gif&ct=g"/>
      <h3> Todays quote! </h3>
      <p> Life is amazing, value it !</p>
      <img width = "300px" src = "https://th.bing.com/th/id/R.c5f4201f6a464e5005217fdb1b06fb7e?rik=9bTsj8CpBmZIMw&pid=ImgRaw&r=0"/>
      
        <h5>Hows you feeling today?</h5>
       Excited?  <input type = 'radio' value='excited'></input> <br></br>
       Happy?  <input type = 'radio' value='happy'></input> <br></br>
       tired?  <input type = 'radio' value='tired'></input>

      </div>
    </div>
  )
}

export default News
