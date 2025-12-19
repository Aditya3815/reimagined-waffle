import api from './api';

// Daily Health Tracking
export const trackHealthGoals = async (patientUid, data) => {
    const response = await api.post(`/health-goals/track/${patientUid}/`, data);
    return response.data;
};

export const getHealthTracking = async (patientUid, date = null) => {
    const params = date ? { date } : {};
    const response = await api.get(`/health-goals/track/${patientUid}/`, { params });
    return response.data;
};

// Medical Tests
export const addMedicalTest = async (patientUid, data) => {
    const response = await api.post(`/health-goals/medical-test/${patientUid}/`, data);
    return response.data;
};

export const getMedicalTests = async (patientUid) => {
    const response = await api.get(`/health-goals/medical-tests/${patientUid}/`);
    return response.data;
};

// Preventive Checkups
export const addPreventiveCheckup = async (patientUid, data) => {
    const response = await api.post(`/health-goals/preventive-checkup/${patientUid}/`, data);
    return response.data;
};

export const getPreventiveCheckups = async (patientUid) => {
    const response = await api.get(`/health-goals/preventive-checkups/${patientUid}/`);
    return response.data;
};

// Doctor View Patient Health
export const getDoctorViewPatientHealth = async (patientUid) => {
    const response = await api.get(`/health-goals/doctor-view/${patientUid}/`);
    return response.data;
};
