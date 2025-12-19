import "./Footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        {/* Left Section */}
        <div className="footer-left">
          <h3>🏥 Hospital Portal</h3>
          <p>
            Providing quality healthcare services with trusted doctors and
            modern facilities.
          </p>
        </div>

        {/* Middle Section */}
        <div className="footer-center">
          <h4>Quick Links</h4>
          <ul>
            <li>Home</li>
            <li>Doctor</li>
            <li>Patient</li>
            <li>Contact</li>
          </ul>
        </div>

        {/* Right Section */}
        <div className="footer-right">
          <h4>Contact Us</h4>
          <p>Email: support@hospital.com</p>
          <p>Phone: +91 98765 43210</p>
        </div>
      </div>

      <div className="footer-bottom">
        © {new Date().getFullYear()} Hospital Management System. All rights
        reserved.
      </div>
    </footer>
  );
};

export default Footer;
