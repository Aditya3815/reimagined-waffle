import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../Context/AuthContext";
import { patientRegister } from "../../services/patientService";
import "./PatientRegister.css";

const PatientRegister = () => {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    password_confirm: "",
    first_name: "",
    last_name: "",
    phone_number: "",
    date_of_birth: "",
    address: "",
    emergency_contact: "",
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
      // Remove empty optional fields
      const submitData = { ...formData };
      if (!submitData.phone_number) delete submitData.phone_number;
      if (!submitData.date_of_birth) delete submitData.date_of_birth;
      if (!submitData.address) delete submitData.address;
      if (!submitData.emergency_contact) delete submitData.emergency_contact;

      const response = await patientRegister(submitData);
      login(response.patient, response.tokens, 'patient');
      navigate("/patient");
    } catch (err) {
      console.error('Registration error:', err.response?.data);
      // Show detailed error message
      if (err.response?.data) {
        const errorData = err.response.data;
        if (typeof errorData === 'object') {
          const errorMessages = Object.entries(errorData)
            .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
            .join('\n');
          setError(errorMessages || "Registration failed. Please try again.");
        } else {
          setError(errorData.error || errorData || "Registration failed. Please try again.");
        }
      } else {
        setError("Registration failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="register-container">
      <h2>Patient Registration</h2>

      {error && <div className="error-message" style={{whiteSpace: 'pre-line'}}>{error}</div>}

      <form onSubmit={handleSubmit}>
        <input name="first_name" placeholder="First Name" value={formData.first_name} onChange={handleChange} required />
        <input name="last_name" placeholder="Last Name" value={formData.last_name} onChange={handleChange} required />
        <input name="email" type="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
        <input name="password" type="password" placeholder="Password (min 8 characters)" value={formData.password} onChange={handleChange} required minLength={8} />
        <input name="password_confirm" type="password" placeholder="Confirm Password" value={formData.password_confirm} onChange={handleChange} required minLength={8} />
        <input name="phone_number" placeholder="Phone Number (optional)" value={formData.phone_number} onChange={handleChange} />
        <input name="date_of_birth" type="date" placeholder="Date of Birth (optional)" value={formData.date_of_birth} onChange={handleChange} />
        <input name="address" placeholder="Address (optional)" value={formData.address} onChange={handleChange} />
        <input name="emergency_contact" placeholder="Emergency Contact (optional)" value={formData.emergency_contact} onChange={handleChange} />
        
        <button type="submit" disabled={loading}>
          {loading ? "Registering..." : "Register"}
        </button>
      </form>

      <p>
        Already have an account? <a href="/patient-login">Login here</a>
      </p>
    </div>
  );
};

export default PatientRegister;
