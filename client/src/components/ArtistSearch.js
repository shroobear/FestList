import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  Container,
  InputGroup,
  Form,
  Button,
  Row,
  Card,
} from "react-bootstrap";

function ArtistSearch() {
  const [searchInput, setSearchInput] = useState("");
  const [artists, setArtists] = useState([]);

  const handleSubmit = (event) => {
    event.preventDefault();

    const query = event.target.elements.artistSearch.value;
    setSearchInput(query);

    console.log("Submitting form with query:", query);
  };

  const fetchArtists = async (query) => {
    try {
      const response = await fetch(`/v1/search_artist`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setArtists(data);
    } catch (error) {
      console.error("There was an error fetching the artists", error);
    }
  };

  useEffect(() => {
    console.log(artists);
  }, [artists]);

  return (
    <div className="ArtistSearch">
      <Container>
        <Form onSubmit={handleSubmit}>
          <InputGroup className="mb-3" size="lg">
            <Form.Control
              name="artistSearch"
              placeholder="Search for Artist"
              aria-label="Artist-Search-Input"
              aria-describedby="basic-addon2"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
            />
            <Button
              variant="outline-secondary"
              id="search-button"
              onClick={() => {
                fetchArtists(searchInput);
              }}
            >
              Search
            </Button>
          </InputGroup>
        </Form>
      </Container>
      <Container>
        <Row className="mx-2 row row-cols-4">
          {artists.map((artist) => (
            <Card key={artist.id}>
              <Card.Img src={artist.images[0]?.url || "#"} />
              <Card.Body>
                <Card.Title>{artist.name}</Card.Title>
              </Card.Body>
            </Card>
          ))}
        </Row>
      </Container>
    </div>
  );
}

export default ArtistSearch;
