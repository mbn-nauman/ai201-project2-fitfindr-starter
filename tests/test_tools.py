from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import get_example_wardrobe, get_empty_wardrobe


def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0


def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []


def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)


def test_search_no_size_filter():
    results_with_size = search_listings("vintage", size="M", max_price=None)
    results_without_size = search_listings("vintage", size=None, max_price=None)
    assert len(results_without_size) >= len(results_with_size)


def test_search_results_sorted_by_relevance():
    results = search_listings("vintage graphic tee", size=None, max_price=None)
    assert len(results) > 1
    # first result should contain more matching keywords than last
    def score(listing):
        searchable = " ".join([
            listing["title"], listing["description"],
            listing["category"], " ".join(listing["style_tags"])
        ]).lower()
        return sum(1 for kw in "vintage graphic tee".split() if kw in searchable)
    assert score(results[0]) >= score(results[-1])


def test_search_size_case_insensitive():
    results_upper = search_listings("jacket", size="M", max_price=None)
    results_lower = search_listings("jacket", size="m", max_price=None)
    assert results_upper == results_lower


# ── suggest_outfit tests ──────────────────────────────────────────────────────

def test_suggest_outfit_returns_string():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    result = suggest_outfit(results[0], get_example_wardrobe())
    assert isinstance(result, str)
    assert len(result) > 0


def test_suggest_outfit_empty_wardrobe_no_crash():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    result = suggest_outfit(results[0], get_empty_wardrobe())
    assert isinstance(result, str)
    assert len(result) > 0


def test_suggest_outfit_empty_wardrobe_no_error_message():
    # empty wardrobe is a handled case — should return advice, not an error string
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    result = suggest_outfit(results[0], get_empty_wardrobe())
    assert "unable" not in result.lower()


# ── create_fit_card tests ─────────────────────────────────────────────────────

def test_create_fit_card_returns_string():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    outfit = suggest_outfit(results[0], get_example_wardrobe())
    result = create_fit_card(outfit, results[0])
    assert isinstance(result, str)
    assert len(result) > 0


def test_create_fit_card_empty_outfit_guard():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    result = create_fit_card("", results[0])
    assert result == "No outfit suggestion was available to generate a caption from."


def test_create_fit_card_whitespace_outfit_guard():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    result = create_fit_card("   ", results[0])
    assert result == "No outfit suggestion was available to generate a caption from."