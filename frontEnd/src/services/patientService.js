import api from './api';

// Patient Authentication
export const patientRegister = async (data) => {
    const response = await api.post('/patients/register/', data);
    return response.data;
};

export const patientLogin = async (email, password) => {
    const response = await api.post('/patients/login/', { email, password });
    return response.data;
};

export const patientTokenRefresh = async (refreshToken) => {
    const response = await api.post('/patients/token/refresh/', { refresh_token: refreshToken });
    return response.data;
};

// Patient Profile
export const getPatientProfile = async (uid) => {
    const response = await api.get(`/patients/profile/${uid}/`);
    return response.data;
};

export const updatePatientProfile = async (uid, data) => {
    const response = await api.put(`/patients/profile/${uid}/`, data);
    return response.data;
};

// Patient Appointments
export const patientBookAppointment = async (doctorUid, appointmentData) => {
    const response = await api.post(`/patients/book-appointment/${doctorUid}/`, appointmentData);
    return response.data;
};

export const getPatientAppointments = async (patientUid) => {
    const response = await api.get(`/patients/appointments/${patientUid}/`);
    return response.data;
};

export const patientCancelAppointment = async (bookingId, patientUid) => {
    const response = await api.post(`/patients/cancel-appointment/${bookingId}/`, { patient_uid: patientUid });
    return response.data;
};
