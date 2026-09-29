def check():
    """
    API endpoint: POST {"password": "..."} → returns strength analysis.
    """
    data     = request.get_json()
    password = data.get("password", "")
    return jsonify(analyse_strength(password))
