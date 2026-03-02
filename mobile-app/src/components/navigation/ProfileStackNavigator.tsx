import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import type { ProfileStackParamList } from '../../types/navigation';
import { TrustScoreScreen } from '../../screens';

const Stack = createNativeStackNavigator<ProfileStackParamList>();

export const ProfileStackNavigator: React.FC = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: true,
        animation: 'slide_from_right',
      }}
    >
      <Stack.Screen
        name="TrustScore"
        component={TrustScoreScreen}
        options={{ title: 'Profile' }}
      />
    </Stack.Navigator>
  );
};
