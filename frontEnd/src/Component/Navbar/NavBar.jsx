import { Link, NavLink } from "react-router-dom";
import "./NavBar.css";

const NavBar = () => {
  return (
    <nav className="navbar">
      {/* Logo / Hospital Name */}
      <div className="navbar-logo">
        <Link to="/">🏥 Hospital Portal</Link>
      </div>

      {/* Navigation Links */}
      <ul className="navbar-links">
        <li>
          <NavLink to="/" end className="nav-link">
            Home
          </NavLink>
        </li>

        <li>
          <NavLink to="/doctor" className="nav-link">
            Doctor Dashboard
          </NavLink>
        </li>

        <li>
          <NavLink to="/patient" className="nav-link">
            Patient Dashboard
          </NavLink>
        </li>

        <li>
          <NavLink to="/doctor-login" className="nav-link">
            Doctor Login
          </NavLink>
        </li>

        <li>
          <NavLink to="/patient-login" className="nav-link">
            Patient Login
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default NavBar;
