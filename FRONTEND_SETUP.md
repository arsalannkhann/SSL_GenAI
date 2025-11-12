# Frontend Setup Guide

## Quick Start

The Streamlit frontend has been replaced with a modern React application.

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will be available at http://localhost:3000

### 3. Start the Backend API

In a separate terminal:

```bash
# From project root
python -m uvicorn api.main:app --reload
```

The API will run at http://localhost:8000

### 4. Access the Application

Open your browser to http://localhost:3000 and start searching for SHL assessments!

## Features

✨ **Modern UI** - Gradient backgrounds, card layouts, smooth animations
🎯 **API Integration** - Full integration with FastAPI backend
⚙️ **Configurable** - Adjust API URL and result count
📝 **Test Support** - Load queries from test-set.csv
📱 **Responsive** - Works on all screen sizes

## Production Build

```bash
cd frontend
npm run build
npm run preview
```

## Deployment

The `frontend/dist` folder can be deployed to:
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any static hosting service

See `frontend/README.md` for detailed deployment instructions.

## Troubleshooting

**API not connecting?**
- Check that the backend is running on port 8000
- Verify CORS is enabled in the API (already configured)
- Update the API URL in the settings panel

**Build errors?**
- Delete `node_modules` and run `npm install` again
- Ensure Node.js version is 18 or higher

**Styles not loading?**
- The Tailwind warnings in the IDE are false positives
- Run `npm run dev` to see the app working correctly
