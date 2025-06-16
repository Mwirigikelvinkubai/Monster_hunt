_chart = {
    "Fire":  {"Earth": 1.5, "Water": 0.5},
    "Water": {"Fire": 1.5,  "Earth": 0.5},
    "Earth": {"Air": 1.5,   "Fire": 0.5},
    "Air":   {"Water": 1.5, "Earth": 0.5},
}
def multiplier(att, dfn):            # fallback 1.0
    return _chart.get(att, {}).get(dfn, 1.0)
