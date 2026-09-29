def index():
    """Home page — renders the generator UI."""
    # Generate a default password on first load
    default_pw = generate_single(
        length=16, charset=build_charset(True, True, True, True, False),
        use_upper=True, use_lower=True, use_numbers=True,
        use_symbols=True, no_repeat=False, exclude_ambiguous=False
    )
    strength = analyse_strength(default_pw)
    return render_template("index.html",
                           default_pw=default_pw,
                           strength=strength)
