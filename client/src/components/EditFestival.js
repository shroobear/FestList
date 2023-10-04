import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Container, Row, Card, Button } from "react-bootstrap";
import ArtistSearch from "./ArtistSearch";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  checkIfArtistExists,
  createArtist,
  checkIfInLineup,
  addToLineup,
} from "./helpers";

function EditFestival() {
  const { festival_id } = useParams();
  const [currentFestival, setCurrentFestival] = useState(null);
  const [lineup, setLineup] = useState([]);
  const [isEditMode, setIsEditMode] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        const festivalResponse = await fetch(`/v1/festivals/${festival_id}`);
        const festivalData = await festivalResponse.json();
        setCurrentFestival(festivalData);

        const lineupResponse = await fetch(`/v1/festivals/${festival_id}/lineup`);
        const lineupData = await lineupResponse.json();
        setLineup(lineupData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }
    fetchData();
  }, [festival_id]);

  async function handleAddToFestival(artistData, festival_id) {
    try {
      let artist = await checkIfArtistExists(artistData.name);
      if (!artist) {
        artist = await createArtist(artistData);
      }

      const lineupEntry = await checkIfInLineup(festival_id, artist.id);
      if (!lineupEntry) {
        await addToLineup(festival_id, artist.id);
        alert("Artist successfully added to festival!");
        const newLineupResponse = await fetch(`/v1/festivals/${festival_id}/lineup`);
        const newLineupData = await newLineupResponse.json();
        setLineup(newLineupData);
      } else {
        alert("Artist is already in the lineup.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Failed operation.");
    }
  }

  async function handleDeleteFromLineup(festivalId, artistId) {
    try {
      const response = await fetch(`/v1/lineups/pair/${festivalId}/${artistId}`, {
        method: "DELETE",
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          alert("Artist successfully removed from festival!");
          const remainingArtists = lineup.filter((a) => a.id !== artistId);
          setLineup(remainingArtists);
        } else {
          alert(data.message || "Failed to remove artist.");
        }
      } else {
        throw new Error("Failed to delete artist from lineup.");
      }
    } catch (error) {
      console.error("Error deleting artist from lineup:", error);
      alert("Error deleting artist from lineup. Please try again.");
    }
  }

  return (
    <main>
      <Container style={{ width: "20rem" }} className="align-content-center">
        <h1 className="page-header">
          {currentFestival ? currentFestival.name : "Loading..."}
        </h1>
        <Row>
          <Card>
            <h2>Lineup</h2>
            <ul>
              {lineup.map((artist) => (
                <li key={artist.id}>
                  {artist.name}
                  {isEditMode && (
                    <Button
                      variant="light"
                      size="sm"
                      onClick={() => handleDeleteFromLineup(currentFestival.id, artist.id)}
                    >
                      ❌
                    </Button>
                  )}
                </li>
              ))}
            </ul>
            <Button
              variant="outline-danger"
              className="mb-2"
              onClick={() => setIsEditMode(!isEditMode)}
            >
              Edit Lineup
            </Button>
          </Card>
        </Row>
      </Container>
      <Container className="mb-5">
        <ArtistSearch onAddToFestival={handleAddToFestival} festival_id={festival_id} />
      </Container>
    </main>
  );
}

export default EditFestival;
