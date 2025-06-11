import { Link } from "react-router-dom";
import { useEffect } from "react";
import { Coins } from 'lucide-react';

const Navbar = () => {

  return (
    <header
      className="border-b border-base-300 fixed w-full top-0 z-50  h-16
    backdrop-blur-lg bg-base-100/80 pb-10"
    >
      <div className="container mx-auto px-4 h-16">
        <div className="flex items-center justify-between h-full">
          {/* Left Side: Logo */}
          <div className="flex items-center gap-4">
            <Link to="/" className="flex items-center gap-2.5 hover:opacity-80 transition-all">
              <div className="size-9 rounded-lg bg-primary/10 flex items-center justify-center">
                <Coins className="w-5 h-5 text-blue-700" />
              </div>
              <h1 className="text-lg font-bold">Arbs4You</h1>
            </Link>
          </div>

          {/* Right Side: Links */}
          <div className="flex items-center gap-5">
            <Link
                to="/how-it-works"
                className="btn btn-sm btn-outline text-blue-700 normal-case"
              >
                How it works
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar; 