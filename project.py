"""
SecurePass - Random Strong Password Generator
Cyber Security Capstone Project | Lenovo x BharatCares
Author:YASHASHVI SINGH

Uses Python's `secrets` module for cryptographically secure
password generation. No data is stored or transmitted.
"""

import check
import generate
import index
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ─────────────────────────────────────────────
# CHARACTER SETS
# ─────────────────────────────────────────────
UPPERCASE  = string.ascii_uppercase                  # A-Z
LOWERCASE  = string.ascii_lowercase                  # a-z
DIGITS     = string.digits                           # 0-9
SYMBOLS    = "!@#$%^&*()_+-=[]{}|;:,.<>?"           # special chars
AMBIGUOUS  = set("lI1O0")                            # confusing chars


# ─────────────────────────────────────────────
# CORE PASSWORD GENERATOR
# ─────────────────────────────────────────────
def build_charset(use_upper, use_lower, use_numbers, use_symbols, exclude_ambiguous):
    """Build character pool based on user options."""
    charset = ""
    if use_upper:   charset += UPPERCASE
    if use_lower:   charset += LOWERCASE
    if use_numbers: charset += DIGITS
    if use_symbols: charset += SYMBOLS

    if exclude_ambiguous:
        charset = "".join(c for c in charset if c not in AMBIGUOUS)

    return charset or LOWERCASE   # fallback to lowercase if nothing selected


def generate_single(length, charset, use_upper, use_lower,
                    use_numbers, use_symbols, no_repeat, exclude_ambiguous):
    """
    Generate one password using Python's secrets module.
    Guarantees at least one character from each selected category.
    """
    guaranteed = []

    def pick_from(pool):
        p = [c for c in pool if c not in AMBIGUOUS] if exclude_ambiguous else list(pool)
        return secrets.choice(p) if p else None

    if use_upper:   guaranteed.append(pick_from(UPPERCASE))
    if use_lower:   guaranteed.append(pick_from(LOWERCASE))
    if use_numbers: guaranteed.append(pick_from(DIGITS))
    if use_symbols: guaranteed.append(pick_from(SYMBOLS))

    guaranteed = [c for c in guaranteed if c]  # remove None

    remaining = length - len(guaranteed)
    pool = list(charset)

    if no_repeat:
        # Remove already-used chars
        used = set(guaranteed)
        pool = [c for c in pool if c not in used]
        extra = []
        for _ in range(remaining):
            if not pool:
                pool = list(charset)   # refill if exhausted
            c = secrets.choice(pool)
            extra.append(c)
            pool.remove(c)
    else:
        extra = [secrets.choice(pool) for _ in range(remaining)]

    password_chars = guaranteed + extra

    # Shuffle using secrets for true randomness
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


def generate_batch(count, length, use_upper, use_lower, use_numbers,
                   use_symbols, no_repeat, exclude_ambiguous):
    """Generate multiple unique passwords."""
    charset = build_charset(use_upper, use_lower, use_numbers,
                            use_symbols, exclude_ambiguous)
    passwords = []
    seen = set()
    attempts = 0
    while len(passwords) < count and attempts < count * 10:
        pw = generate_single(length, charset, use_upper, use_lower,
                              use_numbers, use_symbols, no_repeat, exclude_ambiguous)
        if pw not in seen:
            passwords.append(pw)
            seen.add(pw)
        attempts += 1
    return passwords


# ─────────────────────────────────────────────
# STRENGTH ANALYSER  (pure Python)
# ─────────────────────────────────────────────
def analyse_strength(password):
    """
    Score a password and return label, color, percentage, and criteria.
    """
    if not password:
        return {"label": "—", "color": "#555555", "percent": 0, "score": 0, "criteria": {}}

    length  = len(password)
    has_up  = any(c in UPPERCASE for c in password)
    has_lo  = any(c in LOWERCASE for c in password)
    has_num = any(c in DIGITS    for c in password)
    has_sym = any(c in SYMBOLS   for c in password)
    unique  = len(set(password))
    repeats = any(password[i] == password[i+1] == password[i+2]
                  for i in range(len(password)-2))

    score = 0
    if length >= 8:  score += 10
    if length >= 12: score += 15
    if length >= 16: score += 20
    if length >= 20: score += 10
    if has_up:       score += 10
    if has_lo:       score += 10
    if has_num:      score += 10
    if has_sym:      score += 15
    if unique > length * 0.7: score += 10
    if repeats:      score -= 10
    if not has_sym and not has_num: score -= 5

    score = max(0, min(100, score))

    if score < 30:
        label, color, percent = "Weak",        "#ef4444", 20
    elif score < 55:
        label, color, percent = "Moderate",    "#f97316", 45
    elif score < 75:
        label, color, percent = "Strong",      "#eab308", 70
    elif score < 90:
        label, color, percent = "Very Strong", "#22c55e", 88
    else:
        label, color, percent = "Excellent!",  "#00f5c4", 100

    criteria = {
        "length_12":  length >= 12,
        "length_16":  length >= 16,
        "uppercase":  has_up,
        "lowercase":  has_lo,
        "numbers":    has_num,
        "symbols":    has_sym,
        "no_repeats": not repeats,
        "unique":     unique,
        "length_val": length,
    }

    return {"label": label, "color": color, "percent": percent,
            "score": score, "criteria": criteria}


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────
@app.route("/")
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


@app.route("/generate", methods=["POST"])
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
def check():
    """
    API endpoint: POST {"password": "..."} → returns strength analysis.
    """
    data     = request.get_json()
    password = data.get("password", "")
    return jsonify(analyse_strength(password))


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  SecurePass – Cyber Security Capstone Project")
    print("  Running at: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True)
