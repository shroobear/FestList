import React from "react";
import { Card, Form, Row } from "react-bootstrap";

function FestivalFilter({ onStateChange, uniqueStates }) {
  return (
    <Row className="justify-content-center">
      <Card bg="dark" text="light" className="gap-3" style={{width: "20rem"}}>
        <Form.Group controlId="stateSelect">
          <Form.Label className="mt-1">Select State</Form.Label>
          <Form.Select
            size="sm"
            className="mb-3"
            onChange={(e) => {
              onStateChange(e);
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
    </Row>
  );
}

export default FestivalFilter;
