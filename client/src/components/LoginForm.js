import React from "react";
import { useHistory } from "react-router-dom";
import { useFormik } from "formik";
import * as yup from "yup";
import AppContext from "../context/AppContext";

function LoginForm({ setUser }) {
  const history = useHistory();

  const loginSchema = yup.object().shape({
    email: yup.string().email("Invalid email").required("Must enter email"),
    password: yup.string().required("Must enter a password"),
  });
  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
    },
    validationSchema: loginSchema,
    onSubmit: (values) => {
      fetch("v1/festlist_login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values, null, 2),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data && data.user_id) {
            sessionStorage.setItem("user_id", String(data.user_id));
            sessionStorage.setItem("first_name", data.first_name);
            sessionStorage.setItem("last_name", data.last_name);
            sessionStorage.setItem("username", data.username);
            sessionStorage.setItem("email", data.email);
            const user = {
              user_id: data.user_id,
              first_name: data.first_name,
              last_name: data.last_name,
              username: data.username,
              email: data.email,
            };
            console.log("user from login", user);
            setUser(user);

            history.push("/");
          } else if (data && data.error) {
            console.error(data.error);
          }
        })
        .catch((err) => {
          console.log(err);
          console.error("There was an error with logging in:", err);
        });
    },
  });
  return (
    <main>
      <div className="form-container">
        <h1>Login</h1>
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
          <button type="submit">Login</button>
        </form>
        <p>
          New User? Sign up <a href="/signup">here!</a>
        </p>
      </div>
    </main>
  );
}

export default LoginForm;
