import { createContext, useState } from "react";
import {
  trackHealthGoals,
  getHealthTracking,
  addMedicalTest,
  getMedicalTests,
  addPreventiveCheckup,
  getPreventiveCheckups,
} from "../services/healthGoalsService";
import { getUserData } from "../utils/tokenManager";

export const HealthGoalsContext = createContext();

export const HealthGoalsProvider = ({ children }) => {
  const [healthTracking, setHealthTracking] = useState([]);
  const [medicalTests, setMedicalTests] = useState([]);
  const [preventiveCheckups, setPreventiveCheckups] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchHealthTracking = async () => {
    const userData = getUserData();
    if (!userData) return;

    setLoading(true);
    try {
      const response = await getHealthTracking(userData.uid);
      setHealthTracking(response.tracking || []);
    } catch (error) {
      console.error('Error fetching health tracking:', error);
    } finally {
      setLoading(false);
    }
  };

  const addHealthTracking = async (data) => {
    const userData = getUserData();
    if (!userData) return;

    try {
      await trackHealthGoals(userData.uid, data);
      await fetchHealthTracking();
    } catch (error) {
      console.error('Error adding health tracking:', error);
      throw error;
    }
  };

  const fetchMedicalTests = async () => {
    const userData = getUserData();
    if (!userData) return;

    setLoading(true);
    try {
      const response = await getMedicalTests(userData.uid);
      setMedicalTests(response.tests || []);
    } catch (error) {
      console.error('Error fetching medical tests:', error);
    } finally {
      setLoading(false);
    }
  };

  const addMedicalTestRecord = async (data) => {
    const userData = getUserData();
    if (!userData) return;

    try {
      await addMedicalTest(userData.uid, data);
      await fetchMedicalTests();
    } catch (error) {
      console.error('Error adding medical test:', error);
      throw error;
    }
  };

  const fetchPreventiveCheckups = async () => {
    const userData = getUserData();
    if (!userData) return;

    setLoading(true);
    try {
      const response = await getPreventiveCheckups(userData.uid);
      setPreventiveCheckups(response.checkups || []);
    } catch (error) {
      console.error('Error fetching preventive checkups:', error);
    } finally {
      setLoading(false);
    }
  };

  const addPreventiveCheckupRecord = async (data) => {
    const userData = getUserData();
    if (!userData) return;

    try {
      await addPreventiveCheckup(userData.uid, data);
      await fetchPreventiveCheckups();
    } catch (error) {
      console.error('Error adding preventive checkup:', error);
      throw error;
    }
  };

  return (
    <HealthGoalsContext.Provider
      value={{
        healthTracking,
        medicalTests,
        preventiveCheckups,
        loading,
        fetchHealthTracking,
        addHealthTracking,
        fetchMedicalTests,
        addMedicalTestRecord,
        fetchPreventiveCheckups,
        addPreventiveCheckupRecord,
      }}
    >
      {children}
    </HealthGoalsContext.Provider>
  );
};
