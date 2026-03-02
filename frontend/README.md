# Smart Vendors Frontend

React-based voice-first mobile web application for street vendors.

## Features

- Voice transaction recording with Hindi/English support
- Market price intelligence from 3 mandis
- AI-powered freshness scanner
- B-Grade marketplace
- Trust Score tracking

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast builds
- **TailwindCSS** for styling
- **React Router** for navigation
- **Axios** for API calls

## Setup

### Install Dependencies

```bash
npm install
```

### Configure Environment

```bash
cp .env.example .env
```

The `.env` file is already configured with the production AWS API Gateway:

```env
VITE_API_BASE_URL=https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com
VITE_API_GATEWAY_URL=https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com
```

For local development, uncomment the localhost URLs in `.env`.

### Run Development Server

```bash
npm run dev
```

Open http://localhost:5173

## Build

### Production Build

```bash
npm run build
```

Output in `dist/` directory.

### Deploy to S3

```bash
npm run build
aws s3 sync dist/ s3://smart-vendors-static-dev/ --delete
```

## Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable components
│   ├── pages/            # Page components
│   ├── services/         # API services
│   ├── hooks/            # Custom hooks
│   ├── types/            # TypeScript types
│   ├── utils/            # Utility functions
│   ├── App.tsx           # Main app component
│   └── main.tsx          # Entry point
├── public/               # Static assets
└── index.html           # HTML template
```

## Development

### Code Formatting

```bash
npm run format
```

### Linting

```bash
npm run lint
npm run lint:fix
```

### Testing

```bash
npm test
```

## Environment Variables

```bash
VITE_API_BASE_URL=https://your-api-gateway.execute-api.ap-south-1.amazonaws.com
```

## Demo Credentials

- Username: `demo_vendor`
- Password: `hackathon2024`
