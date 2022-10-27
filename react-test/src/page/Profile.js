import React from 'react'
import { useNavigate, useParams } from "react-router-dom";
const Profile = () => {
  const navigate = useNavigate();

  return (
    <div>
      <h1> Profile </h1>
      <button onClick={() => navigate(-1)}>Go back</button> <br></br>
      <button onClick={() => navigate(1)}>Go Next</button> <br></br>
    </div>
  )
}
export default Profile
