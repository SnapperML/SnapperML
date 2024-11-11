import React, { useState, useEffect } from "react";

const About: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    // Check if the dark-mode class is present on the body
    const darkModeEnabled = document.body.classList.contains("dark-mode");
    setIsDarkMode(darkModeEnabled);

    // Listen for class changes on the body to update state
    const observer = new MutationObserver(() => {
      const darkModeActive = document.body.classList.contains("dark-mode");
      setIsDarkMode(darkModeActive);
    });

    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ["class"],
    });

    // Clean up the observer on component unmount
    return () => observer.disconnect();
  }, []);

  return (
    <div className="container mt-4">
      <div className="about-box">
        <h2>About SnapperML</h2>
        <p>
          SnapperML is a comprehensive framework for experiment tracking and
          machine learning operationalization (MLOps). It is built using
          well-supported technologies like{" "}
          <a href="https://mlflow.org/">MLflow</a>,{" "}
          <a href="https://github.com/ray-project/ray/">Ray</a>, Docker, and
          more. SnapperML provides an opinionated workflow designed to
          facilitate both local and cloud-based experimentation.
        </p>

        <h3>Key Features</h3>
        <ul>
          <li>
            <strong>Automatic Tracking:</strong> Seamless integration with
            MLflow for parameter and metric tracking.
          </li>
          <li>
            <strong>Distributed Training:</strong> First-class support for
            distributed training and hyperparameter optimization using Optuna
            and Ray.
          </li>
          <li>
            <strong>CLI-Based Execution:</strong> Easily package and execute
            projects within containers using our intuitive Command Line
            Interface (CLI).
          </li>
          <li>
            <strong>Web Interface:</strong> A modern web interface developed
            with Vite, React, TypeScript, and Bootstrap for managing experiment
            configurations.
          </li>
        </ul>

        <h3>Project Goals</h3>
        <ul>
          <li>
            <strong>Enhance Maintainability:</strong> By addressing technical
            debt and improving the codebase, making it cleaner and more
            efficient.
          </li>
          <li>
            <strong>Improve Scalability:</strong> Ensure the system can handle
            large-scale experiments and concurrent requests smoothly.
          </li>
          <li>
            <strong>Provide a Robust Web UI:</strong> A user-friendly interface
            that simplifies the setup and execution of ML experiments.
          </li>
          <li>
            <strong>Ensure Reproducibility:</strong> Leverage MLOps principles
            to ensure experiments can be replicated easily.
          </li>
        </ul>

        <h3>Architecture Overview</h3>
        <p>
          SnapperML integrates several components to streamline machine learning
          workflows:
        </p>
        <ul>
          <li>
            <strong>CLI Framework:</strong> Facilitates command-based
            interactions and logging for experiment execution.
          </li>
          <li>
            <strong>Flask API:</strong> Manages requests from the frontend and
            interfaces with backend processes.
          </li>
          <li>
            <strong>Vite-Powered Web UI:</strong> An accessible and intuitive
            web application that handles experiment configurations and tracks
            real-time logs.
          </li>
          <li>
            <strong>Containerized Databases:</strong> Securely stores experiment
            results using containerized MLflow and Optuna databases.
          </li>
        </ul>

        <p>
          For more information, visit our{" "}
          <a href="https://snapperml.readthedocs.io/en/latest/">
            documentation
          </a>
          .
        </p>
        <img
          src={
            isDarkMode ? `public/logo_white_text.png` : `public/logo_text.png`
          }
          alt="SnapperML Banner"
          className="img-fluid center-image"
          style={{ width: "50%" }}
        />
      </div>
    </div>
  );
};

export default About;
