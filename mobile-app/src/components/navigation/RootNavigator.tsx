import React, { useEffect } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../../types/navigation';
import { AuthStackNavigator } from './AuthStackNavigator';
import { MainTabNavigator } from './MainTabNavigator';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import { autoLogin } from '../../store/slices/authSlice';

const Stack = createNativeStackNavigator<RootStackParamList>();

export const RootNavigator: React.FC = () => {
  const dispatch = useAppDispatch();
  const { isAuthenticated } = useAppSelector((state) => state.auth);

  // Attempt auto-login on mount
  useEffect(() => {
    dispatch(autoLogin());
  }, [dispatch]);

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {isAuthenticated ? (
        <Stack.Screen name="Main" component={MainTabNavigator} />
      ) : (
        <Stack.Screen name="Auth" component={AuthStackNavigator} />
      )}
    </Stack.Navigator>
  );
};
