import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navigation = () => {
    const location = useLocation();

    return (
        <div className="navbar bg-base-100 border-b border-base-300">
            <div className="container mx-auto">
                <div className="flex-1">
                    <Link to="/" className="text-xl font-bold">
                        ArbingBot
                    </Link>
                </div>
                <div className="flex-none">
                    <ul className="menu menu-horizontal px-1">
                        <li>
                            <Link 
                                to="/" 
                                className={location.pathname === '/' ? 'active' : ''}
                            >
                                Listings
                            </Link>
                        </li>
                        <li>
                            <Link 
                                to="/how-it-works"
                                className={location.pathname === '/how-it-works' ? 'active' : ''}
                            >
                                How It Works
                            </Link>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default Navigation; 