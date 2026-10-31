import pytest

from arb_detector import calculate_stakes, detect_arbitrage


def make_event(books):
    """Build one Odds API event.

    books is a list of (bookmaker title, [(outcome name, decimal odds), ...]).
    """
    return {
        "home_team": "Home",
        "away_team": "Away",
        "sport_key": "basketball_nba",
        "bookmakers": [
            {
                "title": title,
                "markets": [
                    {
                        "outcomes": [
                            {"name": name, "price": price} for name, price in outcomes
                        ]
                    }
                ],
            }
            for title, outcomes in books
        ],
    }


def test_arbitrage_when_best_prices_sum_below_one():
    event = make_event(
        [
            ("DraftKings", [("Home", 2.10), ("Away", 1.80)]),
            ("FanDuel", [("Home", 1.90), ("Away", 2.20)]),
        ]
    )

    arb = detect_arbitrage(event)

    assert arb is not None
    assert arb["outcomes"]["Home"] == {"bookmaker": "DraftKings", "price": 2.10}
    assert arb["outcomes"]["Away"] == {"bookmaker": "FanDuel", "price": 2.20}
    implied = 1 / 2.10 + 1 / 2.20
    assert implied < 1
    assert arb["implied_prob"] == pytest.approx(implied)
    assert arb["profit_margin"] == round((1 - implied) * 100, 2)


def test_no_arbitrage_when_implied_probability_sums_above_one():
    event = make_event([("DraftKings", [("Home", 1.50), ("Away", 1.50)])])

    assert detect_arbitrage(event) is None


def test_no_arbitrage_when_implied_probability_sums_to_exactly_one():
    # 1/2 + 1/2 == 1, which is a fair market, not an arb.
    event = make_event([("DraftKings", [("Home", 2.0), ("Away", 2.0)])])

    assert detect_arbitrage(event) is None


def test_calculate_stakes_splits_stake_by_implied_probability():
    even = calculate_stakes(100, [2.0, 2.0])
    assert even == pytest.approx([50.0, 50.0])

    # Stake on i is S * (1/odds_i) / sum of implied probabilities.
    uneven = calculate_stakes(100, [2.0, 4.0])
    implied_sum = 1 / 2.0 + 1 / 4.0
    assert uneven == pytest.approx(
        [100 * (1 / 2.0) / implied_sum, 100 * (1 / 4.0) / implied_sum]
    )
    assert sum(uneven) == pytest.approx(100)
