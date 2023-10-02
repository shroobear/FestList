import React, { useContext } from "react";
import { NavLink } from "react-router-dom";
import AppContext from "../context/AppContext";

function NavBar({ logout }) {
    const { currentUser } = useContext(AppContext);

    return (
        <div className="navBar-container">
            <div className="navbar-links">
                <ul>
                    <li>
                        <NavLink exact to="/">
                            Home
                        </NavLink>
                    </li>
                    <li>
                        <NavLink exact to="/festivals">
                            Festivals
                        </NavLink>
                    </li>
                    <li>
                        <NavLink exact to="/profile">
                            Profile
                        </NavLink>
                    </li>
                    <li>
                        {currentUser !== null ? (
                            <button onClick={logout}>
                                Logout
                            </button>
                        ) : (
                            <NavLink exact to="/login">
                                Login
                            </NavLink>
                        )}
                    </li>
                </ul>
            </div>
        </div>
    );
}

export default NavBar;
