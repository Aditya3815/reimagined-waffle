import { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../Context/AuthContext';

const ProtectedRoute = ({ children, requiredRole }) => {
  const { isLoggedIn, role } = useContext(AuthContext);

  if (!isLoggedIn) {
    // Not logged in, redirect to appropriate login page
    return <Navigate to={requiredRole === 'doctor' ? '/doctor-login' : '/patient-login'} replace />;
  }

  if (requiredRole && role !== requiredRole) {
    // Logged in but wrong role, redirect to their own dashboard
    return <Navigate to={role === 'doctor' ? '/doctor' : '/patient'} replace />;
  }

  return children;
};

export default ProtectedRoute;
