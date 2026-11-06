import React from 'react';

function sideLabel(team, details) {
    if (details.point === undefined || details.point === null) return team;
    const point = Number(details.point);
    const text = point > 0 ? `+${point}` : String(point);
    return `${team} ${text}`;
}

const ArbCard = ({ arb }) => {
    const [date, time] = arb.timestamp ? arb.timestamp.split(" ") : ["N/A", "N/A"];
    const market = Object.values(arb.outcomes || {})[0]?.market;
    const marketLabel = market === "spreads" ? "Spread" : market === "h2h" ? "Moneyline" : null;
    return (
      <div className="card bg-base-200 border border-base-300 shadow-md">
        <div className="card-body space-y-2">
          <div className="flex items-center justify-between">
            <h2 className="card-title text-lg font-semibold">
              {arb.event}{marketLabel ? ` · ${marketLabel}` : ""}
            </h2>
            <div className="badge badge-success text-xs">
              {arb.profit_margin}% Profit
            </div>
          </div>
  
          <div className="flex flex-col space-y-1">
            {Object.entries(arb.outcomes).map(([team, details]) => (
              <div key={team} className="flex items-center gap-2 text-sm">
                <span className="text-success">✅</span>
                <span>
                  Bet on <strong>{sideLabel(team, details)}</strong> at <span className="font-medium">{details.bookmaker}</span> (odds: {details.price})
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