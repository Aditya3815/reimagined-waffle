import { useContext, useEffect, useState } from "react";
import { HealthGoalsContext } from "../../Context/HealthGoalsContext";
import "./HealthGoals.css";

const HealthGoals = () => {
  const {
    healthTracking,
    medicalTests,
    preventiveCheckups,
    fetchHealthTracking,
    addHealthTracking,
    fetchMedicalTests,
    addMedicalTestRecord,
    fetchPreventiveCheckups,
    addPreventiveCheckupRecord,
  } = useContext(HealthGoalsContext);

  const [activeTab, setActiveTab] = useState('tracking');
  const [trackingForm, setTrackingForm] = useState({
    date: new Date().toISOString().split('T')[0],
    steps_taken: 0,
    hours_sleep: 0,
    water_intake: 0,
    calories_consumed: 0,
    exercise_minutes: 0,
    notes: '',
  });
  const [testForm, setTestForm] = useState({
    test_name: '',
    test_date: '',
    test_result: '',
    doctor_name: '',
    notes: '',
  });
  const [checkupForm, setCheckupForm] = useState({
    checkup_type: '',
    checkup_date: '',
    doctor_name: '',
    findings: '',
    next_checkup_date: '',
    notes: '',
  });

  useEffect(() => {
    fetchHealthTracking();
    fetchMedicalTests();
    fetchPreventiveCheckups();
  }, []);

  const handleTrackingSubmit = async (e) => {
    e.preventDefault();
    try {
      await addHealthTracking(trackingForm);
      alert('Health tracking added successfully!');
      setTrackingForm({
        date: new Date().toISOString().split('T')[0],
        steps_taken: 0,
        hours_sleep: 0,
        water_intake: 0,
        calories_consumed: 0,
        exercise_minutes: 0,
        notes: '',
      });
    } catch (error) {
      alert('Failed to add health tracking');
    }
  };

  const handleTestSubmit = async (e) => {
    e.preventDefault();
    try {
      await addMedicalTestRecord(testForm);
      alert('Medical test added successfully!');
      setTestForm({ test_name: '', test_date: '', test_result: '', doctor_name: '', notes: '' });
    } catch (error) {
      alert('Failed to add medical test');
    }
  };

  const handleCheckupSubmit = async (e) => {
    e.preventDefault();
    try {
      await addPreventiveCheckupRecord(checkupForm);
      alert('Preventive checkup added successfully!');
      setCheckupForm({ checkup_type: '', checkup_date: '', doctor_name: '', findings: '', next_checkup_date: '', notes: '' });
    } catch (error) {
      alert('Failed to add preventive checkup');
    }
  };

  return (
    <div className="health-goals-container">
      <h1>Health Goals Tracking</h1>

      <div className="tabs">
        <button className={activeTab === 'tracking' ? 'active' : ''} onClick={() => setActiveTab('tracking')}>
          Daily Tracking
        </button>
        <button className={activeTab === 'tests' ? 'active' : ''} onClick={() => setActiveTab('tests')}>
          Medical Tests
        </button>
        <button className={activeTab === 'checkups' ? 'active' : ''} onClick={() => setActiveTab('checkups')}>
          Preventive Checkups
        </button>
      </div>

      {activeTab === 'tracking' && (
        <div className="tab-content">
          <h2>Daily Health Tracking</h2>
          <form onSubmit={handleTrackingSubmit}>
            <input type="date" value={trackingForm.date} onChange={(e) => setTrackingForm({ ...trackingForm, date: e.target.value })} required />
            <input type="number" placeholder="Steps Taken" value={trackingForm.steps_taken} onChange={(e) => setTrackingForm({ ...trackingForm, steps_taken: parseInt(e.target.value) })} />
            <input type="number" step="0.1" placeholder="Hours of Sleep" value={trackingForm.hours_sleep} onChange={(e) => setTrackingForm({ ...trackingForm, hours_sleep: parseFloat(e.target.value) })} />
            <input type="number" step="0.1" placeholder="Water Intake (liters)" value={trackingForm.water_intake} onChange={(e) => setTrackingForm({ ...trackingForm, water_intake: parseFloat(e.target.value) })} />
            <input type="number" placeholder="Calories Consumed" value={trackingForm.calories_consumed} onChange={(e) => setTrackingForm({ ...trackingForm, calories_consumed: parseInt(e.target.value) })} />
            <input type="number" placeholder="Exercise Minutes" value={trackingForm.exercise_minutes} onChange={(e) => setTrackingForm({ ...trackingForm, exercise_minutes: parseInt(e.target.value) })} />
            <textarea placeholder="Notes" value={trackingForm.notes} onChange={(e) => setTrackingForm({ ...trackingForm, notes: e.target.value })} />
            <button type="submit">Add Tracking</button>
          </form>

          <h3>Recent Tracking ({healthTracking.length})</h3>
          {healthTracking.slice(0, 10).map((track, idx) => (
            <div key={idx} className="tracking-card">
              <p><strong>Date:</strong> {track.date}</p>
              <p>Steps: {track.steps_taken} | Sleep: {track.hours_sleep}h | Water: {track.water_intake}L</p>
              <p>Calories: {track.calories_consumed} | Exercise: {track.exercise_minutes}min</p>
              {track.notes && <p><em>{track.notes}</em></p>}
            </div>
          ))}
        </div>
      )}

      {activeTab === 'tests' && (
        <div className="tab-content">
          <h2>Medical Tests</h2>
          <form onSubmit={handleTestSubmit}>
            <input placeholder="Test Name" value={testForm.test_name} onChange={(e) => setTestForm({ ...testForm, test_name: e.target.value })} required />
            <input type="date" value={testForm.test_date} onChange={(e) => setTestForm({ ...testForm, test_date: e.target.value })} required />
            <textarea placeholder="Test Result" value={testForm.test_result} onChange={(e) => setTestForm({ ...testForm, test_result: e.target.value })} />
            <input placeholder="Doctor Name" value={testForm.doctor_name} onChange={(e) => setTestForm({ ...testForm, doctor_name: e.target.value })} />
            <textarea placeholder="Notes" value={testForm.notes} onChange={(e) => setTestForm({ ...testForm, notes: e.target.value })} />
            <button type="submit">Add Test</button>
          </form>

          <h3>Medical Tests ({medicalTests.length})</h3>
          {medicalTests.map((test, idx) => (
            <div key={idx} className="test-card">
              <h4>{test.test_name}</h4>
              <p><strong>Date:</strong> {test.test_date}</p>
              <p><strong>Result:</strong> {test.test_result}</p>
              <p><strong>Doctor:</strong> {test.doctor_name}</p>
              {test.notes && <p><em>{test.notes}</em></p>}
            </div>
          ))}
        </div>
      )}

      {activeTab === 'checkups' && (
        <div className="tab-content">
          <h2>Preventive Checkups</h2>
          <form onSubmit={handleCheckupSubmit}>
            <input placeholder="Checkup Type" value={checkupForm.checkup_type} onChange={(e) => setCheckupForm({ ...checkupForm, checkup_type: e.target.value })} required />
            <input type="date" value={checkupForm.checkup_date} onChange={(e) => setCheckupForm({ ...checkupForm, checkup_date: e.target.value })} required />
            <input placeholder="Doctor Name" value={checkupForm.doctor_name} onChange={(e) => setCheckupForm({ ...checkupForm, doctor_name: e.target.value })} />
            <textarea placeholder="Findings" value={checkupForm.findings} onChange={(e) => setCheckupForm({ ...checkupForm, findings: e.target.value })} />
            <input type="date" placeholder="Next Checkup Date" value={checkupForm.next_checkup_date} onChange={(e) => setCheckupForm({ ...checkupForm, next_checkup_date: e.target.value })} />
            <textarea placeholder="Notes" value={checkupForm.notes} onChange={(e) => setCheckupForm({ ...checkupForm, notes: e.target.value })} />
            <button type="submit">Add Checkup</button>
          </form>

          <h3>Preventive Checkups ({preventiveCheckups.length})</h3>
          {preventiveCheckups.map((checkup, idx) => (
            <div key={idx} className="checkup-card">
              <h4>{checkup.checkup_type}</h4>
              <p><strong>Date:</strong> {checkup.checkup_date}</p>
              <p><strong>Doctor:</strong> {checkup.doctor_name}</p>
              <p><strong>Findings:</strong> {checkup.findings}</p>
              {checkup.next_checkup_date && <p><strong>Next Checkup:</strong> {checkup.next_checkup_date}</p>}
              {checkup.notes && <p><em>{checkup.notes}</em></p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default HealthGoals;
