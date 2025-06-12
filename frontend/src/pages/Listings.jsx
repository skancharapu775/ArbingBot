import React from 'react'
import { useState, useEffect } from 'react'
import AnimatedDots from '../components/AnimatedDots';
import LoadingScreen from '../components/LoadingScreen';
import ArbList from '../components/ArbList';
import ArbFilters from '../components/ArbsFilter';
import BookmakerFilter from '../components/BookmakerFilter';
import toast from 'react-hot-toast';

const Listings = () => {
    const [loading, setLoading] = useState(true);
    const [arbs, setArbs] = useState([]);
    const [sportFilter, setSportFilter] = useState('all');
    const [sortBy, setSortBy] = useState('profit');
    const [lastUpdated, setLastUpdated] = useState(null);
    const [tick, setTick] = useState(0);

    const fetchArbs = () => {
        setLoading(true);
        fetch('http://localhost:5001/api/listings')
        .then(res => res.json())
        .then(data => {
          setArbs(data);
          setLastUpdated(new Date());
          setTimeout(() => {
              setLoading(false);
            }, 700);
        })
        .catch(err => {
          console.error("Failed to load arbs", err);
          setLoading(false);
        });
    }

    const checkTimeElapsed = () => {
        const now = Date.now();
        const diffMs = now - lastUpdated.getTime();
        if (diffMs >= 180000) {
            return true
        }
        return false
    }

    useEffect(() => {
        const interval = setInterval(() => {
          setTick(t => t + 1); 
        }, 300000); // forces a re-render every 5 minutes
    })

    useEffect(() => {
        fetchArbs();
        const interval = setInterval(() => {
            const stat = checkTimeElapsed()
            if (stat) {
                toast((t, {duration: Infinity}) => (
                    <span>
                      Arbs may be stale. Refresh now!
                      <button onClick={() => toast.dismiss(t.id)}>
                        Dismiss
                      </button>
                    </span>
                  ));
            }
        }, 180000); // Note to self: units in ms. Set to 3 mins.
    
        return () => clearInterval(interval);
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
                    {lastUpdated && (
                        <p className={`text-md ${ Date.now() - lastUpdated.getTime() > 20000
                                ? 'text-red-500'
                                : 'text-base-content/60'
                            }`}>
                            Last refreshed at {lastUpdated.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </p>
                    )}
                </div>
                <ArbFilters 
                    sportFilter={sportFilter}
                    setSportFilter={setSportFilter}
                />
                <button 
                    className="btn btn-sm btn-primary"
                    onClick={() => window.location.reload()}
                >Refresh</button>
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