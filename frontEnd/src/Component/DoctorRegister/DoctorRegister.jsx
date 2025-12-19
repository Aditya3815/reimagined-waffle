import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../Context/AuthContext";
import { doctorRegister } from "../../services/doctorService";
import "./DoctorRegister.css";

const DoctorRegister = () => {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    password_confirm: "",
    first_name: "",
    last_name: "",
    phone_number: "",
    specialization: "",
    license_number: "",
    years_of_experience: 0,
    bio: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.password_confirm) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);
    try {
      const response = await doctorRegister(formData);
      login(response.doctor, response.tokens, 'doctor');
      navigate("/doctor");
    } catch (err) {
      setError(err.response?.data?.error || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const value = e.target.type === 'number' ? parseInt(e.target.value) : e.target.value;
    setFormData({ ...formData, [e.target.name]: value });
  };

  return (
    <div className="register-container">
      <h2>Doctor Registration</h2>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <input name="first_name" placeholder="First Name" value={formData.first_name} onChange={handleChange} required />
        <input name="last_name" placeholder="Last Name" value={formData.last_name} onChange={handleChange} required />
        <input name="email" type="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
        <input name="password" type="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
        <input name="password_confirm" type="password" placeholder="Confirm Password" value={formData.password_confirm} onChange={handleChange} required />
        <input name="phone_number" placeholder="Phone Number" value={formData.phone_number} onChange={handleChange} />
        <input name="specialization" placeholder="Specialization" value={formData.specialization} onChange={handleChange} />
        <input name="license_number" placeholder="License Number" value={formData.license_number} onChange={handleChange} />
        <input name="years_of_experience" type="number" placeholder="Years of Experience" value={formData.years_of_experience} onChange={handleChange} />
        <textarea name="bio" placeholder="Bio" value={formData.bio} onChange={handleChange} rows="3" />
        
        <button type="submit" disabled={loading}>
          {loading ? "Registering..." : "Register"}
        </button>
      </form>

      <p>
        Already have an account? <a href="/doctor-login">Login here</a>
      </p>
    </div>
  );
};

export default DoctorRegister;
