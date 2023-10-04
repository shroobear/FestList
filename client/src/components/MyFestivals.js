import React, { useEffect, useState } from "react";
import { Container, Row, Col, Card } from "react-bootstrap";

function MyFestivals() {
  const [rsvpedFestivals, setRsvpedFestivals] = useState([]);
  const [createdFestivals, setCreatedFestivals] = useState([]);

  const user_id = sessionStorage.getItem("user_id");

  useEffect(() => {
    fetch(`/v1/users/${user_id}/rsvps`)
      .then((res) => res.json())
      .then((data) => {
        setRsvpedFestivals(data);
      })
      .catch((error) => {
        console.error("Error fetching RSVPed festivals:", error);
      });

    fetch(`/v1/users/${user_id}/createdFestivals`)
      .then((res) => res.json())
      .then((data) => {
        setCreatedFestivals(data);
      })
      .catch((error) => {
        console.error("Error fetching created festivals:", error);
      });
  }, [user_id]);

  return (
    <main>
      <Container>
        <Row className="mb-4">
          <Col>
            <h2>Festivals I'm Attending</h2>
            {rsvpedFestivals.map((festival) => (
              <Card key={festival.id} className="mb-3">
                <Card.Body>
                  <Card.Title>{festival.name}</Card.Title>
                  <Card.Text>{festival.address}</Card.Text>
                  <Card.Text>{festival.city}, {festival.state}</Card.Text>
                  <Card.Text>Date: {new Date(festival.date).toLocaleDateString()}</Card.Text>
                  <Card.Link href={festival.website} target="_blank">Festival Website</Card.Link>
                </Card.Body>
              </Card>
            ))}
          </Col>

          <Col>
            <h2>Festivals I Created</h2>
            {createdFestivals.map((festival) => (
              <Card key={festival.id} className="mb-3">
                <Card.Body>
                  <Card.Title>{festival.name}</Card.Title>
                  <Card.Text>{festival.address}</Card.Text>
                  <Card.Text>{festival.city}, {festival.state}</Card.Text>
                  <Card.Text>Date: {new Date(festival.date).toLocaleDateString()}</Card.Text>
                  <Card.Link href={festival.website} target="_blank">Festival Website</Card.Link>
                </Card.Body>
              </Card>
            ))}
          </Col>
        </Row>
      </Container>
    </main>
  );
}

export default MyFestivals;