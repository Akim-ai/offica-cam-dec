import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import {LoginPage} from "./Pages/LoginPage";
import {IndexPage} from "./Pages/IndexPage";

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
    <React.StrictMode>

        <Router>
            <Routes>
                <Route path="/" element={<IndexPage />} />
                <Route path="/login" element={<LoginPage/>}/>
            </Routes>
        </Router>
    </React.StrictMode>
);
