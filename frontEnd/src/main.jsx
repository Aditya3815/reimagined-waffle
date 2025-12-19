import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import "./index.css";
import App from "./App.jsx";

import { AuthProvider } from "./Context/AuthContext";
import { AppointmentProvider } from "./Context/AppointmentContext";
import { HealthGoalsProvider } from "./Context/HealthGoalsContext";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <AppointmentProvider>
          <HealthGoalsProvider>
            <App />
          </HealthGoalsProvider>
        </AppointmentProvider>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);
