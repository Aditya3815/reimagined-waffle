import api from './api';

// Doctor Authentication
export const doctorRegister = async (data) => {
    const response = await api.post('/doctors/register/', data);
    return response.data;
};

export const doctorLogin = async (email, password) => {
    const response = await api.post('/doctors/login/', { email, password });
    return response.data;
};

export const doctorTokenRefresh = async (refreshToken) => {
    const response = await api.post('/doctors/token/refresh/', { refresh_token: refreshToken });
    return response.data;
};

// Doctor Profile
export const getDoctorProfile = async (uid) => {
    const response = await api.get(`/doctors/profile/${uid}/`);
    return response.data;
};

export const updateDoctorProfile = async (uid, data) => {
    const response = await api.put(`/doctors/profile/${uid}/`, data);
    return response.data;
};

// Doctor Status
export const toggleDoctorStatus = async (uid) => {
    const response = await api.post(`/doctors/toggle-status/${uid}/`);
    return response.data;
};

// Doctor List
export const getDoctorList = async (activeOnly = false) => {
    const response = await api.get('/doctors/list/', {
        params: { active_only: activeOnly },
    });
    return response.data;
};

// Doctor Availability
export const getDoctorAvailability = async (uid) => {
    const response = await api.get(`/doctors/availability/${uid}/`);
    return response.data;
};

export const updateDoctorAvailability = async (uid, availability) => {
    const response = await api.put(`/doctors/availability/${uid}/`, { availability });
    return response.data;
};

export const checkDoctorAvailability = async (uid, day) => {
    const response = await api.get(`/doctors/check-availability/${uid}/`, {
        params: { day },
    });
    return response.data;
};

// Doctor Appointments
export const bookAppointment = async (doctorUid, appointmentData) => {
    const response = await api.post(`/doctors/book-appointment/${doctorUid}/`, appointmentData);
    return response.data;
};

export const cancelAppointment = async (bookingId) => {
    const response = await api.post(`/doctors/cancel-appointment/${bookingId}/`);
    return response.data;
};

export const getDoctorAppointments = async (doctorUid) => {
    const response = await api.get(`/doctors/appointments/${doctorUid}/`);
    return response.data;
};
