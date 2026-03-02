import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import type { MarketplaceStackParamList } from '../../types/navigation';
import { ListingsScreen } from '../../screens';

const Stack = createNativeStackNavigator<MarketplaceStackParamList>();

export const MarketplaceStackNavigator: React.FC = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: true,
        animation: 'slide_from_right',
      }}
    >
      <Stack.Screen
        name="Listings"
        component={ListingsScreen}
        options={{ title: 'Marketplace' }}
      />
    </Stack.Navigator>
  );
};
