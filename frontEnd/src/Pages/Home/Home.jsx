import "./Home.css";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <h1>Welcome to Hospital Management System</h1>
        <p>
          Book appointments, consult doctors, and manage patient records
          easily and securely.
        </p>

        <div className="hero-buttons">
          <Link to="/patient" className="btn primary">
            Patient Portal
          </Link>
          <Link to="/doctor" className="btn secondary">
            Doctor Portal
          </Link>
        </div>
      </section>

      {/* Services Section */}
      <section className="services">
        <h2>Our Services</h2>

        <div className="service-cards">
          <div className="card">
            <h3>🩺 Consultation</h3>
            <p>Online and in-person doctor consultations.</p>
          </div>

          <div className="card">
            <h3>📅 Appointments</h3>
            <p>Easy and quick appointment booking.</p>
          </div>

          <div className="card">
            <h3>📄 Medical Reports</h3>
            <p>Access medical records anytime.</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
