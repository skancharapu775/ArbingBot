import React from 'react';

const ArbCard = ({ arb }) => {
    const [date, time] = arb.timestamp ? arb.timestamp.split(" ") : ["N/A", "N/A"];
    return (
      <div className="card bg-base-200 border border-base-300 shadow-md">
        <div className="card-body space-y-2">
          <div className="flex items-center justify-between">
            <h2 className="card-title text-lg font-semibold">{arb.event}</h2>
            <div className="badge badge-success text-xs">
              {arb.profit_margin}% Profit
            </div>
          </div>
  
          <div className="flex flex-col space-y-1">
            {Object.entries(arb.outcomes).map(([team, { bookmaker, price }]) => (
              <div key={team} className="flex items-center gap-2 text-sm">
                <span className="text-success">✅</span>
                <span>
                  Bet on <strong>{team}</strong> at <span className="font-medium">{bookmaker}</span> (odds: {price})
                </span>
              </div>
            ))}
            <div className="flex items-center gap-2 text-sm">
                <span className="text-success">🕔</span>
                <span><strong>Detected at {time}</strong> on {date}</span>
            </div>
          </div>
        </div>
      </div>
    );
  };
  
  export default ArbCard;