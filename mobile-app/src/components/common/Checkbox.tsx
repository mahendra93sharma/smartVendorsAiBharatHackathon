/**
 * Reusable Checkbox Component
 */

import React from 'react';
import {
  TouchableOpacity,
  View,
  Text,
  StyleSheet,
  ViewStyle,
} from 'react-native';

interface CheckboxProps {
  label: string;
  checked: boolean;
  onToggle: () => void;
  style?: ViewStyle;
}

export const Checkbox: React.FC<CheckboxProps> = ({
  label,
  checked,
  onToggle,
  style,
}) => {
  return (
    <TouchableOpacity
      style={[styles.container, style]}
      onPress={onToggle}
      activeOpacity={0.7}
      hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
    >
      <View style={[styles.checkbox, checked && styles.checkboxChecked]}>
        {checked && <Text style={styles.checkmark}>✓</Text>}
      </View>
      <Text style={styles.label}>{label}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  checkbox: {
    width: 24,
    height: 24,
    borderWidth: 2,
    borderColor: '#DDD',
    borderRadius: 4,
    marginRight: 8,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFF',
  },
  checkboxChecked: {
    backgroundColor: '#007AFF',
    borderColor: '#007AFF',
  },
  checkmark: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  label: {
    fontSize: 14,
    color: '#333',
  },
});
