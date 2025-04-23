# A script that loads multiple .npy spectrograms and displays them using matplotlib
import numpy as np
import matplotlib.pyplot as plt

def load_spectrogram(file_path):
    """
    Load a spectrogram from a .npy file.
    :param file_path: Path to the .npy file.
    :return: The spectrogram as a NumPy array.
    """
    try:
        spectrogram = np.load(file_path)
        print(f"Spectrogram loaded successfully. Shape: {spectrogram.shape}")
        return spectrogram
    except Exception as e:
        print(f"Error loading spectrogram from {file_path}: {e}")
        return None

def display_spectrograms(spectrograms, titles=None):
    """
    Display multiple spectrograms using Matplotlib.
    :param spectrograms: A list of spectrogram arrays to display.
    :param titles: A list of titles corresponding to each spectrogram.
    """
    num_spectrograms = len(spectrograms)
    plt.figure(figsize=(15, 5 * num_spectrograms))
    
    for i, spectrogram in enumerate(spectrograms):
        plt.subplot(num_spectrograms, 1, i + 1)
        plt.imshow(spectrogram, aspect='auto', origin='lower', cmap='viridis')
        plt.colorbar(label="Intensity")
        title = titles[i] if titles and i < len(titles) else f"Spectrogram {i + 1}"
        plt.title(title)
        plt.xlabel("Time (frames)")
        plt.ylabel("Frequency (bins)")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Allow user to enter multiple file paths
    file_paths = input("Enter the paths to .npy spectrogram files (comma-separated): ").split(',')
    spectrograms = []
    titles = []

    for file_path in file_paths:
        file_path = file_path.strip()  # Clean up any extra spaces
        spectrogram = load_spectrogram(file_path)
        if spectrogram is not None:
            spectrograms.append(spectrogram)
            titles.append(file_path)  # Use file path as the default title

    if spectrograms:
        display_spectrograms(spectrograms, titles)
    else:
        print("No valid spectrograms to display.")