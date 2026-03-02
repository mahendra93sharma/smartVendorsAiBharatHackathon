import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import type { ScannerStackParamList } from '../../types/navigation';
import { CameraScreen } from '../../screens';

const Stack = createNativeStackNavigator<ScannerStackParamList>();

export const ScannerStackNavigator: React.FC = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: true,
        animation: 'slide_from_right',
      }}
    >
      <Stack.Screen
        name="Camera"
        component={CameraScreen}
        options={{ title: 'Scanner' }}
      />
    </Stack.Navigator>
  );
};
