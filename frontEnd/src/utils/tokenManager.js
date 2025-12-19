// Token Management Utilities

export const setTokens = (accessToken, refreshToken) => {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
};

export const getAccessToken = () => {
    return localStorage.getItem('access_token');
};

export const getRefreshToken = () => {
    return localStorage.getItem('refresh_token');
};

export const clearTokens = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
    localStorage.removeItem('user_role');
};

export const setUserData = (userData, role) => {
    localStorage.setItem('user_data', JSON.stringify(userData));
    localStorage.setItem('user_role', role);
};

export const getUserData = () => {
    const data = localStorage.getItem('user_data');
    return data ? JSON.parse(data) : null;
};

export const getUserRole = () => {
    return localStorage.getItem('user_role');
};

export const isAuthenticated = () => {
    return !!getAccessToken();
};
