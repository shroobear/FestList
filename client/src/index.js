import React from "react";
import App from "./App";
import ReactDOM from "react-dom/client";
import "./index.css";
import { BrowserRouter as Router } from "react-router-dom/cjs/react-router-dom.min";
import AppProvider from "./context/AppProvider";

const container = document.getElementById("root");
const root = ReactDOM.createRoot(container);
root.render(
    <Router>
        <AppProvider>
            <App />
        </AppProvider>
    </Router>
);
