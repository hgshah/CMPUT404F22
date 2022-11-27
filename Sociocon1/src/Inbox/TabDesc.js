import React from 'react'

export default function TabDesc({id, title, currentTab, setCurrentTab}) {
  
  function handleClick() {
    setCurrentTab(id)
  }

  return (
    <div>
      <li onClick={handleClick} className={currentTab === id ? "current" : ""}> 
        {title}
      </li>
    </div>
  )
}
