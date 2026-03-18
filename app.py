import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

from services import (
    DEFAULT_CURRENCY,
    DEFAULT_DIRECTION,
    DEFAULT_SORT_FIELD,
    fetch_top_coins,
    filter_coins,
    normalize_currency,
    normalize_direction,
    normalize_sort_field,
    sort_coins,
)

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "")
    currency = normalize_currency(request.args.get("currency", DEFAULT_CURRENCY))
    sort_by = normalize_sort_field(request.args.get("sort", DEFAULT_SORT_FIELD))
    direction = normalize_direction(request.args.get("direction", DEFAULT_DIRECTION))

    error_message = None
    coins = []

    try:
        coins = fetch_top_coins(currency=currency, per_page=50)
        coins = filter_coins(coins, query)
        coins = sort_coins(coins, sort_by=sort_by, direction=direction)
    except Exception:
        error_message = "Unable to load market data right now. Please try again shortly."

    return render_template(
        "index.html",
        coins=coins,
        query=query,
        currency=currency,
        sort_by=sort_by,
        direction=direction,
        error_message=error_message,
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"

    app.run(host="0.0.0.0", port=port, debug=debug)