// src/components/ArbFilters.jsx
import React from 'react';

const ArbFilters = ({ sportFilter, setSportFilter, sortBy, setSortBy }) => {
  return (
    <>
      <select
        className="select select-sm select-bordered"
        value={sportFilter}
        onChange={(e) => setSportFilter(e.target.value)}
      >
        <option value="all">All Sports</option>
        <option value="basketball_nba">Basketball</option>
        <option value="baseball_mlb">Baseball</option>
        <option value="americanfootball_nfl">Football</option>
      </select>

      <select
        className="select select-sm select-bordered"
        value={sortBy}
        onChange={(e) => setSortBy(e.target.value)}
      >
        <option value="profit">Sort by Profit</option>
        <option value="event">Sort by Event</option>
      </select>
    </>
  );
};

export default ArbFilters;
