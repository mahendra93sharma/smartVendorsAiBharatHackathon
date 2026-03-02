import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { linking } from '../../types/navigation';
import { RootNavigator } from './RootNavigator';

export const AppNavigator: React.FC = () => {
  return (
    <NavigationContainer linking={linking}>
      <RootNavigator />
    </NavigationContainer>
  );
};
