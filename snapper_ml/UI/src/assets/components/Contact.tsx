import React from "react";

const Contact: React.FC = () => {
  return (
    <div className="container mt-4">
      <h2 className="contact-title">Meet the Team Behind SnapperML</h2>
      <div className="contact-box">
        <div className="contact-content">
          <img
            src="https://media.licdn.com/dms/image/v2/C4D03AQEK509bM2PyqA/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1517067254242?e=1736985600&v=beta&t=j2xQM__pv4OKAQUEeK2ygK8tInigo5VWEovP1jG43MY"
            alt="Alberto Guillén Perales"
            className="contact-image"
          />
          <div className="contact-text">
            <h3>Alberto Guillén Perales</h3>
            <p>
              Alberto Guillén Perales is a professor and researcher in Computer
              Engineering, known for his extensive academic contributions and
              research collaborations. He began his career at the University of
              California (Irvine) and earned his Ph.D. in 2007, collaborating
              with Napier University and the University of Edinburgh. He has
              over 90 publications and has coordinated master’s programs in Data
              Science and Computer Engineering at the University of Granada. As
              the tutor of the SnapperML project, he has played a pivotal role
              in supervising and guiding its development.
            </p>
          </div>
        </div>
      </div>

      <div className="contact-box">
        <div className="contact-content">
          <img
            src="https://media.licdn.com/dms/image/v2/D4D03AQHdyRunR0h-3Q/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1718247503855?e=1736985600&v=beta&t=_-mCqIb85NWSRHTnGNTfwe_DXd615rO0O0jOBx-R7Ck"
            alt="Yeray López Ramírez"
            className="contact-image"
          />
          <div className="contact-text">
            <h3>Yeray López Ramírez</h3>
            <p>
              Yeray López Ramírez is an ABAP Junior Developer at Taghleef
              Industries and a soon-to-be Computer Engineering graduate from the
              University of Granada (2020-2024). He developed SnapperML as his
              final degree project, titled{" "}
              <q>
                Gestión de Deuda Técnica y Diseño de Interfaz en Framework MLOps
                (SnapperML)
              </q>
              . Yeray has a passion for software development, data science, and
              DevOps, and he brings experience in languages like Rust, C++, and
              JavaScript, alongside a strong dedication to continuous learning
              and community involvement.
            </p>
          </div>
        </div>
      </div>

      <div className="contact-box">
        <div className="contact-content">
          <img
            src="https://media.licdn.com/dms/image/v2/C4E03AQGfhEjbRNYqpQ/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1598525333260?e=1736985600&v=beta&t=Gu21Eg_6W42apP9p89G8GiFc4JR6HKhdStgxNHg2_tk"
            alt="Antonio Molner"
            className="contact-image"
          />
          <div className="contact-text">
            <h3>Antonio Molner Domenech</h3>
            <p>
              Antonio Molner Domenech is a Senior Machine Learning Engineer at
              Procore Technologies and the original creator of SnapperML. He
              earned his degree in Computer Engineering from the University of
              Granada, where he developed SnapperML as his final degree project,
              titled{" "}
              <q>
                Diseño e implementación de ml-experiment: framework para MLOps.
                Aplicación a rayos cósmicos de ultra alta energía
              </q>
              . His work laid the foundation for SnapperML, contributing
              significantly to the field of MLOps frameworks.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;
