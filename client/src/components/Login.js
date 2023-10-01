import React, { useEffect, useState } from 'react';
import { useHistory } from "react-router-dom";
import { useFormik } from 'formik';
import * as yup from 'yup';
import APILink from "../App"



const LoginSchema = yup.object().shape({
    email: yup.string().email('Invalid email').required('Email is required'),
    password: yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
});

const Login = () => {

    const history = useHistory()

    const loginSchema = yup.object().shape({
        email: yup.string().email("Invalid email").required("Must enter email"),
        password: yup.string().required("Must enter a password"),
    })

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
                console.log(data)
                console.log(data.user_id, data.first_name, data.last_name, data.username)
                if (data && data.user_id) {
                    sessionStorage.setItem('userID', String(data.user_id));
                    sessionStorage.setItem('first_name', data.first_name);
                    sessionStorage.setItem('last_name', data.last_name);
                    sessionStorage.setItem('username', data.username);
                    sessionStorage.setItem('email', data.email);

                    history.push('/');
                }
                else if (data && data.error) {
                    console.error(data.error);
                }
            })
            .catch((err) => {
                console.log(err)
                console.error("There was an error with logging in:", err)
            });
        }
    });

    return (
        <div className='form-container'>
            <h1>Login</h1>
            <form onSubmit={formik.handleSubmit} className='form'>
                <label htmlFor="email">Email Address</label>
                <br />
                <input 
                type="email"
                id="email"
                name="email"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur('email')}
                value={formik.values.email}
                />
                <p style={{ color: "red" }}>
                    {formik.touched.email && formik.errors.email ? formik.errors.email : null}
                </p>
                <label htmlFor="password">Password</label>
                <br />
                <input 
                type="password"
                id="password"
                name="password"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur('password')}
                value={formik.values.password}
                />
                <p style={{ color: "red" }}>
                    {formik.touched.password && formik.errors.password ? formik.errors.password : null}
                </p>
                <button type='submit'>Login</button>
            </form>
            <p>New User? Sign up <a href="/signup">here!</a></p>
        </div>
    )
}

export default Login;
