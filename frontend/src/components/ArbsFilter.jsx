// src/components/ArbFilters.jsx
import React from 'react';

const ArbFilters = ({ sportFilter, setSportFilter }) => {
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
    </>
  );
};

export default ArbFilters;
