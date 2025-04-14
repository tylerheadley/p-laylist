import numpy as np
from collections import Counter

def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2)**2))

def knn_predict(training_data, training_labels, test_point, k=3):
    # Calculate the distance from the test point to every point in the training set.
    distances = []
    for i in range(len(training_data)):
        distance = euclidean_distance(test_point, training_data[i])
        distances.append((distance, training_labels[i]))
    
    # Sort the distances in ascending order (shortest distance first).
    distances.sort(key=lambda x: x[0])
    
    # Extract the labels of the k closest neighbors.
    neighbors = [label for (_, label) in distances[:k]]
    
    # Count the frequency of each label among the neighbors and pick the most common one.
    most_common_label = Counter(neighbors).most_common(1)[0][0]
    return most_common_label

# Example usage:
if __name__ == '__main__':
    # Define a simple dataset of 3-dimensional vectors.
    # Here, we’ve got two classes: class 0 and class 1.
    training_data = np.array([
        [1.0, 2.0, 3.0],
        [2.0, 3.0, 4.0],
        [3.0, 1.0, 2.0],
        [8.0, 9.0, 10.0],
        [9.0, 8.0, 11.0],
        [10.0, 10.0, 10.0]
    ])
    training_labels = np.array([0, 0, 0, 1, 1, 1])
    
    # Define a new 3D point to classify.
    test_point = np.array([6.0, 9.0, 7.0])
    
    # Predict the class for the test_point using k=3.
    prediction = knn_predict(training_data, training_labels, test_point, k=3)
    print("Predicted class:", prediction)