import React, { useState } from 'react';

const BOOKMAKERS = [
    "betmgm", "betonlineag", "betrivers", "betus", "bovada", "caesars",
    "draftkings", "fanduel", "fanatics", "lowvig", "mybookieag"
];

const BookmakerFilter = ({ onApply }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [selectedBookmakers, setSelectedBookmakers] = useState([]);

    const toggleBookmaker = (bookmaker) => {
        setSelectedBookmakers(prev => 
            prev.includes(bookmaker)
                ? prev.filter(b => b !== bookmaker)
                : [...prev, bookmaker]
        );
    };

    const handleApply = () => {
        onApply(selectedBookmakers);
        setIsOpen(false);
    };

    return (
        <div className="relative">
            <button
                onClick={() => setIsOpen(true)}
                className="btn btn-sm btn-primary"
            >
                Select Bookmakers
            </button>

            {isOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-base-100 rounded-lg p-6 w-96">
                        <h3 className="text-xl font-bold mb-4">Select Bookmakers</h3>
                        <div className="grid grid-cols-2 gap-2 mb-4">
                            {BOOKMAKERS.map(bookmaker => (
                                <button
                                    key={bookmaker}
                                    onClick={() => toggleBookmaker(bookmaker)}
                                    className={`btn btn-sm ${
                                        selectedBookmakers.includes(bookmaker)
                                            ? 'btn-primary'
                                            : 'btn-ghost'
                                    }`}
                                >
                                    {bookmaker}
                                </button>
                            ))}
                        </div>
                        <div className="flex justify-end gap-2">
                            <button
                                onClick={() => setIsOpen(false)}
                                className="btn btn-ghost btn-sm"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleApply}
                                className="btn btn-primary btn-sm"
                            >
                                Apply
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default BookmakerFilter;
