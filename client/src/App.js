import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import "./App.css"
import NavBar from "./components/NavBar"
import Dashboard from "./components/Dashboard"
import FavoriteArtists from "./components/ArtistSearch";
import MyFestivals from "./components/MyFestivals";
import Profile from "./components/Profile";
import Login from "./components/Login";
import { SignupForm } from "./components/Signup"
import AppProvider from "./context/AppProvider";

const APILink = "http://localhost:5555"


function App() {
  const [user, setUser] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('/v1/check_session')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                setUser(data);
            })
            .catch((error) => {
                setError(error.toString());
            });
    }, []);
    console.log(user)
  return (
      <AppProvider>
        <div>
          <NavBar />
          <Switch>
            <Route path = "/login">
              {user ? null : <Login />}
            </Route>
            <Route path = "/signup">
              {user ? null : <SignupForm />}
            </Route>
            <Route exact path="/">
              <Dashboard />
            </Route>
            <Route path="/favorites">
              <FavoriteArtists />
            </Route>
            <Route path="/festivals">
              <MyFestivals />
            </Route>
            <Route path="/profile">
              <Profile />
            </Route>
          </Switch>
        </div>
      </AppProvider>
  )
}

export default App;
