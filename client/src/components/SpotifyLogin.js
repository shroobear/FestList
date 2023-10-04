import React from "react";
import { Container, Card, Row, Button } from "react-bootstrap";
import { useLocation } from "react-router-dom";

function SpotifyLogin() {
  const APILink = "http://localhost:5555";
  const handleSpotifyLogin = () => {
    window.location.href = `${APILink}/v1/spotify_login`;
  };

  return (
    <main>
      <Container className="align-content-center">
        <Button  onClick={handleSpotifyLogin}>
          Link with Spotify
        </Button>
      </Container>
    </main>
  );
}

export default SpotifyLogin;
