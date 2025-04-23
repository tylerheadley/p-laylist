import numpy as np

def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2)**2))

def knn_neighbors(training_data, training_labels, test_point, k=3):
    distances = []
    for i, point in enumerate(training_data):
        distance = euclidean_distance(test_point, point)
        distances.append((distance, training_labels[i], i, point))
    
    # Sort neighbors by ascending distance (closest first)
    distances.sort(key=lambda x: x[0])
    return distances[:k]

# Example usage:
if __name__ == '__main__':
    # A simple dataset of 3-dimensional vectors
    training_data = np.array([
        [1.0, 2.0, 3.0],
        [2.0, 3.0, 4.0],
        [3.0, 1.0, 2.0],
        [8.0, 9.0, 10.0],
        [9.0, 8.0, 11.0],
        [10.0, 10.0, 10.0]
    ])
    training_labels = np.array([0, 0, 0, 1, 1, 1])
    
    # Define a new test 3D point
    test_point = np.array([4.0, 4.0, 4.0])
    
    # Retrieve the 3 nearest neighbors
    neighbors = knn_neighbors(training_data, training_labels, test_point, k=3)
    
    # Print the neighbors
    print("The 3 nearest neighbors to", test_point, "are:")
    for distance, label, idx, vector in neighbors:
        print(f"Index: {idx}, Distance: {distance:.2f}, Label: {label}, Vector: {vector}")