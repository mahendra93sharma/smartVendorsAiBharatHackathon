// Pre-recorded audio sample transcriptions for demo mode
export const DEMO_AUDIO_SAMPLES = [
  {
    id: 'sample-1',
    language: 'hi-IN',
    text: 'Do kilo tamatar, pachas rupaye',
    translation: 'Two kilos tomatoes, fifty rupees',
    transcription: {
      text: 'Do kilo tamatar, pachas rupaye',
      confidence: 0.92,
      language: 'hi-IN',
    },
    transaction: {
      item_name: 'Tomatoes',
      quantity: 2.0,
      unit: 'kg',
      price_per_unit: 25.0,
      total_amount: 50.0,
    },
  },
  {
    id: 'sample-2',
    language: 'hi-IN',
    text: 'Teen kilo aloo, nabbey rupaye',
    translation: 'Three kilos potatoes, ninety rupees',
    transcription: {
      text: 'Teen kilo aloo, nabbey rupaye',
      confidence: 0.88,
      language: 'hi-IN',
    },
    transaction: {
      item_name: 'Potatoes',
      quantity: 3.0,
      unit: 'kg',
      price_per_unit: 30.0,
      total_amount: 90.0,
    },
  },
  {
    id: 'sample-3',
    language: 'en-IN',
    text: 'Five kilo onions, one hundred twenty rupees',
    translation: 'Five kilo onions, one hundred twenty rupees',
    transcription: {
      text: 'Five kilo onions, one hundred twenty rupees',
      confidence: 0.95,
      language: 'en-IN',
    },
    transaction: {
      item_name: 'Onions',
      quantity: 5.0,
      unit: 'kg',
      price_per_unit: 24.0,
      total_amount: 120.0,
    },
  },
  {
    id: 'sample-4',
    language: 'hi-IN',
    text: 'Ek kilo palak, bees rupaye',
    translation: 'One kilo spinach, twenty rupees',
    transcription: {
      text: 'Ek kilo palak, bees rupaye',
      confidence: 0.90,
      language: 'hi-IN',
    },
    transaction: {
      item_name: 'Spinach',
      quantity: 1.0,
      unit: 'kg',
      price_per_unit: 20.0,
      total_amount: 20.0,
    },
  },
]

// Demo market prices
export const DEMO_MARKET_PRICES = {
  tomatoes: [
    { mandi_name: 'Azadpur Mandi', price_per_kg: 22.0, distance_km: 5.2 },
    { mandi_name: 'Ghazipur Mandi', price_per_kg: 24.0, distance_km: 8.5 },
    { mandi_name: 'Okhla Mandi', price_per_kg: 23.5, distance_km: 6.8 },
  ],
  potatoes: [
    { mandi_name: 'Azadpur Mandi', price_per_kg: 28.0, distance_km: 5.2 },
    { mandi_name: 'Ghazipur Mandi', price_per_kg: 30.0, distance_km: 8.5 },
    { mandi_name: 'Okhla Mandi', price_per_kg: 29.0, distance_km: 6.8 },
  ],
  onions: [
    { mandi_name: 'Azadpur Mandi', price_per_kg: 22.0, distance_km: 5.2 },
    { mandi_name: 'Ghazipur Mandi', price_per_kg: 25.0, distance_km: 8.5 },
    { mandi_name: 'Okhla Mandi', price_per_kg: 23.0, distance_km: 6.8 },
  ],
  spinach: [
    { mandi_name: 'Azadpur Mandi', price_per_kg: 18.0, distance_km: 5.2 },
    { mandi_name: 'Ghazipur Mandi', price_per_kg: 20.0, distance_km: 8.5 },
    { mandi_name: 'Okhla Mandi', price_per_kg: 19.0, distance_km: 6.8 },
  ],
}

// Demo freshness results
export const DEMO_FRESHNESS_RESULTS = [
  {
    category: 'Fresh',
    confidence: 0.89,
    shelf_life_hours: 36,
    suggestions: ['Store in cool place', 'Sell within 2 days'],
  },
  {
    category: 'B-Grade',
    confidence: 0.76,
    shelf_life_hours: 12,
    suggestions: ['Make juice or pickle', 'List on marketplace', 'Discount pricing'],
  },
  {
    category: 'Waste',
    confidence: 0.92,
    shelf_life_hours: 0,
    suggestions: ['Compost', 'Animal feed', 'Dispose properly'],
  },
]

// Demo marketplace buyers
export const DEMO_BUYERS = [
  { name: 'Juice Corner', distance_km: 1.2, type: 'Juice Shop' },
  { name: 'Pickle Factory', distance_km: 3.5, type: 'Food Processing' },
  { name: 'Community Kitchen', distance_km: 2.1, type: 'NGO' },
]

// Get random demo audio sample
export function getRandomDemoAudio() {
  return DEMO_AUDIO_SAMPLES[Math.floor(Math.random() * DEMO_AUDIO_SAMPLES.length)]
}

// Get demo prices for item
export function getDemoPrices(item: string) {
  const normalizedItem = item.toLowerCase()
  return DEMO_MARKET_PRICES[normalizedItem as keyof typeof DEMO_MARKET_PRICES] || DEMO_MARKET_PRICES.tomatoes
}

// Get random freshness result
export function getRandomFreshnessResult() {
  return DEMO_FRESHNESS_RESULTS[Math.floor(Math.random() * DEMO_FRESHNESS_RESULTS.length)]
}
