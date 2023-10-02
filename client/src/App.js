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
  return (
      <AppProvider>
        <div>
          <NavBar />
          <Switch>
            <Route path = "/login">
              <Login />
            </Route>
            <Route path = "/signup">
              <SignupForm />
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
