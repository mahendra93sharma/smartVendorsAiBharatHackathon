import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Alert,
} from 'react-native';
import type { AuthStackScreenProps } from '../types/navigation';
import { Input } from '../components/common/Input';
import { Button } from '../components/common/Button';
import { Checkbox } from '../components/common/Checkbox';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { login } from '../store/slices/authSlice';

type Props = AuthStackScreenProps<'Login'>;

export const LoginScreen: React.FC<Props> = ({ navigation }) => {
  const dispatch = useAppDispatch();
  const { isAuthenticated } = useAppSelector((state) => state.auth);

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [isDemoMode, setIsDemoMode] = useState(true);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<{
    username?: string;
    password?: string;
  }>({});

  // Navigate to main app when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      // Navigation is handled by RootNavigator
    }
  }, [isAuthenticated]);

  const validateForm = (): boolean => {
    const newErrors: { username?: string; password?: string } = {};

    if (!username.trim()) {
      newErrors.username = 'Username is required';
    }

    if (!password.trim()) {
      newErrors.password = 'Password is required';
    } else if (password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleLogin = async () => {
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      const result = await dispatch(
        login({
          username: username.trim(),
          password,
          rememberMe,
          isDemoMode,
        })
      ).unwrap();

      // Success - navigation handled by RootNavigator
      console.log('Login successful:', result);
    } catch (error) {
      Alert.alert(
        'Login Failed',
        typeof error === 'string' ? error : 'An error occurred during login',
        [{ text: 'OK' }]
      );
    } finally {
      setLoading(false);
    }
  };

  const fillDemoCredentials = () => {
    setUsername('demo_vendor');
    setPassword('hackathon2024');
    setIsDemoMode(true);
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.content}>
          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.title}>Vendor App</Text>
            <Text style={styles.subtitle}>
              Sign in to manage your business
            </Text>
          </View>

          {/* Demo Mode Banner */}
          {isDemoMode && (
            <View style={styles.demoBanner}>
              <Text style={styles.demoBannerText}>🎭 Demo Mode</Text>
            </View>
          )}

          {/* Login Form */}
          <View style={styles.form}>
            <Input
              label="Username"
              value={username}
              onChangeText={(text) => {
                setUsername(text);
                setErrors({ ...errors, username: undefined });
              }}
              placeholder="Enter your username"
              autoCapitalize="none"
              autoCorrect={false}
              error={errors.username}
            />

            <Input
              label="Password"
              value={password}
              onChangeText={(text) => {
                setPassword(text);
                setErrors({ ...errors, password: undefined });
              }}
              placeholder="Enter your password"
              secureTextEntry
              error={errors.password}
            />

            <View style={styles.options}>
              <Checkbox
                label="Remember Me"
                checked={rememberMe}
                onToggle={() => setRememberMe(!rememberMe)}
              />

              <Checkbox
                label="Demo Mode"
                checked={isDemoMode}
                onToggle={() => setIsDemoMode(!isDemoMode)}
                style={styles.demoCheckbox}
              />
            </View>

            <Button
              title="Login"
              onPress={handleLogin}
              loading={loading}
              style={styles.loginButton}
            />

            {/* Demo Credentials Helper */}
            {isDemoMode && (
              <View style={styles.demoHelper}>
                <Text style={styles.demoHelperTitle}>Demo Credentials:</Text>
                <Text style={styles.demoHelperText}>
                  Username: demo_vendor
                </Text>
                <Text style={styles.demoHelperText}>
                  Password: hackathon2024
                </Text>
                <Button
                  title="Fill Demo Credentials"
                  onPress={fillDemoCredentials}
                  variant="outline"
                  style={styles.fillDemoButton}
                />
              </View>
            )}
          </View>

          {/* Footer */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>
              Vendor App v1.0.0
            </Text>
            <Text style={styles.footerText}>
              © 2024 All rights reserved
            </Text>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  scrollContent: {
    flexGrow: 1,
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 24,
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#007AFF',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  demoBanner: {
    backgroundColor: '#FFF3CD',
    borderRadius: 8,
    padding: 12,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: '#FFE69C',
  },
  demoBannerText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#856404',
    textAlign: 'center',
  },
  form: {
    backgroundColor: '#FFF',
    borderRadius: 12,
    padding: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  options: {
    marginBottom: 24,
  },
  demoCheckbox: {
    marginTop: 12,
  },
  loginButton: {
    marginBottom: 16,
  },
  demoHelper: {
    backgroundColor: '#F8F9FA',
    borderRadius: 8,
    padding: 16,
    marginTop: 8,
  },
  demoHelperTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  demoHelperText: {
    fontSize: 13,
    color: '#666',
    marginBottom: 4,
    fontFamily: Platform.OS === 'ios' ? 'Courier' : 'monospace',
  },
  fillDemoButton: {
    marginTop: 12,
  },
  footer: {
    marginTop: 32,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#999',
    marginBottom: 4,
  },
});
