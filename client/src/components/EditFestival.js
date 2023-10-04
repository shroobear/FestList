import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Container, Row, Card, Button } from "react-bootstrap";
import ArtistSearch from "./ArtistSearch";
import "bootstrap/dist/css/bootstrap.min.css";
import { checkIfArtistExists, createArtist, checkIfInLineup, addToLineup } from "./helpers";

function EditFestival() {
  const { festival_id } = useParams();
  const [currentFestival, setCurrentFestival] = useState(null);
  const [lineup, setLineup] = useState([])

  const fetchLineup = async () => {
    try {
        const res = await fetch(`/v1/festivals/${festival_id}/lineup`);
        const data = await res.json();
        setLineup(data);
    } catch (error) {
        console.error("Error fetching lineup:", error);
    }
  };

  async function festivalSetter() {
    const response = await fetch(`/v1/festivals/${festival_id}`);
    if (response.ok) {
        const data = await response.json();
        console.log("data from async: ", data)
        return setCurrentFestival(data)
    }
    throw new Error("Festival not found")
  }

  useEffect(() => {
    festivalSetter();
  }, [festival_id])

  useEffect(() => {
    fetchLineup();
  }, [festival_id])

  async function handleAddToFestival(artistData, festival_id) {
    try {
      let artist = await checkIfArtistExists(artistData.name);
      if (!artist) {
        console.log(artistData.id, artistData.name)
        artist = await createArtist(artistData);
      }
  
      const lineupEntry = await checkIfInLineup(festival_id, artist.id);
      if (!lineupEntry) {
        await addToLineup(festival_id, artist.id);
        alert("Artist successfully added to festival!");
      } else {
        alert("Artist is already in the lineup.");
      }
      fetchLineup();
    } catch (error) {
      console.error("Error:", error);
      alert("Failed operation.");
    }
  }

  return (
    <main>
      <Container>
        <h1 className="page-header">
          {currentFestival ? currentFestival.name : "Loading..."}
        </h1>
        <Row></Row>
        <Row>
          <Card>
            <h2>Lineup</h2>
            <ul>
                {lineup.map((artist) => (
                  <li key={artist.id}>{artist.name}</li>  
                ))}
            </ul>
            <Button variant="outline-danger" className="mb-2">Edit Lineup</Button>
          </Card>
        </Row>
      </Container>
      <Container className="mb-5">
        <ArtistSearch onAddToFestival={handleAddToFestival} festival_id={festival_id}/>
      </Container>
    </main>
  );
}

export default EditFestival;
