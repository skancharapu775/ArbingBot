import React from 'react';

const BookmakerFilter = ({ selectedBookmakers, setSelectedBookmakers }) => {
    const bookmakers = [
        "DraftKings",
        "FanDuel",
        "BetMGM",
        "Caesars",
        "PointsBet",
        "BetRivers",
        "WynnBet",
        "Unibet",
        "Barstool",
        "FOX Bet"
    ];

    const toggleBookmaker = (bookmaker) => {
        if (selectedBookmakers.includes(bookmaker)) {
            setSelectedBookmakers(selectedBookmakers.filter(b => b !== bookmaker));
        } else {
            setSelectedBookmakers([...selectedBookmakers, bookmaker]);
        }
    };

    return (
        <div className="flex flex-wrap gap-2">
            {bookmakers.map((bookmaker) => (
                <button
                    key={bookmaker}
                    onClick={() => toggleBookmaker(bookmaker)}
                    className={`btn btn-sm ${
                        selectedBookmakers.includes(bookmaker)
                            ? 'btn-primary'
                            : 'btn-outline'
                    }`}
                >
                    {bookmaker}
                </button>
            ))}
        </div>
    );
};

export default BookmakerFilter; 