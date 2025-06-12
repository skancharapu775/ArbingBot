import React from 'react'
import { useState, useEffect } from 'react'
import AnimatedDots from '../components/AnimatedDots';
import LoadingScreen from '../components/LoadingScreen';
import ArbList from '../components/ArbList';
import ArbFilters from '../components/ArbsFilter';
import BookmakerFilter from '../components/BookmakerFilter';

const Listings = () => {
    const [loading, setLoading] = useState(true);
    const [arbs, setArbs] = useState([]);
    const [sportFilter, setSportFilter] = useState('all');
    const [sortBy, setSortBy] = useState('profit');

    useEffect(() => {
        fetch('http://localhost:5001/api/listings')
          .then(res => res.json())
          .then(data => {
            setArbs(data);
            setTimeout(() => {
                setLoading(false);
            }, 700);
          })
          .catch(err => {
            console.error("Failed to load arbs", err);
            setLoading(false);
          });
    }, []);

    const handleBookmakerApply = (bookmakers) => {
        console.log("Selected bookmakers:", bookmakers);
        setLoading(true);
        const url = `http://localhost:5001/api/bookmakerlistings?bookmakers=${bookmakers.join(',')}`;
        console.log("Fetching from URL:", url);
        fetch(url)
          .then(res => res.json())
          .then(data => {
            console.log("Received data:", data);
            setArbs(data);
            console.log("Updated arbs state:", data);
            setLoading(false);
          })
          .catch(err => {
            console.error("Failed to load filtered arbs", err);
            setLoading(false);
          });
    };

    // Filter and sort the arbs
    const filteredArbs = arbs
        .filter(arb => sportFilter === 'all' || arb.sport === sportFilter)
        .sort((a, b) => {
            if (sortBy === 'profit') {
                return b.profit_margin - a.profit_margin;
            } else {
                return a.event.localeCompare(b.event);
            }
        });
    
    if (loading) return <LoadingScreen/>
    return (
        <div className='max-w-screen-xl mx-auto p-4 space-y-6 items-center'>
            <div className="bg-base-100 border border-base-300 rounded-lg shadow px-5 py-6 flex flex-wrap justify-between items-center gap-4">
                <div>
                    <h2 className="text-lg font-bold">
                        🎯 {filteredArbs.length} Arbitrage Opportunities
                    </h2>
                    <p className="text-sm text-base-content/60">Refreshed every two minutes</p>
                </div>
                <ArbFilters 
                    sportFilter={sportFilter}
                    setSportFilter={setSportFilter}
                />
                <BookmakerFilter onApply={handleBookmakerApply} />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5 space-y-3">
                {filteredArbs.length === 0 ? (
                    <p>No arbitrage opportunities found.</p>
                ) : (
                    <ArbList arbs={filteredArbs}></ArbList>
                )}
            </div>
        </div>
    );
}

export default Listings