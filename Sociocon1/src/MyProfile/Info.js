import axios from 'axios'
import React, { useEffect, useState } from 'react'
import "./Info.css"
import { appBarClasses, Avatar, Button, TextField, Dialog} from '@mui/material';
// import 'antd/dist/antd.css';
import {InputText} from 'primereact/inputtext';
import { flattenOptionGroups } from '@mui/base';
import { green } from '@mui/material/colors';
import { AiFillEdit } from "react-icons/ai";
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';


export default function Info() {

    const [followerCount, setFollowerCount] = useState()
    const [postsCount, setPostsCount] = useState()
    const [realFriendCount, setRealFriendCount] = useState()
    const [profilePic, setProfilePic] = useState("")
    const [cropImage, setCropImage] = useState("")
    const [profile, setProfile] = useState([])
    const [profileView, setProfileView] = useState(false)
    const [src, setSrc] = useState(false)
    const authorid = localStorage.getItem("authorid")
    const token = localStorage.getItem("token")
    // const displayName = localStorage.getItem("displayName") //check to see if this gets updated when changed
    const [displayName, setDisplayName] = useState("")
    const shownProfile = profile.map((item) => item.profileView)
    const ibase64 = localStorage.getItem("image")

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
        await axios.put('https://socioecon.herokuapp.com/authors/' + authorid + '/', {profileImage:base64},
        // await axios.put('http://127.0.0.1:8000//authors/' + authorid + '/', formField,
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

    const editClicked = async() => {
        
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
                console.log(response.data)
                setDisplayName(response.data.displayName)
            })
        }
        
        getProfilePic()
        getFollowerCount()
        getPostsCount()
        getRealFriendsCount()
        getDisplayName()
    }, [])

    return (

        <div className='info'>

            <div className='profileHeader'>
                <h1>Profile</h1>
                <br></br>
                <img className='profilePicture' src={profilePic} alt="" onClick={() => setCropImage(true)}/>
                <br></br>

                <InputText
                type="file"
                accept='/image/*'
                onChange={(e)=>{changeProfilePic(e)}}/>

                <h2 className='showUsername'>
                    {displayName}
                    <AiFillEdit className='editUsername' onClick={() => editClicked()}>

                    </AiFillEdit>
                </h2>
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

        </div>
    )
}


// const onClose = () => {
//     setProfileView(null)
// }

// const onCrop = (view) => {
//     setProfileView(view)
// }

// const saveCroppedImage = () => {
//     setProfile([...profile, {profileView}])
//     setCropImage(false)
// }

{/* <div className='info'>

<div className='profileHeader'>
    <h1>Profile</h1>
    <img className='profilePicture' src={profilePic} onClick={() => setCropImage(true)}/>

    <label htmlFor='' className='showUsername'>{preferredName}</label>

    <Dialog 
    visible={cropImage} header={() => (
        <p htmlFor="" className='imageCrop'>
            Update
        </p>
    )}
    onHide={() => setCropImage(false)}
    >

        <div className='changeName'>
            <Avatar
            onCrop={onCrop}
            onClose={onClose}
            src={src}
            width={500}
            height={400}
            background-color={'green'}
            />

            <div className='changeAswell'>
                <div className='change3'>
                    <Button onClick={saveCroppedImage} label="Save" icon="pi pi-check"></Button>
                </div>
            </div>
        </div>
    </Dialog>
    
    <InputText 
    type="file"
    accept='/image/*'
    onChange={(e)=>{changeProfilePic(e)}}/>

</div>

</div> */}