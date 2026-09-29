def generate():
    """
    API endpoint: POST JSON config → returns generated password(s) + strength.
    """
    data = request.get_json()

    length           = max(8, min(32, int(data.get("length", 16))))
    use_upper        = bool(data.get("uppercase",         True))
    use_lower        = bool(data.get("lowercase",         True))
    use_numbers      = bool(data.get("numbers",           True))
    use_symbols      = bool(data.get("symbols",           True))
    no_repeat        = bool(data.get("no_repeat",         False))
    exclude_ambiguous= bool(data.get("exclude_ambiguous", False))
    count            = max(1, min(10, int(data.get("count", 1))))

    passwords = generate_batch(
        count, length, use_upper, use_lower,
        use_numbers, use_symbols, no_repeat, exclude_ambiguous
    )

    results = [
        {"password": pw, "strength": analyse_strength(pw)}
        for pw in passwords
    ]

    return jsonify({"passwords": results})


@app.route("/check", methods=["POST"])
