import numpy as np
import os

def truncate_spectrograms(spectrogram1, spectrogram2):
    """
    Truncate two spectrograms along the time (column) dimension to match their shapes.
    The shorter number of columns will be used as the target length.

    Parameters:
    spectrogram1 (np.ndarray): First spectrogram.
    spectrogram2 (np.ndarray): Second spectrogram.

    Returns:
    tuple: Truncated spectrograms (truncated1, truncated2).
    """
    min_time_dim = min(spectrogram1.shape[1], spectrogram2.shape[1])
    truncated1 = spectrogram1[:, :min_time_dim]
    truncated2 = spectrogram2[:, :min_time_dim]
    return truncated1, truncated2

def rank_spectrogram_similarity(input_file, dataset_folder):
    """
    Ranks the similarity of spectrograms in a folder compared to a given input file
    based on the Frobenius norm.

    Parameters:
    input_file (str): Path to the input .npy file.
    dataset_folder (str): Path to the folder containing .npy spectrogram files.

    Returns:
    list: A sorted list of tuples (filename, Frobenius norm) in ascending order of similarity.
    """
    # Load the input spectrogram
    input_spectrogram = np.load(input_file)

    # Initialize a list to store the similarity scores
    similarity_scores = []

    # Iterate through all .npy files in the dataset folder
    for file_name in os.listdir(dataset_folder):
        file_path = os.path.join(dataset_folder, file_name)

        # # Skip the input file itself
        # if file_path == input_file:
        #     continue

        # Check if the file is an .npy file
        if file_name.endswith('.npy'):
            # Load the current spectrogram
            spectrogram = np.load(file_path)

            # Truncate the spectrograms to match their size
            truncated_input, truncated_spectrogram = truncate_spectrograms(input_spectrogram, spectrogram)

            # Compute the Frobenius norm (similarity measure)
            frobenius_norm = np.linalg.norm(truncated_input - truncated_spectrogram, ord='fro')

            # Append the file name and similarity score to the list
            similarity_scores.append((file_name, frobenius_norm))

    # Sort the list by similarity scores in ascending order
    similarity_scores.sort(key=lambda x: x[1])

    return similarity_scores


# Example usage
if __name__ == "__main__":
    # Specify the path to the input file and dataset folder
    input_file = "test_dataset/similar_songs/song_1.npy"
    dataset_folder = "test_dataset/similar_songs"

    # Rank the similarities
    ranked_similarities = rank_spectrogram_similarity(input_file, dataset_folder)

    # Display the results
    print("Ranked Similarities (file, Frobenius norm):")
    for file_name, norm in ranked_similarities:
        print(f"{file_name}: {norm:.4f}")