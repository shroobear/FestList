import React from "react";
import { NavLink } from "react-router-dom";

function NavBar() {
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
                            My Festivals
                        </NavLink>
                    </li>
                    <li>
                        <NavLink exact to="/profile">
                            Profile
                        </NavLink>
                    </li>
                    <li>
                        <NavLink exact to="/favorites">
                            Favorite Artists
                        </NavLink>
                    </li>
                </ul>
            </div>
        </div>
    );
}

export default NavBar;