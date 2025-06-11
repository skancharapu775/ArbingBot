import React from 'react';

const HowItWorks = () => {
    return (
        <div className="max-w-4xl mx-auto p-6 space-y-8">
            <h1 className="text-4xl font-bold text-center mb-8">How Sports Betting Arbitrage Works</h1>

            <section className="space-y-4">
                <h2 className="text-2xl font-semibold text-primary">What is Arbitrage Betting?</h2>
                <p className="text-lg">
                    Arbitrage betting (also known as "arbing" or "sure betting") is a technique where you place bets on all possible outcomes of an event across different bookmakers to guarantee a profit, regardless of the result.
                </p>
            </section>

            <section className="space-y-4">
                <h2 className="text-2xl font-semibold text-primary">How Does It Work?</h2>
                <div className="space-y-4">
                    <div className="bg-base-200 p-4 rounded-lg">
                        <h3 className="text-xl font-semibold mb-2">1. Find Price Differences</h3>
                        <p>
                            Different bookmakers may offer different odds for the same event. Our system automatically scans multiple bookmakers to find these price differences.
                        </p>
                    </div>

                    <div className="bg-base-200 p-4 rounded-lg">
                        <h3 className="text-xl font-semibold mb-2">2. Calculate Stakes</h3>
                        <p>
                            For each arbitrage opportunity, we calculate the optimal stake for each outcome to ensure a profit regardless of the result. The calculation takes into account:
                        </p>
                        <ul className="list-disc list-inside mt-2 space-y-1">
                            <li>Odds from each bookmaker</li>
                            <li>Total investment amount</li>
                            <li>Profit margin</li>
                        </ul>
                    </div>

                    <div className="bg-base-200 p-4 rounded-lg">
                        <h3 className="text-xl font-semibold mb-2">3. Place the Bets</h3>
                        <p>
                            Once you've identified an arbitrage opportunity, you need to place the bets quickly before the odds change. Our system shows you:
                        </p>
                        <ul className="list-disc list-inside mt-2 space-y-1">
                            <li>Which bookmakers to use</li>
                            <li>How much to bet on each outcome</li>
                            <li>Your guaranteed profit</li>
                        </ul>
                    </div>
                </div>
            </section>

            <section className="space-y-4">
                <h2 className="text-2xl font-semibold text-primary">Example</h2>
                <div className="bg-base-200 p-6 rounded-lg">
                    <p className="mb-4">Let's say we have a tennis match between Player A and Player B:</p>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="bg-base-100 p-4 rounded">
                            <h4 className="font-semibold">Bookmaker 1</h4>
                            <p>Player A: 2.10</p>
                            <p>Player B: 1.90</p>
                        </div>
                        <div className="bg-base-100 p-4 rounded">
                            <h4 className="font-semibold">Bookmaker 2</h4>
                            <p>Player A: 1.95</p>
                            <p>Player B: 2.05</p>
                        </div>
                    </div>
                    <p className="mt-4">
                        By betting $100 on Player A at Bookmaker 1 and $102.44 on Player B at Bookmaker 2, you guarantee a profit of $7.56 regardless of who wins!
                    </p>
                </div>
            </section>

            <section className="space-y-4">
                <h2 className="text-2xl font-semibold text-primary">Important Considerations</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-base-200 p-4 rounded-lg">
                        <h3 className="text-xl font-semibold mb-2">Advantages</h3>
                        <ul className="list-disc list-inside space-y-1">
                            <li>Guaranteed profit</li>
                            <li>No risk of losing</li>
                            <li>Works with any sport</li>
                            <li>Can be automated</li>
                        </ul>
                    </div>
                    <div className="bg-base-200 p-4 rounded-lg">
                        <h3 className="text-xl font-semibold mb-2">Challenges</h3>
                        <ul className="list-disc list-inside space-y-1">
                            <li>Need multiple bookmaker accounts</li>
                            <li>Odds can change quickly</li>
                            <li>Bookmakers may limit accounts</li>
                            <li>Requires significant capital</li>
                        </ul>
                    </div>
                </div>
            </section>

            <section className="space-y-4">
                <h2 className="text-2xl font-semibold text-primary">Getting Started</h2>
                <div className="bg-base-200 p-4 rounded-lg">
                    <ol className="list-decimal list-inside space-y-2">
                        <li>Create accounts with multiple bookmakers</li>
                        <li>Fund your accounts</li>
                        <li>Use our platform to find arbitrage opportunities</li>
                        <li>Place your bets quickly when you find a good opportunity</li>
                        <li>Monitor your accounts and profits</li>
                    </ol>
                </div>
            </section>
        </div>
    );
};

export default HowItWorks; 