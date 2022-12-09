import React from 'react'
import Sidebar from '../Sidebar'
import Info from './Info'
import News from '../News'
import Postbox from '../Homepage/Postbox'
import "./Profile.css"
import {Button} from '@mui/material';
//link :https://www.youtube.com/watch?v=ygV99J2Ehjs
// author: https://www.youtube.com/@edurise8679
//license: https://creativecommons.org/licenses/
function Profile() {
  // const defaultDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  // const [theme, setTheme] = useLocalStorage('theme', defaultDark ? 'dark' : 'light');

  // const switchTheme = () => {
  //   const newTheme = theme === 'light' ? 'dark' : 'light'
  //   setTheme(newTheme)

  // }
  return (
    // <div className='profile' data-theme={theme}>
    <div className='profile'>
      {/* <Button onClick={switchTheme}>
            Switch to {theme === 'light' ? 'Dark' : 'Light'} Theme
          </Button> */}
      <Sidebar/>
      <Info/>
      <News/>
    </div>
  )
}

export default Profile
