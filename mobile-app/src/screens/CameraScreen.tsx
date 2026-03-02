import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import type { ScannerStackScreenProps } from '../types/navigation';

type Props = ScannerStackScreenProps<'Camera'>;

export const CameraScreen: React.FC<Props> = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Scanner</Text>
      <Text style={styles.subtitle}>Freshness scanner coming soon</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
  },
});
