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

def extract_spectrogram(wav_file, n_fft=2048, hop_length=1024, win_length=None):
    """
    Compute the raw spectrogram of a .wav file
    
    Parameters:
        wav_file (str): Path to the wav file.
        n_fft (int): The number of FFT points, 
                     larger values indicate better frequnecy resolution at the 
                     cost of time resolution
        hop_length (int): Number of samples between successive frames.
                          larger value reduce overlap between frame, but reduces
                          time resolution
        win_length (int): The length of the window for STFT
    
    Returns:
        np.ndarray: Spectrogram of audio file.
    """

    # Load audio file
    y, sr = librosa.load(wav_file, sr=None)
    
    # Find STFT (spectrogram)
    spectrogram = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
    
    # Change it to magnitude
    magnitude = np.abs(spectrogram)
    
    return magnitude

def extract_chroma_features(wav_file, n_chroma=12):
    """
    Load a wav file and extract Chroma features.
    
    Parameters:
        wav_file (str): Path to the wav file.
        n_chroma (int): Number of chroma coefficients to extra
                        There are twelve different pitch coefficients.
    
    Returns:
        np.ndarray: A vector of averaged Chroma features of shape (n_chroma,).
    """
    # Load audio file with its native sampling rate
    y, sr = librosa.load(wav_file, sr=None)
    
    # Compute MFCCs: result shape is (n_mfcc, n_frames)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_chroma=n_chroma)
    
    # Average MFCCs across time frames to get a single vector per file
    chroma_mean = np.mean(chroma, axis=1)
    
    return chroma_mean

def extract_tempogram(wav_file, hop_length=512):
    """
    Load a wav file and extract tempo features.
    
    Parameters:
        wav_file (str): Path to the wav file.
        hop_length (int): Hop length for frame extraction
                          512 seems to be the norm (???)
    
    Returns:
        np.ndarray: Tempogram of audio file.
    """
    # Load audio file with its native sampling rate
    y, sr = librosa.load(wav_file, sr=8000)
    
    # Compute the tempogram
    tempogram = librosa.feature.tempogram(y=y, sr=sr, hop_length=hop_length)

    return tempogram

def extract_rhythm(wav_file, hop_length=512):
    """
    Load a wav file and extract spectral rhythm features - tempogram-ratio.
    
    Parameters:
        wav_file (str): Path to the wav file.
        hop_length (int): Hop length for frame extraction
                          512 seems to be the norm (???)
    
    Returns:
        np.ndarray: Tempogram of audio file.
    """
    # Load audio file with its native sampling rate
    y, sr = librosa.load(wav_file, sr=8000)
    
    # Compute the tempogram
    spectral_rhythm = librosa.feature.tempogram_ratio(y=y, sr=sr, hop_length=hop_length)

    return spectral_rhythm


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
                    # Commented out mfcc for now
                    # mfcc_features = extract_mfcc_features(file_path)
                    #projected_features = random_feature_map(mfcc_features, target_dim=target_dim)

                    # Commented out chroma for now
                    # chroma_features = extract_chroma_features(file_path)
                    # projected_features = random_feature_map(chroma_features, target_dim=target_dim)

                    # Commented out tempogram for now
                    # Extract tempogram for the file (an array)
                    # tempogram = extract_tempogram(file_path)

                    # Convert the tempogram to a 1D vector
                    # tempogram_flat = tempogram.flatten()

                    # Apply random feature map to the tempogram
                    # projected_features = random_feature_map(tempogram_flat, target_dim=target_dim)

                    # Commented out spectral rhythm for now
                    # Extract rhythm for the file (an array)
                    # spectral_rhythm = extract_rhythm(file_path)

                    # Convert the spectral rhythm tempogram to a 1D vector
                    # rhythm_flat = spectral_rhythm.flatten()

                    # Apply random feature map to the rhythm features
                    # projected_features = random_feature_map(rhythm_flat, target_dim=target_dim)

                    spectrogram = extract_spectrogram(file_path)
                    
                    # Convert the spectrogram into a 1D vector
                    spectrogram_flat = spectrogram.flatten()

                    projected_features = random_feature_map(spectrogram_flat, target_dim=target_dim)


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