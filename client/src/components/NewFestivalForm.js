import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import * as yup from "yup";
import { useFormik } from "formik";
import { Container, Form, Button, Alert } from "react-bootstrap";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

function NewFestivalForm() {
  const history = useHistory();
  const [startDate, setStartDate] = useState(new Date());
  const [showBanner, setShowBanner] = useState(false);

  const festivalFormSchema = yup.object().shape({
    name: yup.string().required("Must enter a festival name"),
    address: yup.string().required("Must enter an address"),
    city: yup.string().required("Must enter a city"),
    state: yup.string().required("Must select a state"),
    date: yup.date().required("Must enter a date"),
    website: yup.string(),
  });
  const formik = useFormik({
    initialValues: {
      name: "",
      address: "",
      city: "",
      state: "",
      date: new Date().toISOString(),
      website: "",
    },
    validationSchema: festivalFormSchema,
    onSubmit: (values) => {
      fetch("/v1/festivals", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values, null, 2),
      })
        .then((res) => {
          if (res.status !== 201) {
            return res.json().then((data) => {
              throw new Error(data.message);
            });
          }
          return res.json();
        })
        .then((data) => {
          console.log("Festival successfully posted: ", data);
          setShowBanner(true);
          setTimeout(() => {
            history.push(`/festivals/${data.id}/edit`);
            setShowBanner(false);
          }, 2000);
        })
        .catch((err) => {
          console.error("There was an error creating the festival:", err);
        });
    },
  });

  const usStates = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
  ];

  return (
    <main>
      <Container>
        <h1 className="page-header">Create New Festival</h1>
        {showBanner && (
          <Alert
            variant="success"
            onClose={() => setShowBanner(false)}
            dismissible
          >
            Festival successfully created!
          </Alert>
        )}
        <Form
          className="align-content-center justify-content-center"
          style={{ width: "50%", margin: "auto" }}
          onSubmit={formik.handleSubmit}
        >
          <Form.Group className="form">
            <Form.Label htmlFor="name">Festival Name</Form.Label>
            <Form.Control
              type="text"
              id="name"
              name="name"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur("")}
              value={formik.values.name}
              placeholder="Enter Festival Name"
            />
            {formik.touched.name && formik.errors.name ? (
              <p style={{ color: "red " }}>{formik.errors.name}</p>
            ) : null}
            <Form.Label htmlFor="address">Street Address</Form.Label>
            <Form.Control
              type="text"
              id="address"
              name="address"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur("")}
              value={formik.values.address}
              placeholder="Enter Street Address"
            />
            {formik.touched.address && formik.errors.address ? (
              <p style={{ color: "red " }}>{formik.errors.address}</p>
            ) : null}
            <Form.Label htmlFor="city">City</Form.Label>
            <Form.Control
              type="text"
              id="city"
              name="city"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur("")}
              value={formik.values.city}
              placeholder="Enter City"
            />
            {formik.touched.city && formik.errors.city ? (
              <p style={{ color: "red " }}>{formik.errors.city}</p>
            ) : null}
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
              <p style={{ color: "red " }}>{formik.errors.state}</p>
            ) : null}
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

            <Form.Label htmlFor="website">Website Link</Form.Label>
            <Form.Control
              type="text"
              id="website"
              name="website"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur("")}
              value={formik.values.website}
              placeholder="Enter Website URL"
            />
            {formik.touched.website && formik.errors.website ? (
              <p style={{ color: "red " }}>{formik.errors.website}</p>
            ) : null}
          </Form.Group>
          <Button
            size="lg"
            variant="primary"
            type="submit"
            style={{
              display: "block",
              marginLeft: "auto",
              marginRight: "auto",
              marginTop: "0.5rem",
            }}
          >
            Submit
          </Button>
        </Form>
      </Container>
    </main>
  );
}

export default NewFestivalForm;
