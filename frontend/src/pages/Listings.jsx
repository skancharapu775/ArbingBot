import React from 'react'
import { useState, useEffect } from 'react'
import AnimatedDots from '../components/AnimatedDots';
import LoadingScreen from '../components/LoadingScreen';
import ArbList from '../components/ArbList';
import ArbFilters from '../components/ArbsFilter';


const Listings = () => {
    const [loading, setLoading] = useState(true);
    const [arbs, setArbs] = useState([]);
    const [sportFilter, setSportFilter] = useState('');
    const [sortBy, setSportBy] = useState('');

    useEffect(() => {
        fetch('http://localhost:5001/api/listings')
          .then(res => res.json())
          .then(data => {
            setArbs(data);
            setLoading(false);
          })
          .catch(err => {
            console.error("Failed to load arbs", err);
            setLoading(false);
          });
      }, []);
    
    if (loading) return <LoadingScreen/>
  return (
    <div className='max-w-screen-xl mx-auto p-4 space-y-6 items-center'>
        <div className="bg-base-100 border border-base-300 rounded-lg shadow px-5 py-6 flex flex-wrap justify-between items-center gap-4">
            <div>
                <h2 className="text-lg font-bold">
                    🎯 {arbs.length} Arbitrage Opportunities
                </h2>
                <p className="text-sm text-base-content/60">Refreshed live</p>
            </div>
            <ArbFilters/>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 space-y-4">
            {arbs.length === 0 ? (
                <p>No arbitrage opportunities found.</p>
            ) : (
                <ArbList arbs={arbs}></ArbList>
                )
            }
        </div>
    </div>

  )
}
export default Listings