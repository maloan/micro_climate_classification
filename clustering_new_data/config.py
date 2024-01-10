"""
Constant values used throughout the program.
"""

# Temperature correction coefficients
TEMP_CORRECTION_COEFFICIENT = 0.775
TEMP_CORRECTION_INTERCEPT = 2.748

# Temperature thresholds
TEMPERATURE_THRESHOLDS = [
    [-2, 0, 3],  # January
    [-2, 1, 4],  # February
    [1, 5, 9],  # March
    [4, 9, 13],  # April
    [9, 13, 17],  # May
    [12, 16, 20],  # June
    [14, 18, 22],  # July
    [14, 18, 22],  # August
    [10, 14, 17],  # September
    [5, 9, 13],  # October
    [0, 4, 7],  # November
    [-1, 0, 3]  # December
]

# DNI thresholds
RADIATION_THRESHOLDS = [
    [0, 43, 191],  # January
    [0, 77, 278],  # February
    [0, 126, 364],  # March
    [0, 166, 414],  # April
    [0, 201, 412],  # May
    [0, 220, 442],  # June
    [0, 226, 456],  # July
    [0, 195, 423],  # August
    [0, 140, 358],  # September
    [0, 87, 278],  # October
    [0, 49, 210],  # November
    [0, 34, 190]  # December
]

# Start time for maximum divergence
MIN_TIME = 11

# End time for maximum divergence
MAX_TIME = 16

# Voltage threshold
VOLTAGE_THRESHOLD = 5.0
