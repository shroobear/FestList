import React, { useContext } from 'react';
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
