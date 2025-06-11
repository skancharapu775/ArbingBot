# ArbingBot

A Flask and React app for detecting arbitrage opportunities in sports betting.

## Setup

### Backend (Flask)

1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Run the Flask server:
   ```bash
   python3 app.py
   ```
   The server will run on http://localhost:5001.

### Frontend (React + Vite)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Install Tailwind CSS and its dependencies:
   ```bash
   npm install -D tailwindcss postcss autoprefixer daisyui@latest
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```
   The app will open in your browser at http://localhost:5173.

## Usage

- The React app fetches arbitrage opportunities from the Flask backend and displays them in a grid layout.
- To view raw data, visit http://localhost:5001/api/listings in your browser.

## Troubleshooting

- If you encounter port conflicts, ensure no other services are using port 5001 (Flask) or 5173 (Vite).
- For CORS issues, ensure `flask-cors` is installed and enabled in your Flask app.
- If you see Node.js version warnings, consider updating to Node.js v18.18.0 or later.