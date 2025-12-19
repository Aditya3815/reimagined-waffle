import { createContext, useState, useEffect } from "react";
import { getDoctorAppointments, cancelAppointment as cancelDoctorAppointment } from "../services/doctorService";
import { getPatientAppointments, patientCancelAppointment } from "../services/patientService";
import { getUserData, getUserRole } from "../utils/tokenManager";

export const AppointmentContext = createContext();

export const AppointmentProvider = ({ children }) => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchAppointments = async () => {
    const userData = getUserData();
    const userRole = getUserRole();
    
    if (!userData || !userRole) return;

    setLoading(true);
    try {
      let response;
      if (userRole === 'doctor') {
        response = await getDoctorAppointments(userData.uid);
      } else if (userRole === 'patient') {
        response = await getPatientAppointments(userData.uid);
      }
      setAppointments(response.appointments || []);
    } catch (error) {
      console.error('Error fetching appointments:', error);
    } finally {
      setLoading(false);
    }
  };

  const deleteAppointment = async (bookingId) => {
    const userData = getUserData();
    const userRole = getUserRole();

    try {
      if (userRole === 'doctor') {
        await cancelDoctorAppointment(bookingId);
      } else if (userRole === 'patient') {
        await patientCancelAppointment(bookingId, userData.uid);
      }
      await fetchAppointments(); // Refresh list
    } catch (error) {
      console.error('Error canceling appointment:', error);
      throw error;
    }
  };

  return (
    <AppointmentContext.Provider
      value={{ appointments, loading, fetchAppointments, deleteAppointment }}
    >
      {children}
    </AppointmentContext.Provider>
  );
};

