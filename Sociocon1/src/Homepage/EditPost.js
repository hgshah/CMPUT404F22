import React from 'react'
import Post from './Post'

export default ({changeToFalse}) => {
  return (
    <div>
        <div onClick={() => changeToFalse()}></div>
      <input value = "Post Title" />
      <input value = "Post Body" />
      <button type="submit" />
    </div>
  )
}
