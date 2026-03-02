/**
 * Reusable Input Component
 */

import React, { useState } from 'react';
import {
  View,
  TextInput,
  Text,
  StyleSheet,
  ViewStyle,
  TextStyle,
  TouchableOpacity,
} from 'react-native';

interface InputProps {
  label: string;
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
  secureTextEntry?: boolean;
  error?: string;
  autoCapitalize?: 'none' | 'sentences' | 'words' | 'characters';
  autoCorrect?: boolean;
  keyboardType?: 'default' | 'email-address' | 'numeric' | 'phone-pad';
  style?: ViewStyle;
  inputStyle?: TextStyle;
  editable?: boolean;
}

export const Input: React.FC<InputProps> = ({
  label,
  value,
  onChangeText,
  placeholder,
  secureTextEntry = false,
  error,
  autoCapitalize = 'none',
  autoCorrect = false,
  keyboardType = 'default',
  style,
  inputStyle,
  editable = true,
}) => {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [isFocused, setIsFocused] = useState(false);

  const togglePasswordVisibility = () => {
    setIsPasswordVisible(!isPasswordVisible);
  };

  return (
    <View style={[styles.container, style]}>
      <Text style={styles.label}>{label}</Text>
      <View style={styles.inputContainer}>
        <TextInput
          style={[
            styles.input,
            isFocused && styles.inputFocused,
            error && styles.inputError,
            !editable && styles.inputDisabled,
            inputStyle,
          ]}
          value={value}
          onChangeText={onChangeText}
          placeholder={placeholder}
          placeholderTextColor="#999"
          secureTextEntry={secureTextEntry && !isPasswordVisible}
          autoCapitalize={autoCapitalize}
          autoCorrect={autoCorrect}
          keyboardType={keyboardType}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          editable={editable}
        />
        {secureTextEntry && (
          <TouchableOpacity
            style={styles.eyeIcon}
            onPress={togglePasswordVisibility}
            hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
          >
            <Text style={styles.eyeIconText}>
              {isPasswordVisible ? '👁️' : '👁️‍🗨️'}
            </Text>
          </TouchableOpacity>
        )}
      </View>
      {error && <Text style={styles.errorText}>{error}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  inputContainer: {
    position: 'relative',
  },
  input: {
    height: 48,
    borderWidth: 1,
    borderColor: '#DDD',
    borderRadius: 8,
    paddingHorizontal: 16,
    fontSize: 16,
    backgroundColor: '#FFF',
    color: '#333',
  },
  inputFocused: {
    borderColor: '#007AFF',
    borderWidth: 2,
  },
  inputError: {
    borderColor: '#FF3B30',
  },
  inputDisabled: {
    backgroundColor: '#F5F5F5',
    color: '#999',
  },
  eyeIcon: {
    position: 'absolute',
    right: 12,
    top: 12,
    padding: 4,
  },
  eyeIconText: {
    fontSize: 20,
  },
  errorText: {
    fontSize: 12,
    color: '#FF3B30',
    marginTop: 4,
  },
});
