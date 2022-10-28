// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0
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
