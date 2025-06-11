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
                    <p className="mb-4">Let's say we have a baseball game between the Los Angeles Angels and Oakland Athletics:</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        <div className="bg-base-100 p-4 rounded">
                            <h4 className="font-semibold">FanDuel</h4>
                            <p>Los Angeles Angels: 1.22</p>
                            <p>Oakland Athletics: 4.20</p>
                        </div>
                        <div className="bg-base-100 p-4 rounded">
                            <h4 className="font-semibold">DraftKings</h4>
                            <p>Los Angeles Angels: 1.24</p>
                            <p>Oakland Athletics: 3.92</p>
                        </div>
                        <div className="bg-base-100 p-4 rounded">
                            <h4 className="font-semibold">BetMGM</h4>
                            <p>Los Angeles Angels: 1.25</p>
                            <p>Oakland Athletics: 3.90</p>
                        </div>
                        <div className="bg-base-100 p-4 rounded">
                            <h4 className="font-semibold">MyBookie.ag</h4>
                            <p>Los Angeles Angels: 1.18</p>
                            <p>Oakland Athletics: 4.60</p>
                        </div>
                        <div className="bg-base-100 p-4 rounded">
                            <h4 className="font-semibold">Bovada</h4>
                            <p>Los Angeles Angels: 1.22</p>
                            <p>Oakland Athletics: 4.00</p>
                        </div>
                    </div>
                    <p className="mt-4">
                        By betting $100 on the Angels at MyBookie.ag (1.18) and $25.65 on the Athletics at FanDuel (4.20), you guarantee a profit of $4.35 regardless of who wins!
                    </p>
                </div>
            </section>

            <section className="space-y-4">
                <h2 className="text-2xl font-semibold text-primary">Supported Bookmakers</h2>
                <div className="bg-base-200 p-6 rounded-lg">
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">FanDuel</h4>
                        </div>
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">DraftKings</h4>
                        </div>
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">BetMGM</h4>
                        </div>
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">MyBookie.ag</h4>
                        </div>
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">Bovada</h4>
                        </div>
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">Caesars</h4>
                        </div>
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">PointsBet</h4>
                        </div>
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">BetRivers</h4>
                        </div>
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">WynnBet</h4>
                        </div>
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">Unibet</h4>
                        </div>
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">Barstool</h4>
                        </div>
                        <div className="bg-base-100 p-4 rounded text-center">
                            <h4 className="font-semibold">FOX Bet</h4>
                        </div>
                    </div>
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