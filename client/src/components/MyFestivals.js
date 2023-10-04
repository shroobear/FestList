import React, { useEffect, useState } from "react";
import { Container, Row, Col, Card, Button } from "react-bootstrap";
import FestivalDetailsEditModal from "./FestivalDetailsEditModal";

function MyFestivals() {
  const [rsvpedFestivals, setRsvpedFestivals] = useState([]);
  const [createdFestivals, setCreatedFestivals] = useState([]);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedFestivalForEdit, setSelectedFestivalForEdit] = useState(null);

  const user_id = sessionStorage.getItem("user_id");

  const fetchFestivalsData = () => {
    fetch(`/v1/users/${user_id}/rsvps`)
      .then((res) => res.json())
      .then((data) => setRsvpedFestivals(data))
      .catch((error) => console.error("Error fetching RSVPed festivals:", error));

    fetch(`/v1/users/${user_id}/created_festivals`)
      .then((res) => res.json())
      .then((data) => setCreatedFestivals(data))
      .catch((error) => console.error("Error fetching created festivals:", error));
  };

  useEffect(() => {
    fetchFestivalsData();
  }, [user_id]);

  const handleSaveChanges = (values) => {
    fetch(`/v1/festivals/${selectedFestivalForEdit.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(values),
    })
      .then((res) => {
        if (res.ok) {
          alert("Changes saved successfully!");
          return res.json();
        } else {
          return res.json().then((data) => {
            throw new Error(data.message || "Failed to save changes.");
          });
        }
      })
      .catch((error) => {
        console.error(error);
        alert("An error occurred: " + error.message);
      })
      .finally(() => {
        setShowEditModal(false);
      });
  };

  function handleDelete(festivalId) {
    fetch(`/v1/festivals/${festivalId}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message.includes("successfully")) {
          const updatedFestivals = createdFestivals.filter(
            (festival) => festival.id !== festivalId
          );
          setCreatedFestivals(updatedFestivals);
        } else {
          console.error("Error deleting festival:", data.message);
        }
      })
      .catch((error) => console.error("Error:", error));
  }

  function generateUrl(website) {
    return `http://${website}`;
  }

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
                  <Card.Text>
                    {festival.city}, {festival.state}
                  </Card.Text>
                  <Card.Text>
                    Date: {new Date(festival.date).toLocaleDateString()}
                  </Card.Text>
                  <Card.Link
                    href={generateUrl(festival.website)}
                    target="_blank"
                  >
                    Festival Website
                  </Card.Link>
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
                  <Card.Text>
                    {festival.city}, {festival.state}
                  </Card.Text>
                  <Card.Text>
                    Date: {new Date(festival.date).toLocaleDateString()}
                  </Card.Text>
                  <Card.Link
                    href={generateUrl(festival.website)}
                    target="_blank"
                  >
                    Festival Website
                  </Card.Link>
                </Card.Body>
                <Button
                  className="w-100 mb-2"
                  variant="light"
                  onClick={() => {
                    setSelectedFestivalForEdit(festival);
                    setShowEditModal(true);
                  }}
                >
                  🖊️ Edit Festival Details
                </Button>
                <Button
                  className="w-100 mb-2"
                  variant="primary"
                  onClick={() =>
                    (window.location.href = `/festivals/${festival.id}/edit`)
                  }
                >
                  📝 Edit Lineup
                </Button>
                <Button
                  className="w-100"
                  variant="danger"
                  onClick={() => handleDelete(festival.id)}
                >
                  🗑️ Delete Festival
                </Button>
              </Card>
            ))}
          </Col>
        </Row>
      </Container>

      {selectedFestivalForEdit && (
        <FestivalDetailsEditModal
          show={showEditModal}
          handleClose={() => setShowEditModal(false)}
          festival={selectedFestivalForEdit}
          onSave={handleSaveChanges}
          festId={selectedFestivalForEdit.id}
          refreshFestivals={fetchFestivalsData}
        />
      )}
    </main>
  );
}

export default MyFestivals;
