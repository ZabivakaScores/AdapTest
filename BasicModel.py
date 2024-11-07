import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

# Step 1: Load Data from CSV
data = pd.read_csv('C:/Users/insar4/OneDrive - ABB/Documents/Adaptest/input_data.csv')

# Separate features (X) and target (y)
X = data[['Load (%)']]
y = data['Response time (s)']

# Step 2: Apply Polynomial Regression for Non-Linear Relationship
poly = PolynomialFeatures(degree=2)  # You can experiment with the degree (e.g., 2 or 3)
X_poly = poly.fit_transform(X)
model = LinearRegression()
model.fit(X_poly, y)

# Step 3: Generate New Test Cases with Boundary and Randomized Load Values

# Define boundary test cases and random load values
boundary_loads = [1, 5, 95, 100]  # Boundary values (you can adjust as needed)
random_loads = np.random.randint(1, 100, size=5)  # Random values between 1 and 100

# Combine both sets of loads
new_loads = np.concatenate([boundary_loads, random_loads])
new_loads = np.unique(new_loads)  # Remove duplicates if any

# Predict response times for these new loads
new_loads_poly = poly.transform(new_loads.reshape(-1, 1))
predicted_response_times = model.predict(new_loads_poly)

# Create DataFrame for the suggested test cases
suggested_test_cases = pd.DataFrame({
    'Load (%)': new_loads,
    'Predicted Response time (s)': predicted_response_times
})

print("Additional Suggested Test Cases:")
print(suggested_test_cases)

# Step 4: Optional Visualization

# Plot initial data points and predicted values for new load cases
plt.scatter(X, y, color='blue', label='Initial Data')
plt.plot(new_loads, predicted_response_times, color='red', linestyle='--', label='Predicted Test Cases')
plt.xlabel('Load (%)')
plt.ylabel('Response time (s)')
plt.title('Load vs Response Time with Additional Test Cases')
plt.legend()
plt.show()