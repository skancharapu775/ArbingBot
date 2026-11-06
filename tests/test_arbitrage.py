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

    arbs = detect_arbitrage(event)

    assert len(arbs) == 1
    arb = arbs[0]
    assert arb["outcomes"]["Home"]["bookmaker"] == "DraftKings"
    assert arb["outcomes"]["Home"]["price"] == 2.10
    assert arb["outcomes"]["Away"]["bookmaker"] == "FanDuel"
    assert arb["outcomes"]["Away"]["price"] == 2.20
    implied = 1 / 2.10 + 1 / 2.20
    assert implied < 1
    assert arb["implied_prob"] == pytest.approx(implied)
    assert arb["profit_margin"] == round((1 - implied) * 100, 2)


def test_no_arbitrage_when_implied_probability_sums_above_one():
    event = make_event([("DraftKings", [("Home", 1.50), ("Away", 1.50)])])

    assert detect_arbitrage(event) == []


def test_no_arbitrage_when_implied_probability_sums_to_exactly_one():
    # 1/2 + 1/2 == 1, which is a fair market, not an arb.
    event = make_event([("DraftKings", [("Home", 2.0), ("Away", 2.0)])])

    assert detect_arbitrage(event) == []


def _book(title, markets):
    return {
        "title": title,
        "markets": [
            {
                "key": key,
                "outcomes": [
                    {"name": name, "price": price, **({"point": point} if point is not None else {})}
                    for name, price, point in outcomes
                ],
            }
            for key, outcomes in markets
        ],
    }


def test_moneyline_is_not_compared_with_a_spread():
    event = {
        "home_team": "Spurs",
        "away_team": "Timberwolves",
        "sport_key": "basketball_nba",
        "bookmakers": [
            _book("BetMGM", [("h2h", [("Timberwolves", 5.75, None), ("Spurs", 1.15, None)])]),
            _book("BetRivers", [
                ("h2h", [("Timberwolves", 5.40, None), ("Spurs", 1.16, None)]),
                ("spreads", [("Timberwolves", 1.85, 13.5), ("Spurs", 1.95, -13.5)]),
            ]),
        ],
    }

    assert detect_arbitrage(event) == []


def test_spread_arbitrage_requires_the_same_point():
    event = {
        "home_team": "Home",
        "away_team": "Away",
        "sport_key": "basketball_nba",
        "bookmakers": [
            _book("DraftKings", [("spreads", [("Home", 2.10, -3.5), ("Away", 1.90, 3.5)])]),
            _book("FanDuel", [("spreads", [("Home", 1.85, -3.5), ("Away", 2.15, 3.5)])]),
            _book("BetMGM", [("spreads", [("Home", 1.50, -7.5), ("Away", 2.80, 7.5)])]),
        ],
    }

    arbs = detect_arbitrage(event)

    assert len(arbs) == 1
    assert arbs[0]["outcomes"]["Home"]["price"] == 2.10
    assert arbs[0]["outcomes"]["Home"]["point"] == -3.5
    assert arbs[0]["outcomes"]["Away"]["price"] == 2.15
    assert arbs[0]["outcomes"]["Away"]["point"] == 3.5


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
