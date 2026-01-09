# Setup Guide

## Quick Start

### 1. Install Dependencies

**Frontend:**
```bash
npm install
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create `backend/.env`:
```
OPENAI_API_KEY=your_key_here
DATABASE_URL=sqlite:///./crystal_trade.db
```

Create `.env` in root (optional):
```
VITE_API_URL=http://localhost:8000
```

### 3. Initialize Database

```bash
cd backend
python init_db.py
```

### 4. Run the Application

**Development mode (all services):**
```bash
npm run dev
```

This starts:
- React dev server: http://localhost:5173
- FastAPI backend: http://localhost:8000
- Electron app (auto-opens)

**Or run separately:**

Terminal 1 - Frontend:
```bash
npm run dev:react
```

Terminal 2 - Backend:
```bash
npm run dev:api
```

Terminal 3 - Electron:
```bash
npm run dev:electron
```

## Testing Without OpenAI API

If you don't have an OpenAI API key, the application will still work but AI features will return default/mock data. You can modify `backend/services/ai_analyzer.py` to use mock responses for testing.

## Troubleshooting

### Port Already in Use
- Change ports in `vite.config.ts` (frontend) or `backend/main.py` (backend)

### Database Errors
- Delete `backend/crystal_trade.db` and run `python init_db.py` again

### Electron Not Opening
- Make sure React dev server is running first
- Check that port 5173 is accessible

### Import Errors
- Make sure you're in the correct directory
- Verify all dependencies are installed
- Check Python path includes backend directory

