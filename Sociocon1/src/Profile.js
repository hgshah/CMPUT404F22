import React from 'react'
import Sidebar from './Sidebar'
import News from './News'
import ReactMarkdown from 'react-markdown'
import Postbox from './Homepage/Postbox'
import  {useEffect, useState} from 'react'
import ReactDom from 'react-dom'
//link :https://www.youtube.com/watch?v=ygV99J2Ehjs

function Profile() {
  const [markdown,setMarkdown] = useState('')

  function convert(){
    console.log(ReactDom.render(<ReactMarkdown>{markdown}</ReactMarkdown>, document.body))
  }

  return (
    
    <div className='profile'>
      <Sidebar/>
      
      <input 
                onChange={e => setMarkdown(e.target.value)} 
                value= {markdown} 
                placeholder='Enter commonMark' 
                type = "text"
                name = "markdown"
                />
      <button onClick={convert}>Convert</button>
      
    </div>
  )
}

export default Profile
