import React, { useEffect, useState, useContext } from 'react';
import { useHistory } from "react-router-dom";
import { useFormik } from 'formik';
import * as yup from 'yup';
import AppContext from '../context/AppContext';
import LoginForm from './LoginForm';



function Login() {

    const { setCurrentUser } = useContext(AppContext)

    function setUser(user) {
        console.log("user from callback:", user)
        setCurrentUser(user)    
    }

    return (
        <div>
            <LoginForm setUser={setUser}/>
        </div>
    )
}

export default Login;
