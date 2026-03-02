import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import type { AuthStackParamList } from '../../types/navigation';
import { LoginScreen } from '../../screens';

const Stack = createNativeStackNavigator<AuthStackParamList>();

export const AuthStackNavigator: React.FC = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
        animation: 'fade',
      }}
    >
      <Stack.Screen name="Login" component={LoginScreen} />
    </Stack.Navigator>
  );
};
