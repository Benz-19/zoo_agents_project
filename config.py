# Animal energy settings
ENERGY_DECAY = 3
FEED_ENERGY_GAIN = 35
FEEDING_THRESHOLD = 40  # Feed when energy < 40

# ML settings
ML_CONFIDENCE_THRESHOLD = 0.65

# Food supply settings
FOOD_DECREASE = 2  # Food decreases by this amount each tick
LOW_FOOD_THRESHOLD = 20  # Warn when food stock is below this

# Food stock settings
INITIAL_FOOD_STOCK = {
    "meat": 1000000000,
    "plants": 20000000,
    "fish": 1000000,
    "insects": 1000000
}

# Timing intervals
TICK_INTERVAL = 2  # Seconds between animal updates
FEEDING_INTERVAL = 3  # Seconds between feeding checks