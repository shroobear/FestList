import React, { useState, useEffect } from "react";
import * as yup from "yup";
import { useFormik } from "formik";
import { Modal, Form, Button } from "react-bootstrap";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { usStates } from "./helpers";

function FestivalDetailsEditModal({ show, handleClose, festival, refreshFestivals, onSave }) {
  const [startDate, setStartDate] = useState(new Date(festival.date));

  useEffect(() => {
    setStartDate(new Date(festival.date));
  }, [festival.date]);

  const formik = useFormik({
    initialValues: {
      name: festival.name,
      address: festival.address,
      city: festival.city,
      state: festival.state,
      date: new Date(festival.date).toISOString().split("T")[0],
      website: festival.website,
    },
    validationSchema: yup.object().shape({
      name: yup.string().required("Name Required"),
      address: yup.string().required("Address Required"),
      city: yup.string().required("City Required"),
      state: yup.string().required("State Required"),
      date: yup.date().required("Date Required"),
      website: yup.string(),
    }),
    onSubmit: (values) => {
      onSave(values);
    },
  });

  function handleSaveChanges() {
    fetch(`/v1/festivals/${festival.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formik.values, null, 2),
    })
      .then((res) => {
        if (res.ok) {
          alert("Changes saved successfully!");
          refreshFestivals();
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
        handleClose();
      });
  }

  return (
    <div>
      <Modal
        show={show}
        onHide={handleClose}
        className="d-flex align-items-center justify-content-center"
      >
        <Modal.Header closeButton>
          <Modal.Title>Edit Festival Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.Label htmlFor="name">Festival Name</Form.Label>
              <Form.Control
                type="text"
                id="name"
                name="name"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.name}
                placeholder="Enter Festival Name"
              />
              {formik.touched.name && formik.errors.name ? (
                <div className="text-danger">{formik.errors.name}</div>
              ) : null}
            </Form.Group>

            <Form.Group>
              <Form.Label htmlFor="address">Street Address</Form.Label>
              <Form.Control
                type="text"
                id="address"
                name="address"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.address}
                placeholder="Enter Street Address"
              />
              {formik.touched.address && formik.errors.address ? (
                <div className="text-danger">{formik.errors.address}</div>
              ) : null}
            </Form.Group>

            <Form.Group>
              <Form.Label htmlFor="city">City</Form.Label>
              <Form.Control
                type="text"
                id="city"
                name="city"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.city}
                placeholder="Enter City"
              />
              {formik.touched.city && formik.errors.city ? (
                <div className="text-danger">{formik.errors.city}</div>
              ) : null}
            </Form.Group>

            <Form.Group>
              <Form.Label htmlFor="state">State</Form.Label>
              <Form.Select
                id="state"
                name="state"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.state}
              >
                <option value="">Select A State</option>
                {usStates.map((state, index) => (
                  <option key={index} value={state}>
                    {state}
                  </option>
                ))}
              </Form.Select>
              {formik.touched.state && formik.errors.state ? (
                <div className="text-danger">{formik.errors.state}</div>
              ) : null}
            </Form.Group>

            <Form.Group>
              <Form.Label htmlFor="date">Date</Form.Label>
              <DatePicker
                type="date"
                id="date"
                name="date"
                selected={startDate}
                onChange={(date) => {
                  const formattedDate = date.toISOString().slice(0, 10);
                  setStartDate(date);
                  formik.setFieldValue("date", formattedDate);
                }}
                dateFormat="yyyy-MM-dd"
              />
            </Form.Group>

            <Form.Group>
              <Form.Label htmlFor="website">Website Link</Form.Label>
              <Form.Control
                type="text"
                id="website"
                name="website"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.website}
                placeholder="Enter Website URL"
              />
              {formik.touched.website && formik.errors.website ? (
                <div className="text-danger">{formik.errors.website}</div>
              ) : null}
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSaveChanges}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default FestivalDetailsEditModal;
