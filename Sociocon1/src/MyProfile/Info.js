import axios from 'axios'
import React, { useEffect, useState } from 'react'
import "./Info.css"
import { appBarClasses, Avatar, Button, TextField, Dialog, modalClasses} from '@mui/material';
// import 'antd/dist/antd.css';
import {InputText} from 'primereact/inputtext';
import { flattenOptionGroups } from '@mui/base';
import { green } from '@mui/material/colors';
import { AiFillEdit, AiFillCloseSquare, AiFillCheckSquare } from "react-icons/ai";
import defaultPP from "./defaultpp.png"
// import Popup from 'reactjs-popup';
// import 'reactjs-popup/dist/index.css';


export default function Info() {

    const [followerCount, setFollowerCount] = useState()
    const [postsCount, setPostsCount] = useState()
    const [realFriendCount, setRealFriendCount] = useState()
    const [profilePic, setProfilePic] = useState("")
    // const [cropImage, setCropImage] = useState("")
    const [profile, setProfile] = useState([])
    const [profileView, setProfileView] = useState(false)
    const [src, setSrc] = useState(false)
    const authorid = localStorage.getItem("authorid")
    const token = localStorage.getItem("token")
    // const displayName = localStorage.getItem("displayName") //check to see if this gets updated when changed
    const [displayedName, setDisplayName] = useState("")
    const [userGithub, setUserGithub] = useState("")
    const shownProfile = profile.map((item) => item.profileView)
    const ibase64 = localStorage.getItem("image")
    const [editModal, setEditModal] = useState(false)
    const [gitModal, setGitModal] = useState(false)

    let pb64
    const changeProfilePic = async(e) => {
        console.log("E: ", e)
        const pic = e.target.files[0];
        console.log("PIC: ", pic)
        const base64 = await toB64(pic)
        console.log("b64: ", base64)
        pb64 = await toB64(pic)
        console.log("pb64: ", pb64)
        // console.log(typeof pic.type.substring(0,5))
        //check if it is an image
        if (pic === null) {
            localStorage.removeItem("image")
            // console.log(pic)
        } else {
            localStorage.setItem("image", base64)
            // localStorage.setItem("image", pic)
        }
        setProfilePic(base64)

        let formField = new FormData();
        formField.append("profileImage",ibase64)
        // console.log(base64)
        // const profile_picture = {profileImage:ibase64}
        // console.log(ibase64)
        // console.log(typeof ibase64)

        //set new profile pic
        await axios.put('https://socioecon.herokuapp.com/authors/' + authorid + '/', {profileImage:base64},
                    {headers: {"Content-Type":"application/json", "Authorization": "Token " + token}}
        ).then((response) => {
            // console.log("RESPONSE: ", response)
        }).catch((error) => {
            // console.log("ERROR: ", error.response)
        })
        
    }

    const toB64 = (pimage) => {
        // console.log("PIMAGE: ",pimage)
        return new Promise ((resolve,reject)=>{
            const filereader = new FileReader();
            filereader.readAsDataURL(pimage)

            filereader.onload = ()=>{
                resolve(filereader.result)
            }
            filereader.onerror = ((error)=>{
                reject(error)   
            })
        })
    }

    const toggleModal = async() => {
        setEditModal(!editModal)
    }
    const toggleGitModal = async() => {
        setGitModal(!gitModal)
    }

    const handleSubmit = async() => {
        setEditModal(!editModal)
        // console.log(displayName)
        await axios.put('https://socioecon.herokuapp.com/authors/' + authorid + '/', {displayName:displayedName}, {
            headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
        }).then((response) => {
            console.log(response)
        }).catch((error) => {
            console.log("ERROR: ", error.response)
        })
    }

    const handleGitSubmit = async() => {
        setGitModal(!gitModal)
        await axios.put('https://socioecon.herokuapp.com/authors/' + authorid + '/', {github:userGithub}, {
            headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
        }).then((response) => {
            console.log(response)
        }).catch((error) => {
            console.log("ERROR: ", error.response)
        })
    }

    const handleDeletePP = async() => {
        await axios.put('https://socioecon.herokuapp.com/authors/' + authorid + '/', {profileImage:""},
        {headers: {"Content-Type":"application/json", "Authorization": "Token " + token}}
        ).then((response) => {
            // console.log("RESPONSE: ", response)
        }).catch((error) => {
            // console.log("ERROR: ", error.response)
        })
    }

    useEffect(() => {
        async function getProfilePic() {
            await axios.get('https://socioecon.herokuapp.com/authors/self/', {
                headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
            }).then((response) => {
                //if "" then put default pic
                
                setProfilePic(response.data.profileImage)
                // console.log(response.data.profileImage)
            })
            //show default profile pic
            if (profilePic === "") {
                await axios.put('https://socioecon.herokuapp.com/authors/' + authorid + '/', {profileImage:defaultPP},
                    {headers: {"Content-Type":"application/json", "Authorization": "Token " + token}}
                ).then((response) => {
                    // console.log("RESPONSE: ", response)
                }).catch((error) => {
                     // console.log("ERROR: ", error.response)
                })
            }
        }

        async function getFollowerCount() {
            await axios.get('https://socioecon.herokuapp.com/authors/' + authorid + '/followers/', 
            {headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
        }).then((response) => {
            setFollowerCount(response.data.items.length)
        })
        }

        async function getPostsCount() {
            await axios.get('https://socioecon.herokuapp.com/authors/' + authorid + '/posts/', {
                headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
            }).then((response) => {
                // console.log(response.data.items.length)
                setPostsCount(response.data.items.length)
            })
        }

        async function getRealFriendsCount() {
            await axios.get('https://socioecon.herokuapp.com/authors/' + authorid + '/real-friends/',
            {headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
        }).then((response) => {
            // console.log(response.data.items.length)
            setRealFriendCount(response.data.items.length)
        })
        }

        async function getDisplayName() {
            await axios.get('https://socioecon.herokuapp.com/authors/self/', {
                headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
            }).then((response) => {
                // console.log(response.data)
                setDisplayName(response.data.displayName)
            })
        }

        async function getGitgub() {
            await axios.get('https://socioecon.herokuapp.com/authors/self/', {
                headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
            }).then((response) => {
                // console.log(response.data.github)
                setUserGithub(response.data.github)
            })
        }
        
        getProfilePic()
        getFollowerCount()
        getPostsCount()
        getRealFriendsCount()
        getDisplayName()
        getGitgub()
    }, [])

    return (

        <div className='info'>

            <div className='profileHeader'>
                <h1>Profile</h1>
                <br></br>
                <img className='profilePicture' src={profilePic} alt=""/>
                <br></br>

                <InputText
                type="file"
                accept='/image/*'
                onChange={(e)=>{changeProfilePic(e)}}/>
                <Button className='delete_pp' onClick={() => handleDeletePP()}>
                    Delete Profile Pic
                </Button>

                <h2 className='showUsername'>
                    {displayedName} <span>
                    <AiFillEdit className='editUsername' onClick={() => toggleModal()}> </AiFillEdit></span>
                    <p className='user_github'>
                        {userGithub} <span>
                        <AiFillEdit className='editUsername' onClick={() => toggleGitModal()}> </AiFillEdit></span>
                    </p>
                </h2>
                {editModal && (
                <div className='edit_modal'>
                    <div className='overlay' onClick={() => toggleModal()}> </div>
                    <div className='edit_content'>
                        <h2>Edit Display Name</h2>
                        <AiFillCloseSquare className='close_modal' onClick={() => toggleModal()}> </AiFillCloseSquare>
                        <form>
                            <input
                            type="text"
                            placeholder='Username'
                            onChange={(e) => setDisplayName(e.target.value)}>
                            </input>
                            <AiFillCheckSquare className='submit' onClick={() => handleSubmit()}></AiFillCheckSquare>
                        </form>
                    </div>
                </div>
                )}

                {gitModal && (
                <div className='edit_modal'>
                    <div className='overlay' onClick={() => toggleGitModal()}> </div>
                    <div className='edit_content'>
                        <h2>Edit Github</h2>
                        <AiFillCloseSquare className='close_modal' onClick={() => toggleGitModal()}> </AiFillCloseSquare>
                        <form>
                            <input
                            type="text"
                            placeholder='Github URL'
                            onChange={(e) => setUserGithub(e.target.value)}>
                            </input>
                            <AiFillCheckSquare className='submit' onClick={() => handleGitSubmit()}></AiFillCheckSquare>
                        </form>
                    </div>
                </div>
                )}

            </div>
            <div className='socials'>
                <table className='display_socials'>
                    <tr>
                        <th>Followers</th>
                        <th>Real Friends</th>
                        <th>Posts</th>
                    </tr>
                    <tr>
                        <td>{followerCount}</td>
                        <td>{realFriendCount}</td>
                        <td>{postsCount}</td>
                    </tr>
                </table>
            </div>
            <div className='my_info'>

            </div>

        </div>
    )
}