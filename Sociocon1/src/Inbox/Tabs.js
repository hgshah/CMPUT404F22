import React from 'react'

export default function Tabs({id, currentTab, children}) {
  return (
    currentTab === id ? <div className="Tabs"> {children}</div> : null
  )
}
