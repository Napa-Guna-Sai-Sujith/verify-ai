import React, { createContext, useContext, useState, useEffect } from 'react';
import { registerUserProfile, getUserProfile, updateUserProfile as apiUpdateUserProfile } from '../services/api';

const AuthContext = createContext({});

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState(null);

  useEffect(() => {
    const initSession = async () => {
      const savedUser = localStorage.getItem('verity_user');
      const savedProfile = localStorage.getItem('verity_profile');

      if (savedUser && savedProfile) {
        try {
          const parsedUser = JSON.parse(savedUser);
          const parsedProfile = JSON.parse(savedProfile);

          if (parsedUser?.email) {
            // Validate session against Neon DB before trusting localStorage
            try {
              const dbProfile = await getUserProfile(parsedUser.email);
              if (dbProfile) {
                // Valid: set session
                setUser(parsedUser);
                setProfile(dbProfile);
                localStorage.setItem('verity_profile', JSON.stringify(dbProfile));
              } else {
                // Profile removed from DB: clear invalid session
                _clearSession();
              }
            } catch (netErr) {
              // Network error: trust localStorage as fallback so user isn't logged out offline
              setUser(parsedUser);
              setProfile(parsedProfile);
            }
          } else {
            _clearSession();
          }
        } catch (e) {
          _clearSession();
        }
      }
      setLoading(false);
    };

    initSession();
  }, []);

  const _clearSession = () => {
    localStorage.removeItem('verity_user');
    localStorage.removeItem('verity_profile');
    setUser(null);
    setProfile(null);
  };

  const register = async ({ email, password, fullName, preferredLanguage }) => {
    setAuthError(null);
    const result = await registerUserProfile({ email, fullName, preferredLanguage });
    if (!result) {
      throw new Error('Failed to create account. Please try again.');
    }
    // Never auto-login on register — force explicit sign in
    _clearSession();
    return result;
  };

  const login = async ({ email, password }) => {
    setAuthError(null);
    // Check if user exists in Neon DB
    const dbProfile = await getUserProfile(email);

    if (!dbProfile) {
      throw new Error('No account found with that email. Please register first.');
    }

    const sessionUser = { id: dbProfile.id, email: dbProfile.email };
    localStorage.setItem('verity_user', JSON.stringify(sessionUser));
    localStorage.setItem('verity_profile', JSON.stringify(dbProfile));
    setUser(sessionUser);
    setProfile(dbProfile);
    return { user: sessionUser, profile: dbProfile };
  };

  const logout = () => {
    _clearSession();
  };

  const updateProfile = async ({ fullName, preferredLanguage }) => {
    if (!user?.email) return;
    const updated = await apiUpdateUserProfile({
      email: user.email,
      fullName,
      preferredLanguage,
    });
    if (updated) {
      setProfile(updated);
      localStorage.setItem('verity_profile', JSON.stringify(updated));
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        loading,
        authError,
        register,
        login,
        logout,
        updateProfile,
        isConfigured: true,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
