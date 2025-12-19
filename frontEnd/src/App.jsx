import "./App.css";
import { Routes, Route } from "react-router-dom";

import NavBar from "./Component/Navbar/NavBar";
import Footer from "./Component/Footer/Footer";
import ProtectedRoute from "./Component/ProtectedRoute";

import Home from "./Pages/Home/Home";
import DoctorDash from "./Pages/DoctorDash/DoctorDash";
import PatientDash from "./Pages/PatientDash/PatientDash";
import HealthGoals from "./Pages/HealthGoals/HealthGoals";

import PatientLogin from "./Component/PatientLogin/PatientLogin";
import PatientRegister from "./Component/PatientRegister/PatientRegister";
import DoctorLogin from "./Component/DoctorLogin/DoctorLogin";
import DoctorRegister from "./Component/DoctorRegister/DoctorRegister";

function App() {
  return (
    <>
      <NavBar />

      <Routes>
        <Route path="/" element={<Home />} />
        
        {/* Protected Doctor Routes */}
        <Route 
          path="/doctor" 
          element={
            <ProtectedRoute requiredRole="doctor">
              <DoctorDash />
            </ProtectedRoute>
          } 
        />
        
        {/* Protected Patient Routes */}
        <Route 
          path="/patient" 
          element={
            <ProtectedRoute requiredRole="patient">
              <PatientDash />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/health-goals" 
          element={
            <ProtectedRoute requiredRole="patient">
              <HealthGoals />
            </ProtectedRoute>
          } 
        />
        
        {/* Public Routes */}
        <Route path="/doctor-login" element={<DoctorLogin />} />
        <Route path="/doctor-register" element={<DoctorRegister />} />
        <Route path="/patient-login" element={<PatientLogin />} />
        <Route path="/patient-register" element={<PatientRegister />} />
      </Routes>

      <Footer />
    </>
  );
}

export default App;
