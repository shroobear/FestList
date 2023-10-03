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
import "../App.css";

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
          <InputGroup className="my-3" size="lg">
            <Form.Control
              name="artistSearch"
              placeholder="Search for Artist"
              aria-label="Artist-Search-Input"
              aria-describedby="basic-addon2"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
            />
            <Button
              variant="dark"
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
        <Row xs={1} md={2} className="g-2 justify-content-center gap-3">
          {artists.map((artist) => (
            <Card
              key={artist.id}
              style={{ width: "20rem", height: "30rem" }}
              bg="dark"
              className="my-auto text-center"
            >
              <Card.Img
                variant="top"
                style={{
                  maxHeight: "80%",
                  objectFit: "cover",
                  padding: "10px",
                }}
                src={
                  artist.images[0]?.url ||
                  "https://assets.simpleviewinc.com/simpleview/image/upload/c_fill,f_jpg,h_640,q_65,w_640/v1/clients/springfield/Concerts_Live_Music_d30b0459-d42e-424b-8ccf-31419a06694d.jpg"
                }
              />
              <Card.Body className="d-flex justify-content-center align-items-center">
                <div>
                  <Button
                    href={artist.external_urls["spotify"]}
                    target="_blank"
                    text="white"
                    variant="primary"
                    className="mb-3"
                  >
                    {artist.name}
                  </Button>{" "}
                  <br />
                  <Button variant="outline-light" size="sm">
                    Add to Festival
                  </Button>{" "}
                  <Button variant="outline-light" size="sm">
                    Add to Favorites
                  </Button>
                </div>
              </Card.Body>
            </Card>
          ))}
        </Row>
      </Container>
    </div>
  );
}

export default ArtistSearch;
