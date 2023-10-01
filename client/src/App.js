import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import "./App.css"
import NavBar from "./components/NavBar"
import Dashboard from "./components/Dashboard"
import FavoriteArtists from "./components/FavoriteArtists";
import MyFestivals from "./components/MyFestivals";
import Profile from "./components/Profile";

function App() {
  return (
      <div>
        <NavBar />
        <Switch>
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
  )
}

export default App;
