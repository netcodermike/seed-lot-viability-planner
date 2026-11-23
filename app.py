from fractions import Fraction
from math import ceil, isfinite

def analyze(data):
    tested, sprouted, target = (data[key] for key in ("tested", "sprouted", "target"))
    reserve = data["reserve_percent"]
    if any(type(value) is not int for value in (tested, sprouted, target)) or not 0 < sprouted <= tested or target <= 0:
        raise ValueError("Enter positive counts with at least one sprout and no more sprouts than seeds tested")
    if type(reserve) not in (int,float) or not isfinite(reserve) or not 0 <= reserve <= 100:
        raise ValueError("Reserve percent must be between zero and 100")
    rate = Fraction(sprouted, tested)
    base = ceil(target / rate)
    buffered = ceil(base * (1 + Fraction(str(reserve)) / 100))
    return {"observed_rate":round(float(rate), 6), "base_seed_count":base, "with_reserve":buffered}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
