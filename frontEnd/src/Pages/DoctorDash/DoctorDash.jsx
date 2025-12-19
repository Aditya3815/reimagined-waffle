import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AppointmentContext } from "../../Context/AppointmentContext";
import { AuthContext } from "../../Context/AuthContext";
import { toggleDoctorStatus } from "../../services/doctorService";
import "./DoctorDash.css";

const DoctorDash = () => {
  const navigate = useNavigate();
  const { appointments, loading, fetchAppointments, deleteAppointment } = useContext(AppointmentContext);
  const { user, logout } = useContext(AuthContext);
  const [isOnline, setIsOnline] = useState(true);
  const [toggling, setToggling] = useState(false);

  useEffect(() => {
    if (user) {
      fetchAppointments();
      setIsOnline(user.is_active !== false);
    }
  }, [user]);

  const handleToggleStatus = async () => {
    if (!user) return;
    setToggling(true);
    try {
      const response = await toggleDoctorStatus(user.uid);
      setIsOnline(response.is_active);
    } catch (error) {
      console.error('Error toggling status:', error);
    } finally {
      setToggling(false);
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

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to logout?')) {
      logout();
      navigate('/doctor-login');
    }
  };

  return (
    <div className="doctor-dashboard">
      <div className="dashboard-header">
        <h1>Doctor Dashboard</h1>
        <div className="header-actions">
          <div className="status-toggle">
            <span>Status: {isOnline ? '🟢 Online' : '🔴 Offline'}</span>
            <button onClick={handleToggleStatus} disabled={toggling}>
              {toggling ? 'Updating...' : (isOnline ? 'Go Offline' : 'Go Online')}
            </button>
          </div>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      {loading ? (
        <p>Loading appointments...</p>
      ) : appointments.length === 0 ? (
        <p>No appointments</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Booking ID</th>
              <th>Patient Name</th>
              <th>Email</th>
              <th>Phone</th>
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
                <td>{a.booking_id?.substring(0, 8)}...</td>
                <td>{a.patient_name || a.patient_details?.name}</td>
                <td>{a.patient_email || a.patient_details?.email}</td>
                <td>{a.patient_phone || a.patient_details?.phone_number}</td>
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
  );
};

export default DoctorDash;
