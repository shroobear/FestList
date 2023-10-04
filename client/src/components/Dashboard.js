import React from "react";
import { Container, Row, Col, Button, Card } from "react-bootstrap";

function Dashboard() {
  const isLoggedIn = sessionStorage.getItem("user_id");
  
  return (
    <main>
      <Container>
        <Row className="mt-5 mb-3">
          <Col className="text-center">
            <h1>Welcome to FestFinder!</h1>
            <p>Discover and manage music festivals that fit your vibe.</p>
          </Col>
        </Row>

        {!isLoggedIn && (
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
          <Card style={{width: "25rem"}} className="align-content-center">
            <Col className="text-center">
              <h3>Features</h3>
              <ul>
                <li>Discover new festivals across the US.</li>
                <li>RSVP to your favorite events.</li>
                <li>Create and manage your own festivals.</li>
                <li>
                  *Coming Soon!* Integrate with Spotify to generate festival
                  playlists.
                </li>
              </ul>
            </Col>
          </Card>
        </Row>
      </Container>
    </main>
  );
}

export default Dashboard;
