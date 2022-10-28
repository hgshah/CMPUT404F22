import React from 'react'
import Feed from './Feed'
import Sidebar from './Sidebar'
import News from './News'
function Home() {
  return (
    <div className='home'>
        <Sidebar />

        {/*feed */}
        < Feed />
        {/*widgets */}
        <News />
    </div>
  )
}

export default Home
