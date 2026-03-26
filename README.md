# Route Optimizer (Route_OP)

A Python-based web application designed to calculate and display the most optimal travel routes between predefined destinations. It evaluates multiple pathways and provides detailed cost breakdowns based on vehicle dynamics and distances.

## Description

The `Route_OP` project leverages a Flask backend to serve a route optimization engine. At its core, it implements **Dijkstra's Algorithm** paired with a modified **Yen’s k-shortest paths** approach to identify up to three of the best available routes between source and destination nodes across a statically defined adjacency matrix (representing locations tightly clustered around Belagavi, like Central Bus Stand, KLE University, and Tilakwadi).

Beyond simply finding the shortest physical path, the application features a robust `CostCalculator` that factors in:
- Base vehicle fixed costs (Bike, Car, SUV, etc.)
- Dynamic fuel costs based on travel distance and vehicle mileage
- Passenger rates
- Toll segment charges
- Per-kilometer maintenance costs

This comprehensive cost and route calculation provides users with a transparent array of alternative routes to choose from.

## How to Use and Run

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- (Optional but recommended) A virtual environment

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/spro047/Route_OP.git
   cd Route_OP
   ```

2. **Install dependencies**:
   Ensure you have Flask installed.
   ```bash
   pip install Flask
   ```

3. **Start the Flask Server**:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   Open a web browser and navigate to `http://127.0.0.1:5000`. You will be presented with the frontend UI where you can input your source, destination, vehicle type, and current fuel/mileage metrics.

## Challenges Faced

Developing this routing and cost-optimization engine presented a few core algorithmic logic challenges:

1. **K-Shortest Paths Algorithm Implementation**: Relying solely on Dijkstra's Algorithm only yields the *absolute shortest* path. Ensuring users received 2nd and 3rd alternative routes required carefully implementing a Yen-like spur path algorithm dynamically on an adjacency matrix, temporarily removing and restoring edges without corrupting the core graph data structure.
2. **Abstracting the Cost Calculations**: Structuring the backend so that cost calculation logic (Fuel, Tolls, Vehicle type modifiers) was entirely decoupled from the geometric pathfinding logic. This ensures that toll rates or petrol prices can be adjusted centrally in the `CostCalculator` class without risking logical breaks in the graph algorithms.
3. **Handling Disconnected Graphs (Unreachable Nodes)**: Ensuring the Dijkstra algorithm appropriately returned empty arrays (and subsequently triggered user-friendly error messages on the frontend) if a destination node happened to be mathematically unreachable from the source within the adjacency matrix.
4. **Data Normalization**: Guaranteeing that edge cases (like users inputting negative mileage or 0 available fuel) were gracefully defaulted or caught before throwing mathematical ZeroDivisionErrors during the `fuel_cost` operations.
