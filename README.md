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

### Frontend (React)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React app:
   ```bash
   npm start
   ```
   The app will open in your browser at http://localhost:3000.

## Usage

- The React app fetches arbitrage opportunities from the Flask backend and displays them in a grid layout.
- To view raw data, visit http://localhost:5001/listings in your browser.

## Troubleshooting

- If you encounter port conflicts, ensure no other services are using port 5001 (Flask) or 5000 (AirPlay on macOS).
- For CORS issues, ensure `flask-cors` is installed and enabled in your Flask app.