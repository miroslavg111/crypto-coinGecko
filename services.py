import os
import time
from typing import Any, Dict, List

import requests

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

DEFAULT_CURRENCY = "eur"
DEFAULT_SORT_FIELD = "market_cap"
DEFAULT_DIRECTION = "desc"

ALLOWED_CURRENCIES = {"usd", "eur", "bgn"}
ALLOWED_SORT_FIELDS = {"market_cap", "price", "change_24h", "volume", "rank"}

CACHE_TTL_SECONDS = 60

_cache: dict[str, dict[str, Any]] = {}


def get_api_key() -> str | None:
    value = os.getenv("COINGECKO_API_KEY", "").strip()
    return value or None


def normalize_currency(currency: str | None) -> str:
    if not currency:
        return DEFAULT_CURRENCY

    value = currency.strip().lower()
    return value if value in ALLOWED_CURRENCIES else DEFAULT_CURRENCY


def normalize_sort_field(sort_by: str | None) -> str:
    if not sort_by:
        return DEFAULT_SORT_FIELD

    value = sort_by.strip().lower()
    return value if value in ALLOWED_SORT_FIELDS else DEFAULT_SORT_FIELD


def normalize_direction(direction: str | None) -> str:
    if not direction:
        return DEFAULT_DIRECTION

    value = direction.strip().lower()
    return value if value in {"asc", "desc"} else DEFAULT_DIRECTION


def fetch_top_coins(currency: str = DEFAULT_CURRENCY, per_page: int = 50) -> List[Dict[str, Any]]:
    currency = normalize_currency(currency)
    cache_key = f"coins:{currency}:{per_page}"

    cached = get_cached_data(cache_key)
    if cached is not None:
        return cached

    url = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {
        "vs_currency": currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1,
        "sparkline": "false",
    }

    headers = build_headers()

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    coins = [transform_coin(item) for item in data]

    set_cached_data(cache_key, coins)
    return coins


def build_headers() -> Dict[str, str]:
    headers: Dict[str, str] = {
        "Accept": "application/json",
    }

    api_key = get_api_key()
    if api_key:
        headers["x-cg-demo-api-key"] = api_key

    return headers


def transform_coin(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "rank": item.get("market_cap_rank"),
        "name": item.get("name", ""),
        "symbol": item.get("symbol", "").upper(),
        "price": item.get("current_price"),
        "change_24h": item.get("price_change_percentage_24h"),
        "volume": item.get("total_volume"),
        "market_cap": item.get("market_cap"),
    }


def filter_coins(coins: List[Dict[str, Any]], query: str | None) -> List[Dict[str, Any]]:
    if not query:
        return coins

    query = query.strip().lower()
    if not query:
        return coins

    filtered = []
    for coin in coins:
        name = str(coin.get("name", "")).lower()
        symbol = str(coin.get("symbol", "")).lower()

        if query in name or query in symbol:
            filtered.append(coin)

    return filtered


def sort_coins(
    coins: List[Dict[str, Any]],
    sort_by: str = DEFAULT_SORT_FIELD,
    direction: str = DEFAULT_DIRECTION,
) -> List[Dict[str, Any]]:
    sort_by = normalize_sort_field(sort_by)
    direction = normalize_direction(direction)

    reverse = direction == "desc"

    return sorted(
        coins,
        key=lambda coin: safe_number(coin.get(sort_by)),
        reverse=reverse,
    )


def safe_number(value: Any) -> float:
    if value is None:
        return float("-inf")

    if isinstance(value, (int, float)):
        return float(value)

    try:
        return float(value)
    except (TypeError, ValueError):
        return float("-inf")


def get_cached_data(key: str) -> List[Dict[str, Any]] | None:
    entry = _cache.get(key)
    if not entry:
        return None

    if time.time() > entry["expires_at"]:
        _cache.pop(key, None)
        return None

    return entry["data"]


def set_cached_data(key: str, data: List[Dict[str, Any]]) -> None:
    _cache[key] = {
        "data": data,
        "expires_at": time.time() + CACHE_TTL_SECONDS,
    }