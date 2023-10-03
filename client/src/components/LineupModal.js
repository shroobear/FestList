import React, { useEffect } from "react";
import { Modal, Button, Row } from "react-bootstrap";

function LineupModal({ show, setShow, currentFestival, lineup, setLineup }) {
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  useEffect(() => {
    if (currentFestival) {
      fetch("/v1/festivals/" + currentFestival.id + "/lineup")
      .then ((res) => res.json())
      .then((data) => {
        console.log(data)
        setLineup(data);
        handleShow();
      });
    }
  }, [currentFestival])

  return (
    <main>
      <Modal
        style={{ "z-index": "9999" }}
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
          <Button variant="outline-primary">RSVP</Button>
          <Button variant="outline-primary">Generate Playlist</Button>
        </Row>
      </Modal>
    </main>
  );
}

export default LineupModal;
