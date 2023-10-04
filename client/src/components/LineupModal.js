import React, { useEffect, useState } from "react";
import { Modal, Button, Row } from "react-bootstrap";

function LineupModal({ show, setShow, currentFestival, lineup, setLineup }) {
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [hasRSVPed, setHasRSVPed] = useState(false);

  useEffect(() => {
    const user_id = sessionStorage.getItem('user_id');
    console.log("current festival:", currentFestival);

    fetch(`/v1/users/${user_id}/rsvps`)
    .then(res => res.json())
    .then(data => {
        console.log("RSVPs data for user:", data);
        const rsvpForCurrentFestival = data.find(rsvp => String(rsvp.festival_id) === String(currentFestival.id));

        if(rsvpForCurrentFestival) {
            setHasRSVPed(true);
        } else {
            setHasRSVPed(false);
        }
    })
    .catch(error => {
      console.error('Error checking RSVP status:', error);
    });
  }, [currentFestival]);

  useEffect(() => {
    if (currentFestival) {
      fetch("/v1/festivals/" + currentFestival.id + "/lineup")
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setLineup(data);
        handleShow();
      });
    }
  }, [currentFestival]);

  function handleRSVPClick() {
    const rsvpData = {
      user_id: sessionStorage.getItem('user_id'),
      festival_id: currentFestival.id
    };

    fetch("/v1/rsvps", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(rsvpData),
    })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      setHasRSVPed(true);
    });
  }

  return (
    <main>
      <Modal
        style={{ "zIndex": "9999" }}
        centered={true}
        show={show}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        onHide={handleClose}
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            {currentFestival ? currentFestival.name : "Loading..."}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <h4>Lineup:</h4>
          {lineup &&
            lineup.map((artist) => {
              return <p key={artist.id}>{artist.name}</p>;
            })}
        </Modal.Body>
        <Row className="mx-4 my-3 justify-content-center gap-1">
          {hasRSVPed ? <Button variant="outline-primary" disabled>See you soon!</Button> : <Button variant="outline-primary" onClick={handleRSVPClick}>RSVP</Button>}
          <Button variant="outline-primary" disabled>Generate Playlist *coming soon*</Button>
        </Row>
      </Modal>
    </main>
  );
}

export default LineupModal;
