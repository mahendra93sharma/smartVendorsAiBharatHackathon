import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import type { PricesStackParamList } from '../../types/navigation';
import { PriceSearchScreen } from '../../screens';

const Stack = createNativeStackNavigator<PricesStackParamList>();

export const PricesStackNavigator: React.FC = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: true,
        animation: 'slide_from_right',
      }}
    >
      <Stack.Screen
        name="PriceSearch"
        component={PriceSearchScreen}
        options={{ title: 'Prices' }}
      />
    </Stack.Navigator>
  );
};
