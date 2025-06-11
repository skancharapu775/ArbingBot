import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [arbitrageOpps, setArbitrageOpps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArbitrageOpps = async () => {
      try {
        const response = await fetch('http://localhost:5001/listings');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setArbitrageOpps(data);
        setLoading(false);
      } catch (error) {
        setError('Error fetching data: ' + error.message);
        setLoading(false);
      }
    };

    fetchArbitrageOpps();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="App">
      <header className="App-header">
        <h1>Arbitrage Opportunities</h1>
        <div className="opportunities-list">
          {arbitrageOpps.map((opp, index) => (
            <div key={index} className="opportunity-card">
              <h2>{opp.event}</h2>
              <p>Profit Margin: {opp.profit_margin}%</p>
              <div className="bets">
                {Object.entries(opp.outcomes).map(([team, details]) => (
                  <div key={team} className="bet">
                    <p>Bet on {team} at {details.bookmaker}</p>
                    <p>Odds: {details.price}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;
