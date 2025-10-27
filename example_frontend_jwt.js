/**
 * Frontend JWT Authentication Example
 * 
 * This file demonstrates how to integrate JWT authentication in a frontend application.
 * Copy and adapt this code for your frontend framework (React, Vue, Angular, etc.)
 */

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Token Storage Management
 */
class TokenManager {
    static setAccessToken(token) {
        localStorage.setItem('access_token', token);
    }

    static getAccessToken() {
        return localStorage.getItem('access_token');
    }

    static setRefreshToken(token) {
        localStorage.setItem('refresh_token', token);
    }

    static getRefreshToken() {
        return localStorage.getItem('refresh_token');
    }

    static clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }

    static isAuthenticated() {
        return !!this.getAccessToken();
    }
}

/**
 * API Client with Automatic Token Management
 */
class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    /**
     * Make an authenticated request with automatic token refresh
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        // Add access token to headers if available
        const accessToken = TokenManager.getAccessToken();
        const headers = {
            'Content-Type': 'application/json',
            ...(options.headers || {})
        };

        if (accessToken) {
            headers['Authorization'] = `Bearer ${accessToken}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            // If token expired, try to refresh
            if (response.status === 401 && accessToken) {
                const newAccessToken = await this.refreshAccessToken();
                if (newAccessToken) {
                    // Retry request with new token
                    headers['Authorization'] = `Bearer ${newAccessToken}`;
                    const retryResponse = await fetch(url, {
                        ...options,
                        headers
                    });
                    return await this.handleResponse(retryResponse);
                } else {
                    // Refresh failed, user needs to login again
                    this.handleUnauthorized();
                    throw new Error('Authentication failed');
                }
            }

            return await this.handleResponse(response);
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }

    /**
     * Handle API response
     */
    async handleResponse(response) {
        const contentType = response.headers.get('content-type');

        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            if (response.ok) {
                return data;
            } else {
                throw new Error(data.detail || data.message || 'API request failed');
            }
        } else {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('API request failed');
            }
        }
    }

    /**
     * Refresh access token
     */
    async refreshAccessToken() {
        const refreshToken = TokenManager.getRefreshToken();
        if (!refreshToken) {
            return null;
        }

        try {
            const response = await fetch(`${this.baseURL}/auth/token/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                TokenManager.setAccessToken(data.access);
                return data.access;
            } else {
                // Refresh token expired
                TokenManager.clearTokens();
                return null;
            }
        } catch (error) {
            console.error('Token refresh error:', error);
            return null;
        }
    }

    /**
     * Handle unauthorized access
     */
    handleUnauthorized() {
        TokenManager.clearTokens();
        // Redirect to login page or show login modal
        // window.location.href = '/login';
        console.log('User logged out - token expired');
    }

    // Convenience methods
    async get(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'GET' });
    }

    async post(endpoint, data, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async put(endpoint, data, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async delete(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'DELETE' });
    }
}

// Initialize API client
const apiClient = new APIClient(API_BASE_URL);

/**
 * Authentication Service
 */
const AuthService = {
    /**
     * Register a new user
     */
    async register(userData) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (response.ok) {
                return { success: true, data };
            } else {
                return { success: false, errors: data };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    /**
     * Login user
     */
    async login(username, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Store tokens
                TokenManager.setAccessToken(data.access);
                TokenManager.setRefreshToken(data.refresh);

                return { success: true, data };
            } else {
                return { success: false, errors: data };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    /**
     * Logout user
     */
    async logout() {
        try {
            await apiClient.post('/auth/logout/');
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            TokenManager.clearTokens();
        }
    },

    /**
     * Get current user profile
     */
    async getProfile() {
        try {
            return await apiClient.get('/auth/profile/');
        } catch (error) {
            console.error('Get profile error:', error);
            throw error;
        }
    },

    /**
     * Update user profile
     */
    async updateProfile(userData) {
        try {
            return await apiClient.put('/auth/profile/update/', userData);
        } catch (error) {
            console.error('Update profile error:', error);
            throw error;
        }
    },

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        return TokenManager.isAuthenticated();
    }
};

/**
 * Weather Service (Example of using authenticated endpoints)
 */
const WeatherService = {
    /**
     * Get weather for a city
     */
    async getWeather(city) {
        try {
            return await apiClient.get(`/weather/?city=${city}`);
        } catch (error) {
            console.error('Get weather error:', error);
            throw error;
        }
    },

    /**
     * Get weather history
     */
    async getWeatherHistory() {
        try {
            return await apiClient.get('/weather/history/');
        } catch (error) {
            console.error('Get weather history error:', error);
            throw error;
        }
    }
};

/**
 * Example Usage
 */
async function example() {
    // Example: Register user
    const registerResult = await AuthService.register({
        username: 'testuser',
        email: 'test@example.com',
        first_name: 'Test',
        last_name: 'User',
        password: 'securepassword123',
        password_confirm: 'securepassword123'
    });

    if (registerResult.success) {
        console.log('Registration successful:', registerResult.data);
    } else {
        console.error('Registration failed:', registerResult.errors);
        return;
    }

    // Example: Login
    const loginResult = await AuthService.login('testuser', 'securepassword123');

    if (loginResult.success) {
        console.log('Login successful');

        // Example: Get profile
        try {
            const profile = await AuthService.getProfile();
            console.log('User profile:', profile);
        } catch (error) {
            console.error('Failed to get profile:', error);
        }

        // Example: Get weather
        try {
            const weather = await WeatherService.getWeather('London');
            console.log('Weather:', weather);
        } catch (error) {
            console.error('Failed to get weather:', error);
        }

        // Example: Logout
        await AuthService.logout();
        console.log('Logged out');
    } else {
        console.error('Login failed:', loginResult.errors);
    }
}

// Export for use in your application
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        TokenManager,
        APIClient,
        AuthService,
        WeatherService
    };
}

// Auto-run example if this is a standalone script
if (typeof window === 'undefined' && typeof module !== 'undefined') {
    // Running in Node.js environment
    example();
}


