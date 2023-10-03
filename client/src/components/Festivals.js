import React, { useState, useEffect } from "react";
import ArtistSearch from "./ArtistSearch";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  Button,
  Form,
  Card,
  Row,
  Container
} from "react-bootstrap";
import LineupModal from "./LineupModal";

function Festivals() {
  const [festivals, setFestivals] = useState([]);
  const [lineup, setLineup] = useState([]);
  const [show, setShow] = useState(false);
  const [currentFestival, setCurrentFestival] = useState(null);

  useEffect(() => {
    fetch("/v1/festivals")
      .then((res) => res.json())
      .then((data) => {
        setFestivals(data);
      });
  }, []);

  function handleCardClick(festival) {
    console.log(festival);
    setCurrentFestival(festival);
  }

  return (
    <main>
      <div>
          <Container>
            <h1 className="page-header">Festivals</h1>
            <Row xs={1} md={2} className="justify-content-center gap-3">
              {festivals.map((festival) => (
              <Card
                key={festival.id}
                border="info"
                className="my-2"
                style={{ width: "20rem" }}
              >
                <Card.Header>{festival.date}</Card.Header>
                <Card.Body>
                  <Card.Title>{festival.name}</Card.Title>
                  <Card.Text>
                    {festival.address}
                    <br />
                    {festival.city}
                    {", "}
                    {festival.state}
                    <br />
                    <Button onClick={() => handleCardClick(festival)}>
                      View Lineup
                    </Button>
                  </Card.Text>
                </Card.Body>
              </Card>
            ))}
            </Row>
          </Container>
      </div>
      <LineupModal
        show={show}
        setShow={setShow}
        currentFestival={currentFestival}
        lineup={lineup}
        setLineup={setLineup}
      />
      <ArtistSearch />
      <button>Create New Festival</button>
    </main>
  );
}

export default Festivals;
