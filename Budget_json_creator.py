import json

budget = {
    "EmergencySavings": {
        "Name": "EmergencySavings",
        "Type": "Emergency Fund",
        "Cash": 500,
        "Assets": [
            {
                "Symbol": "QQQ",
                "Qty": 2,
            },
            {
                "Symbol": "QYLG",
                "Qty": 3,
            },
        ]
    },
    "Books": {
        "Name": "Books",
        "Type": "Low Income",
        "Cash": 500,
        "Assets": [
            {
                "Symbol": "QQQ",
                "Qty": 10,
            },
            {
                "Symbol": "QYLG",
                "Qty": 30,
            },
        ]
    },
}

print(budget)
with open("Budgets/default.json", "w") as f:
    json.dump(budget, f)
