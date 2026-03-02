import React from 'react';
import { Platform } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/MaterialIcons';
import type { MainTabParamList } from '../../types/navigation';
import { HomeStackNavigator } from './HomeStackNavigator';
import { PricesStackNavigator } from './PricesStackNavigator';
import { ScannerStackNavigator } from './ScannerStackNavigator';
import { MarketplaceStackNavigator } from './MarketplaceStackNavigator';
import { ProfileStackNavigator } from './ProfileStackNavigator';

const Tab = createBottomTabNavigator<MainTabParamList>();

export const MainTabNavigator: React.FC = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: '#4CAF50',
        tabBarInactiveTintColor: '#757575',
        tabBarStyle: {
          height: Platform.OS === 'ios' ? 88 : 64,
          paddingBottom: Platform.OS === 'ios' ? 24 : 8,
          paddingTop: 8,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '600',
        },
      }}
    >
      <Tab.Screen
        name="HomeTab"
        component={HomeStackNavigator}
        options={{
          tabBarLabel: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Icon name="home" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="PricesTab"
        component={PricesStackNavigator}
        options={{
          tabBarLabel: 'Prices',
          tabBarIcon: ({ color, size }) => (
            <Icon name="trending-up" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="ScannerTab"
        component={ScannerStackNavigator}
        options={{
          tabBarLabel: 'Scanner',
          tabBarIcon: ({ color, size }) => (
            <Icon name="camera-alt" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="MarketplaceTab"
        component={MarketplaceStackNavigator}
        options={{
          tabBarLabel: 'Marketplace',
          tabBarIcon: ({ color, size }) => (
            <Icon name="store" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="ProfileTab"
        component={ProfileStackNavigator}
        options={{
          tabBarLabel: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <Icon name="person" size={size} color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
};
