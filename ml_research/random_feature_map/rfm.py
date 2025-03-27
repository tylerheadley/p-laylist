import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from sklearn.kernel_approximation import RBFSampler

def prepare_wav_file(file_path, new_dim=8, gamma=1.0):
    """
    Load a WAV file, compute 16 MFCCs, and perform a random feature mapping 
    using scikit-learn's RBFSampler to reduce dimensionality.
    
    The function also plots the MFCC spectrogram and the resulting random feature map.
    
    Parameters:
        file_path (str): Path to the .wav file.
        new_dim (int): The target dimension for the random feature map (n_components).
        gamma (float): Parameter for the RBF kernel in RBFSampler.
                       
    Returns:
        z (np.ndarray): The random feature map vector (of dimension new_dim)
                         ready for input to a KNN classifier.
    """
    # Load the audio file with its original sampling rate
    y, sr = librosa.load(file_path, sr=None)
    
    # Compute 16 MFCCs (resulting in a matrix of shape (16, T))
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=16)
    
    # Plot the MFCC spectrogram
    # plt.figure(figsize=(10, 4))
    # librosa.display.specshow(mfccs, x_axis='time')
    # plt.colorbar()
    # plt.title('MFCC Spectrogram')
    # plt.tight_layout()
    # plt.show()
    
    # Compute a fixed-length representation by taking the mean of MFCCs over time
    mfcc_vector = np.mean(mfccs, axis=1)  # shape: (16,)
    
    # Reshape to (1, 16) as RBFSampler expects 2D input (samples, features)
    mfcc_vector = mfcc_vector.reshape(1, -1)
    
    # Create the RBFSampler instance
    rbf_sampler = RBFSampler(gamma=gamma, n_components=new_dim, random_state=42)
    
    # Fit and transform the MFCC vector to obtain the random feature map
    # Note: For a single sample, fit_transform works fine.
    z = rbf_sampler.fit_transform(mfcc_vector)
    
    # z is of shape (1, new_dim); flatten it to a 1D vector
    z = z.flatten()
    
    # Plot the random feature map as a bar chart
    plt.figure(figsize=(8, 4))
    plt.bar(np.arange(new_dim), z)
    plt.xlabel('Random Feature Index')
    plt.ylabel('Feature Value')
    plt.title('Random Feature Map (RBFSampler)')
    plt.tight_layout()
    plt.show()
    
    return z

# Example usage: Run the module directly and pass the WAV file path as a command-line argument.
if __name__ == '__main__':
    print("hello world")
    features = prepare_wav_file("ml_research/random_feature_map/blues.00000.wav")
    print("Random feature map vector:", features)