"""Frontend interface / rendering script for Epi-Spread."""

from __future__ import annotations

from typing import Optional

from flask import Flask, render_template, jsonify, request

from src.core.engine import Engine
from src.config.settings import Settings


app = Flask(__name__)
engine: Optional[Engine] = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state", methods=["GET"])
def get_state():
    if engine is None:
        return jsonify({"error": "Game not started"}), 400
    stats = engine.get_stats()
    return jsonify({
        "state": engine.get_state().name,
        "day": stats.day,
        "susceptible": stats.susceptible,
        "infected": stats.infected,
        "recovered": stats.recovered,
        "dead": stats.dead,
        "vaccinated": stats.vaccinated,
        "action_points": stats.action_points,
    })


@app.route("/api/start", methods=["POST"])
def start_game():
    global engine
    engine = Engine(Settings())
    engine.start_game()
    return jsonify({"status": "started"})


@app.route("/api/turn", methods=["POST"])
def end_turn():
    if engine is None:
        return jsonify({"error": "Game not started"}), 400
    engine.end_turn()
    return jsonify({"status": "turn_complete"})


@app.route("/api/action/vaccinate", methods=["POST"])
def vaccinate():
    if engine is None:
        return jsonify({"error": "Game not started"}), 400
    data = request.get_json()
    x, y = data.get("x"), data.get("y")
    success = engine.vaccinate_cell(x, y)
    return jsonify({"success": success})


@app.route("/api/action/lockdown", methods=["POST"])
def lockdown():
    if engine is None:
        return jsonify({"error": "Game not started"}), 400
    data = request.get_json()
    x, y = data.get("x"), data.get("y")
    success = engine.lockdown_cell(x, y)
    return jsonify({"success": success})


if __name__ == "__main__":
    app.run(debug=True)