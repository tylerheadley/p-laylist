import numpy as np
import os
from librosa.feature import mfcc
from librosa.core import load
from sklearn.preprocessing import StandardScaler

def extract_mfcc_features(file_path, n_mfcc=16, sr=22050):
    """
    Extracts and normalizes MFCC features, averaged across time, from a spectrogram file.

    Parameters:
    file_path (str): Path to the .npy spectrogram file.
    n_mfcc (int): Number of MFCC coefficients to extract.
    sr (int): Sampling rate for MFCC computation.

    Returns:
    np.ndarray: Averaged and normalized MFCC coefficients (fixed-size vector).
    """
    # Load the spectrogram
    spectrogram = np.load(file_path)

    # Simulate a time-domain signal from the spectrogram
    signal = spectrogram.sum(axis=0)  # Sum over frequency to approximate a waveform

    # Extract MFCC features
    mfcc_features = mfcc(y=signal, sr=sr, n_mfcc=n_mfcc)

    # Average MFCCs across the time dimension
    averaged_mfcc = np.mean(mfcc_features, axis=1)

    # Normalize the MFCC vector (z-score normalization)
    scaler = StandardScaler()
    normalized_mfcc = scaler.fit_transform(averaged_mfcc.reshape(-1, 1)).flatten()

    return normalized_mfcc


def rank_similarity_using_mfcc(input_file, dataset_folder, n_mfcc=16, sr=22050):
    """
    Ranks the similarity of spectrograms based on averaged MFCC features.

    Parameters:
    input_file (str): Path to the input .npy file.
    dataset_folder (str): Path to the folder containing .npy spectrogram files.
    n_mfcc (int): Number of MFCC coefficients to use.
    sr (int): Sampling rate for MFCC computation.

    Returns:
    list: Sorted list of tuples (filename, similarity score).
    """
    # Extract MFCC features for the input spectrogram
    input_mfcc = extract_mfcc_features(input_file, n_mfcc=n_mfcc, sr=sr)

    # Initialize a list for similarity scores
    similarity_scores = []

    # Process each spectrogram file in the dataset
    for file_name in os.listdir(dataset_folder):
        file_path = os.path.join(dataset_folder, file_name)

        # Skip the input file itself
        if file_path == input_file:
            continue

        # Check if the file is an .npy file
        if file_name.endswith('.npy'):
            # Extract MFCC features for the current spectrogram
            current_mfcc = extract_mfcc_features(file_path, n_mfcc=n_mfcc, sr=sr)

            # Compute Euclidean distance as the similarity metric
            distance = np.linalg.norm(input_mfcc - current_mfcc)

            # Append the file name and similarity score
            similarity_scores.append((file_name, distance))

    # Sort similarity scores in ascending order
    similarity_scores.sort(key=lambda x: x[1])

    return similarity_scores


# Example usage
if __name__ == "__main__":
    # Define paths
    input_file = "test_dataset/disco.00000.wav.npy"
    dataset_folder = "test_dataset/"

    # Rank the similarities
    ranked_similarities = rank_similarity_using_mfcc(input_file, dataset_folder)

    # Display the results
    print("Ranked Similarities (file, Euclidean distance):")
    for file_name, distance in ranked_similarities:
        print(f"{file_name}: {distance:.4f}")