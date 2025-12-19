import { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AppointmentContext } from "../../Context/AppointmentContext";
import { AuthContext } from "../../Context/AuthContext";
import { getDoctorList, checkDoctorAvailability } from "../../services/doctorService";
import { patientBookAppointment } from "../../services/patientService";
import "./PatientDash.css";

const PatientDash = () => {
  const navigate = useNavigate();
  const { appointments, fetchAppointments, deleteAppointment } = useContext(AppointmentContext);
  const { isLoggedIn, user, logout } = useContext(AuthContext);
  const [showPopup, setShowPopup] = useState(false);
  const [doctors, setDoctors] = useState([]);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [form, setForm] = useState({
    doctor_uid: "",
    day: "",
    start_time: "",
    end_time: "",
    reason: "",
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      fetchAppointments();
      loadDoctors();
    }
  }, [user]);

  const loadDoctors = async () => {
    try {
      const response = await getDoctorList(true); // active only
      setDoctors(response.doctors || []);
    } catch (error) {
      console.error('Error loading doctors:', error);
    }
  };

  const handleDoctorChange = async (doctorUid) => {
    setForm({ ...form, doctor_uid: doctorUid, day: "", start_time: "", end_time: "" });
    setAvailableSlots([]);
  };

  const handleDayChange = async (day) => {
    setForm({ ...form, day, start_time: "", end_time: "" });
    if (!form.doctor_uid || !day) return;

    try {
      const response = await checkDoctorAvailability(form.doctor_uid, day);
      setAvailableSlots(response.time_slots || []);
    } catch (error) {
      console.error('Error checking availability:', error);
      setAvailableSlots([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user) return;

    setLoading(true);
    try {
      await patientBookAppointment(form.doctor_uid, {
        patient_uid: user.uid,
        day: form.day,
        start_time: form.start_time,
        end_time: form.end_time,
        reason: form.reason,
      });

      setForm({ doctor_uid: "", day: "", start_time: "", end_time: "", reason: "" });
      setShowPopup(false);
      await fetchAppointments();
      alert('Appointment booked successfully!');
    } catch (error) {
      console.error('Booking error:', error.response?.data);
      const errorMsg = error.response?.data?.error || error.response?.data?.message || 'Failed to book appointment';
      alert(errorMsg);
    } finally {
      setLoading(false);
    }
  };


  const handleCancelAppointment = async (bookingId) => {
    if (window.confirm('Are you sure you want to cancel this appointment?')) {
      try {
        await deleteAppointment(bookingId);
        alert('Appointment cancelled successfully');
      } catch (error) {
        alert('Failed to cancel appointment');
      }
    }
  };

  return (
    <div className="patient-layout">
      <div className="patient-dashboard">
        <h1>Patient Dashboard</h1>

        <button className="book-btn" onClick={() => setShowPopup(true)}>
          Book Appointment
        </button>

        {showPopup && (
          <div className="popup-overlay">
            <div className="popup">
              <h2>Book Appointment</h2>

              <form onSubmit={handleSubmit}>
                <select
                  value={form.doctor_uid}
                  onChange={(e) => handleDoctorChange(e.target.value)}
                  required
                >
                  <option value="">Select Doctor</option>
                  {doctors.map((doc) => (
                    <option key={doc.uid} value={doc.uid}>
                      Dr. {doc.first_name} {doc.last_name} - {doc.specialization}
                    </option>
                  ))}
                </select>

                {form.doctor_uid && (
                  <select
                    value={form.day}
                    onChange={(e) => handleDayChange(e.target.value)}
                    required
                  >
                    <option value="">Select Day</option>
                    <option value="monday">Monday</option>
                    <option value="tuesday">Tuesday</option>
                    <option value="wednesday">Wednesday</option>
                    <option value="thursday">Thursday</option>
                    <option value="friday">Friday</option>
                    <option value="saturday">Saturday</option>
                    <option value="sunday">Sunday</option>
                  </select>
                )}

                {form.day && availableSlots.length > 0 && (
                  <select
                    value={form.start_time && form.end_time ? `${form.start_time}-${form.end_time}` : ''}
                    onChange={(e) => {
                      if (e.target.value) {
                        const [start, end] = e.target.value.split('-');
                        setForm({ ...form, start_time: start, end_time: end });
                      }
                    }}
                    required
                  >
                    <option value="">Select Time Slot</option>
                    {availableSlots.filter(slot => slot.is_available).map((slot, idx) => (
                      <option key={idx} value={`${slot.start_time}-${slot.end_time}`}>
                        {slot.start_time} - {slot.end_time}
                      </option>
                    ))}
                  </select>
                )}

                <input
                  placeholder="Reason for visit (optional)"
                  value={form.reason}
                  onChange={(e) => setForm({ ...form, reason: e.target.value })}
                />

                <div className="popup-buttons">
                  <button type="submit" disabled={loading}>
                    {loading ? 'Booking...' : 'Confirm'}
                  </button>
                  <button
                    type="button"
                    className="cancel"
                    onClick={() => setShowPopup(false)}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {appointments.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Doctor</th>
                <th>Specialization</th>
                <th>Day</th>
                <th>Time</th>
                <th>Reason</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map((a) => (
                <tr key={a.booking_id}>
                  <td>{a.doctor_name}</td>
                  <td>{a.doctor_specialization}</td>
                  <td>{a.day}</td>
                  <td>{a.start_time} - {a.end_time}</td>
                  <td>{a.reason || 'N/A'}</td>
                  <td>{a.status}</td>
                  <td>
                    {a.status === 'confirmed' && (
                      <button onClick={() => handleCancelAppointment(a.booking_id)}>
                        Cancel
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="patient-sidebar">
        <h3>Menu</h3>
        <button>Dashboard</button>
        <button onClick={() => navigate('/health-goals')}>Health Goals</button>
        <button>Appointments</button>

        {!isLoggedIn ? (
          <button onClick={() => navigate("/patient-login")}>Login</button>
        ) : (
          <button className="logout" onClick={() => {
            if (window.confirm('Are you sure you want to logout?')) {
              logout();
              navigate('/patient-login');
            }
          }}>Logout</button>
        )}
      </div>
    </div>
  );
};

export default PatientDash;
