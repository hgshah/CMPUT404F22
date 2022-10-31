// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0

import React from 'react'
import "./SidebarOption.css"
function SidebarOption({ active, text, Icon}) {
  return (
    <div className = {`sidebarOption ${active 
    && 'sidebarOption__active'}`}>
      <Icon />
      <h2>{text}</h2>
    </div>
  )
}

export default SidebarOption
