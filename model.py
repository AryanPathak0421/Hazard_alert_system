# model.py
# Simple rule-based hazard prediction

def predict_hazard(crowd_density, temperature, movement_speed):
    """
    Rule-based hazard prediction.
    """
    hazard_level = "Safe"
    message = "Area is safe."

    # Basic rules
    if crowd_density > 10 or movement_speed < 0.5:
        hazard_level = "Crowded"
        message = "Crowding detected. Monitor closely."

    if crowd_density > 20 or (movement_speed < 0.3 and temperature > 35):
        hazard_level = "Highly Crowded"
        message = "High crowd density! Alert authorities."

    if crowd_density > 30 or (movement_speed < 0.2 and temperature > 38):
        hazard_level = "Critical"
        message = "Critical zone! Immediate action required!"

    return {
        "hazard_level": hazard_level,
        "message": message
    }


if __name__ == "__main__":
    print(predict_hazard(25, 36, 0.2))
