import React, { useContext } from "react";
import { Container, Row, Col, Button, Card } from "react-bootstrap";
import SpotifyLogin from "./SpotifyLogin";
import AppContext from "../context/AppContext";
import "bootstrap/dist/css/bootstrap.min.css";

function Dashboard() {
  const { currentUser } = useContext(AppContext);

  return (
    <main>
      <Container>
        <Row className="mt-5 mb-3">
          <Col className="text-center">
            <h1 className="page-header">Welcome to FestList!</h1>
            <p className="page-header">Discover and manage music festivals that fit your vibe.</p>
          </Col>
        </Row>

        {!currentUser && (
          <Row className="mb-3">
            <Col className="text-center">
              <Button variant="light" href="/login">
                Sign In
              </Button>
              <Button variant="outline-light" href="/signup" className="ml-2">
                Sign Up
              </Button>
            </Col>
          </Row>
        )}

        <Row className="mb-3 justify-content-center">
          <Card style={{ width: "25rem" }} className="align-content-center">
            <Col className="text-center">
              <h3>Features</h3>
              <ul>
                <li>Discover new festivals across the US.</li>
                <li>RSVP to your favorite events.</li>
                <li>Create and manage your own festivals.</li>
                <li>
                  Be sure to login with Spotify using the link below to generate
                  festival lineups!
                </li>
              </ul>
            </Col>
          </Card>
        </Row>
        <div className="d-flex justify-content-center align-items-center">
          {currentUser && <SpotifyLogin />}
        </div>
      </Container>
    </main>
  );
}

export default Dashboard;
