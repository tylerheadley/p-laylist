import os
import numpy as np
import librosa

#TODO: Complete RFM processing for a folder (iterate through subdirectories and process .wav)

def extract_mfcc_features(wav_file, n_mfcc=16):
    """
    Load a wav file and extract MFCC features.
    
    Parameters:
        wav_file (str): Path to the wav file.
        n_mfcc (int): Number of MFCC coefficients to extract.
    
    Returns:
        np.ndarray: A vector of averaged MFCCs of shape (n_mfcc,).
    """
    # Load audio file with its native sampling rate
    y, sr = librosa.load(wav_file, sr=None)
    
    # Compute MFCCs: result shape is (n_mfcc, n_frames)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    
    # Average MFCCs across time frames to get a single vector per file
    mfccs_mean = np.mean(mfccs, axis=1)
    
    return mfccs_mean

def random_feature_map(features, target_dim=8, random_state=42):
    """
    Applies a random projection to reduce the dimensionality of the feature vector.
    
    Parameters:
        features (np.ndarray): Input feature vector (shape: (original_dim,)).
        target_dim (int): The target lower dimension.
        random_state (int): Seed for reproducibility.
        
    Returns:
        np.ndarray: The transformed feature vector of shape (target_dim,).
    """
    np.random.seed(random_state)
    original_dim = features.shape[0]
    
    # Create a random projection matrix
    random_matrix = np.random.randn(original_dim, target_dim)
    
    # Project the feature vector using the random matrix
    projected_features = np.dot(features, random_matrix)
    
    return projected_features

def process_directory(directory, target_dim=8):
    """
    Recursively process all .wav files in a directory and its subdirectories.
    
    Parameters:
        directory (str): The root directory to search.
        target_dim (int): Target dimension after random feature mapping.
    
    Returns:
        dict: A dictionary where keys are file paths and values are the processed feature vectors.
    """
    results = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".wav"):
                file_path = os.path.join(root, file)
                try:
                    mfcc_features = extract_mfcc_features(file_path)
                    projected_features = random_feature_map(mfcc_features, target_dim=target_dim)
                    results[file_path] = projected_features
                    print(f"Processed: {file_path}")
                except Exception as e:
                    print(f"Failed processing {file_path} with error: {e}")
    return results

def main():
    folder = input("Enter the folder path containing wav files: ")
    # Adjust target_dim if needed; default here is 8.
    results = process_directory(folder, target_dim=8)
    
    print("\nFinal processed features:")
    for file_path, features in results.items():
        print(f"\nFile: {file_path}")
        print("Projected features:", features)

if __name__ == "__main__":
    main()