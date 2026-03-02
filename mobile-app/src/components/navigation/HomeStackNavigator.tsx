import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import type { HomeStackParamList } from '../../types/navigation';
import { HomeScreen } from '../../screens';

const Stack = createNativeStackNavigator<HomeStackParamList>();

export const HomeStackNavigator: React.FC = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: true,
        animation: 'slide_from_right',
      }}
    >
      <Stack.Screen
        name="Home"
        component={HomeScreen}
        options={{ title: 'Home' }}
      />
    </Stack.Navigator>
  );
};
