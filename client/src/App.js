import React, { useEffect, useContext } from "react";
import { Switch, Route, useHistory } from "react-router-dom";
import "./App.css";
import NavBar from "./components/NavBar";
import Dashboard from "./components/Dashboard";
import FavoriteArtists from "./components/ArtistSearch";
import Profile from "./components/Profile";
import Login from "./components/Login";
import { SignupForm } from "./components/Signup";
import { Redirect } from "react-router-dom/cjs/react-router-dom.min";
import AppContext from "./context/AppContext";
import Festivals from "./components/Festivals";
import NewFestivalForm from "./components/NewFestivalForm";
import EditFestival from "./components/EditFestival";
import MyFestivals from "./components/MyFestivals";



function App() {
  const history = useHistory();
  const { currentUser, setCurrentUser, setErrorMessage } = useContext(AppContext);
  function logout() {
    sessionStorage.clear();
    fetch("/v1/logout");
    setCurrentUser(null);
    history.push("/login");

    return null;
  }

  useEffect(() => {
    fetch("/v1/check_session")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setCurrentUser(data);
      })
      .catch((error) => {
        setErrorMessage(error.toString());
      });
  }, []);
  console.log("currentUser from useEffect", currentUser);
  return (
    <div>
      <NavBar logout={logout} />
      <Switch>
        <Route
          path="/login"
          render={() => (currentUser ? <Redirect to="/" /> : <Login />)}
        />
        <Route path="/signup">{currentUser ? null : <SignupForm />}</Route>
        <Route exact path="/">
          <Dashboard />
        </Route>
        <Route path="/favorites">
          <FavoriteArtists />
        </Route>
        <Route exact path="/festivals">
          <Festivals />
        </Route>
        <Route path="/myfestivals">
          <MyFestivals />
        </Route>
        <Route exact path="/festivals/new">
          <NewFestivalForm />
        </Route>
        <Route path="/festivals/:festival_id/edit">
          <EditFestival />
        </Route>
      </Switch>
    </div>
  );
}

export default App;
