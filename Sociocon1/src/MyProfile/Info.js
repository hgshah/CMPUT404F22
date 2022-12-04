import axios from 'axios'
import React, { useEffect, useState } from 'react'
import "./Info.css"

import {InputText} from 'primereact/inputtext';
import { Button, Dialog } from '@mui/material';
import { flattenOptionGroups } from '@mui/base';
import { green } from '@mui/material/colors';


export default function Info() {

    const [profilePic, setProfilePic] = useState("")
    const [cropImage, setCropImage] = useState("")
    const [profile, setProfile] = useState([])
    const [profileView, setProfileView] = useState(false)
    const [src, setSrc] = useState(false)
    const authorid = localStorage.getItem("authorid")
    const token = localStorage.getItem("token")
    const preferredName = localStorage.getItem("preferredName") //check to see if this gets updated when changed
    const shownProfile = profile.map((item) => item.profileView)
    const ibase64 = localStorage.getItem("image")

    let pb64
    const changeProfilePic = async(e) => {
        const pic = e.target.files[0];
        const base64 = await toB64(pic)
        pb64 = await toB64(pic)
        // console.log(typeof pic.type.substring(0,5))
        //check if it is an image
        if (pic && pic.type.substring(0,5) === 'image') {
            localStorage.setItem("image", base64)
            setProfilePic(base64)
            // console.log(pic)
        }

        let formField = new FormData();
        formField.append("profileImage",ibase64)
        // console.log(base64)
        // const profile_picture = {profileImage:ibase64}
        // console.log(ibase64)
        // console.log(typeof ibase64)
        await axios.put('https://socioecon.herokuapp.com/authors/' + authorid + '/', formField,
        // await axios.put('http://127.0.0.1:8000//authors/' + authorid + '/', formField,
        {headers: {"Content-Type":"application/json", "Authorization": "Token " + token}}
        ).then((response) => {
            console.log(response)
        })
    }

    const toB64 = (pimage) => {
        return new Promise ((resolve,reject)=>{
            const filereader = new FileReader();
            filereader.readAsDataURL(pimage)
            filereader.onload = (()=>{
                resolve(filereader.result)
            })
            filereader.onerror = ((error)=>{
                reject(error)   
            })
        })
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

    useEffect(() => {
        async function getProfilePic() {
            await axios.get('https://socioecon.herokuapp.com/authors/self/', {
                headers: {"Content-Type":"application/json", "Authorization": "Token " + token},
            }).then((response) => {
                // console.log(response.data.profileImage)
            })
        }
        getProfilePic()
    }, [])

    return (

        <div className='info'>

            <div className='profileHeader'>
                <h1>Profile</h1>
                <br></br>
                <img className='profilePicture' src={profilePic} onClick={() => setCropImage(true)}/>
                <br></br>
                <InputText
                type="file"
                accept='/image/*'
                onChange={(e)=>{changeProfilePic(e)}}/>

                <h2 className='showUsername'>
                    <br></br>{preferredName}
                </h2>

            </div>

        </div>
    )
}

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