import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { useFormik } from "formik";
import * as yup from "yup";

export const SignupForm = () => {
  const [errorMessage, setErrorMessage] = useState("");

  const history = useHistory();

  const formSchema = yup.object().shape({
    email: yup.string().email("Invalid email").required("Must enter email"),
    firstName: yup.string().required("Must enter a name").max(15),
    lastName: yup.string().required("Must enter a name").max(15),
    username: yup.string().required("Must enter a username").max(20),
    password: yup.string().required("Must enter a password"),
    confirmPassword: yup
      .string()
      .label("confirm password")
      .required("Please re-type your password")
      .oneOf([yup.ref("password"), null], "Passwords must match"),
  });

  const formik = useFormik({
    initialValues: {
      email: "",
      username: "",
      firstName: "",
      lastName: "",
      password: "",
      confirmPassword: "",
    },
    validationSchema: formSchema,
    onSubmit: (values) => {
      fetch("v1/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values, null, 2),
      })
        .then((res) => {
          if (res.status === 409) {
            return res.json().then((data) => {
              throw new Error(data.message);
            });
          }
          return res.json();
        })
        .then((data) => {
          if (data && data.id) {
            history.push("/login");
          } else if (data && data.error) {
            console.error(data.error);
          }
        })
        .catch((err) => {
          console.error("There was an error with the registration:", err);
          setErrorMessage(err.message);
        });
    },
  });
  return (
    <main>
      <div className="form-container">
        <h1>Signup Form</h1>
        <form onSubmit={formik.handleSubmit} className="form">
          <label htmlFor="email">Email Address</label>
          <br />
          <input
            type="email"
            id="email"
            name="email"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur("email")}
            value={formik.values.email}
          />
          <p style={{ color: "red" }}>
            {formik.touched.email && formik.errors.email
              ? formik.errors.email
              : null}
          </p>
          <label htmlFor="firstName">First Name</label>
          <br />
          <input
            type="text"
            id="firstName"
            name="firstName"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur("firstName")}
            value={formik.values.firstName}
          />
          <p style={{ color: "red" }}>
            {formik.touched.firstName && formik.errors.firstName
              ? formik.errors.firstName
              : null}
          </p>
          <label htmlFor="lastName">Last Name</label>
          <br />
          <input
            type="text"
            id="lastName"
            name="lastName"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur("lastName")}
            value={formik.values.lastName}
          />
          <p style={{ color: "red" }}>
            {formik.touched.lastName && formik.errors.lastName
              ? formik.errors.lastName
              : null}
          </p>
          <label htmlFor="username">Username</label>
          <br />
          <input
            type="text"
            id="username"
            name="username"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur("username")}
            value={formik.values.username}
          />
          <p style={{ color: "red" }}>
            {formik.touched.username && formik.errors.username
              ? formik.errors.username
              : null}
          </p>
          <label htmlFor="password">Password</label>
          <br />
          <input
            type="password"
            id="password"
            name="password"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur("password")}
            value={formik.values.password}
          />
          <p style={{ color: "red" }}>
            {formik.touched.password && formik.errors.password
              ? formik.errors.password
              : null}
          </p>
          <label htmlFor="confirmPassword">Confirm Password</label>
          <br />
          <input
            type="password"
            id="confirmPassword"
            name="confirmPassword"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur("confirmPassword")}
            value={formik.values.confirmPassword}
          />
          <p style={{ color: "red" }}>
            {formik.touched.confirmPassword && formik.errors.confirmPassword
              ? formik.errors.confirmPassword
              : null}
          </p>
          {errorMessage && (
            <p style={{ color: "red" }} classname="error-message">
              {errorMessage}
            </p>
          )}
          <br />
          <button type="submit">Submit</button>
        </form>
        <p>
          Already registered? Click <a href="/login">here</a> to Login
        </p>
      </div>
    </main>
  );
};
