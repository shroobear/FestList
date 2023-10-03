import React, { useState, useEffect } from "react";
import ArtistSearch from "./ArtistSearch";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button, Form, Card, Row, Container } from "react-bootstrap";
import LineupModal from "./LineupModal";

function Festivals() {
  const [festivals, setFestivals] = useState([]);
  const [lineup, setLineup] = useState([]);
  const [show, setShow] = useState(false);
  const [currentFestival, setCurrentFestival] = useState(null);
  const [filterType, setFilterType] = useState("");
  const [filterValue, setFilterValue] = useState("");
  const [filteredFestivals, setFilteredFestivals] = useState([])

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

  function getUniqueStates(festivals) {
    return [...new Set(festivals.map((festival) => festival.state))];
  }

  const uniqueStates = getUniqueStates(festivals);

  useEffect(() => {
    setFilteredFestivals(festivals);
  }, [festivals])

  function handleStateChange(e) {
    const selectedState = e.target.value;

    if (selectedState === "") {
        setFilteredFestivals(festivals);
    } else {
        const newStateFilteredFestivals = festivals.filter(festival => festival.state === selectedState);
        setFilteredFestivals(newStateFilteredFestivals)
    }
  }

  return (
    <main>
      <div>
        <Container>
          <h1 className="page-header">Festivals</h1>
          <Card bg="dark" text="light" className="g-2 mx-3 my-3" width="20rem">
            <Form.Group controlId="stateSelect">
              <Form.Label>Select State</Form.Label>
              <Form.Select
                size="sm"
                onChange={(e) => {handleStateChange(e)
                }}
              >
                <option value="">Choose...</option>
                {uniqueStates.map((state, index) => (
                  <option key={index} value={state}>
                    {state}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
          </Card>

          <Row xs={1} md={2} className="justify-content-center gap-3">
            {filteredFestivals.map((festival) => (
              <Card
                data-bs-theme="dark"
                key={festival.id}
                border="info"
                className="my-2 text-center"
                style={{ width: "21rem" }}
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
