class SharedState:
    animals = {}
    energy_log = {
        "lion": [],
        "elephant": [],
        "zebra": []
    }
    food = {
        "meat": 500,
        "plants": 800,
        "fish": 400
    }
    deaths = {
        "lion": 0,
        "elephant": 0,
        "zebra": 0
    }
    stop_simulation = False
