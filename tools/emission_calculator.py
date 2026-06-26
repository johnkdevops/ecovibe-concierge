## 📊 Emission Calculator

### Usage
from tools.emission_calculator import EmissionCalculator

calculator = EmissionCalculator()

# Calculate emissions
emissions = calculator.calculate_emissions(
    activity="driving",
    distance=100,
    unit="miles"
)

# Get recommendations
recommendations = calculator.get_recommendations(
    activity="driving",
    distance=100,
    unit="miles"
)