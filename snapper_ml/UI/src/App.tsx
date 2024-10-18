import React from "react";
import { Route, Routes } from "react-router-dom";
import NavBar from "./assets/components/NavBar";
import FileUpload from "./assets/components/FileUpload";
import About from "./assets/components/About"; // Import new About component
import Contact from "./assets/components/Contact"; // Import new Contact component

const App: React.FC = () => {
  return (
    <div>
      <NavBar></NavBar>
      <Routes>
        <Route path="/" element={<FileUpload />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </div>
  );
};

export default App;
