import React from "react";
import { Route, Routes } from "react-router-dom";
import NavBar from "./assets/components/NavBar";
import FileUpload from "./assets/components/FileUpload";
import About from "./assets/components/About";
import Contact from "./assets/components/Contact";
import "../styles.css";

const App: React.FC = () => {
  return (
    <div className="app-container">
      <NavBar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<FileUpload />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </main>
      <footer className="footer text-center mt-4">
        <p className="footer-text">
          Released under the MIT License.
          <br />
          Copyright 2024 SnapperML. All rights reserved.
        </p>
      </footer>
    </div>
  );
};

export default App;
