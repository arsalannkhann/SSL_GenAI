# SHL Assessment Recommendation Frontend

A modern, responsive React frontend for the SHL Assessment Recommendation System. Built with Vite, React 18, TailwindCSS, and Lucide icons.

## Features

- 🎨 **Modern UI/UX** - Clean, gradient-based design with smooth animations
- 🔍 **Smart Search** - AI-powered assessment recommendations
- 📊 **Results Display** - Card-based layout with relevance scores
- ⚙️ **Configurable** - Adjustable API URL and top-K results
- 📝 **Test Dataset Support** - Load queries from test-set.csv
- 🌐 **Responsive** - Works on desktop, tablet, and mobile
- ♿ **Accessible** - ARIA labels and semantic HTML

## Tech Stack

- **Framework**: React 18 with Vite
- **Styling**: TailwindCSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **UI Components**: Custom components inspired by shadcn/ui

## Prerequisites

- Node.js 18+ and npm
- Backend API running (default: http://localhost:8000)

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. (Optional) Create a `.env` file:
```bash
cp .env.example .env
```

## Development

Start the development server:
```bash
npm run dev
```

The app will be available at http://localhost:3000

The dev server includes:
- Hot Module Replacement (HMR)
- API proxy to avoid CORS issues
- Fast refresh for instant feedback

## Build

Create a production build:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   │   ├── Alert.jsx
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   └── Input.jsx
│   │   ├── QueryInput.jsx   # Main query input form
│   │   └── ResultsDisplay.jsx # Results grid
│   ├── lib/
│   │   └── utils.js         # Utility functions
│   ├── App.jsx              # Main application
│   ├── main.jsx            # Entry point
│   └── index.css           # Global styles
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Configuration

### API URL
You can change the API URL in three ways:

1. **UI Settings** - Click the settings icon and enter the URL
2. **Environment Variable** - Set `VITE_API_URL` in `.env`
3. **Default** - Uses `http://localhost:8000` by default

### Top-K Results
Adjust the number of recommendations (1-20) using the slider in the settings panel.

### Test Dataset
Place your `test-set.csv` file in the `../data/` directory. The app will automatically load it for quick testing.

## API Integration

The frontend expects the backend to expose:

### POST /recommend
```json
{
  "query": "string",
  "top_k": 10
}
```

Response:
```json
{
  "query": "string",
  "recommendations": [
    {
      "assessment_name": "string",
      "assessment_url": "string",
      "relevance_score": 0.95,
      "test_type": "string",
      "duration": "string"
    }
  ],
  "total_results": 10
}
```

### GET /health
Health check endpoint.

## Deployment

### Using Vite Build

1. Build the production bundle:
```bash
npm run build
```

2. The `dist/` folder contains the static files ready for deployment to:
   - Netlify
   - Vercel
   - AWS S3 + CloudFront
   - Any static hosting service

### Using Docker

A Dockerfile is not included, but you can create one:

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)

## Troubleshooting

### API Connection Issues
- Ensure the backend is running
- Check CORS settings in the backend
- Verify the API URL in settings

### Build Errors
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`

## License

Same as parent project.
