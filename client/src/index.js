import React from "react";
import App from "./App";
import ReactDOM from "react-dom/client";
import "./index.css";
import { createRoot } from "react-dom/client";
import { BrowserRouter as Router } from "react-router-dom/cjs/react-router-dom.min";

const container = document.getElementById("root");
const root = ReactDOM.createRoot(container);
root.render(
    <Router>
        <App />
    </Router>
);
