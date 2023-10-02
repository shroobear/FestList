import React, {useState, useEffect } from "react";
import AppContext from "./AppContext"

const AppProvider = ({ children }) => {

    const [currentUser, setCurrentUser] = useState({
        username: "",
        email: "",
        first_name: "",
        last_name: "",
        userID: "",
    })

    const [errorMessage, setErrorMessage] = useState("")



    const appContextValues = {
        currentUser,
        setCurrentUser,
        errorMessage,
        setErrorMessage,
    };

    return (
        < AppContext.Provider value={appContextValues}>
            {children}
        </AppContext.Provider>
    );
};


export default AppProvider