import numpy as np
import librosa, librosa.display
import matplotlib.pyplot as plt
import json
import os

# You probably need to install ffmpeg (brew install ffmpeg on mac) to load .mp3 files
# For the random samples, I'm using the gtzan/marysas genre dataset https://huggingface.co/datasets/marsyas/gtzan
# TODO: load in gtzan dataset and complete the random samples dataset.

FIG_SIZE = (15,10)

# song_id = {2, 3, 4, 5}

# Path to the GTZAN dataset
dataset_path = 'test_songs/random_songs/'

# Iterate through each genre folder
for genre in os.listdir(dataset_path):
    genre_path = os.path.join(dataset_path, genre)
    
    # Check if it's a directory
    if os.path.isdir(genre_path):
        print(f"Processing genre: {genre}")
        
        # Iterate through each audio file in the genre folder
        for filename in os.listdir(genre_path):
            if filename.endswith('.wav'):  # Check if the file is a .wav file
                file_path = os.path.join(genre_path, filename)
                npy_path = f"test_dataset/random_songs/{filename}"
                
                # Load the audio file using librosa
                signal, sample_rate = librosa.load(file_path, sr=8000)
                
                # Process the audio as needed
                print(f"Loaded {filename} from {genre} with sample rate {sample_rate}")
                
                # (Optional) Perform operations like extracting features, etc.
                # e.g., mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)

                # STFT -> spectrogram
                hop_length = 512 # in num. of samples
                n_fft = 2048 # window in num. of samples

                # calculate duration hop length and window in seconds
                hop_length_duration = float(hop_length)/sample_rate
                n_fft_duration = float(n_fft)/sample_rate

                # perform stft
                stft = librosa.stft(signal, n_fft=n_fft, hop_length=hop_length)

                # calculate abs values on complex numbers to get magnitude
                spectrogram = np.abs(stft)

                # apply logarithm to cast amplitude to Decibels
                log_spectrogram = librosa.amplitude_to_db(spectrogram) # returns numpy array

                # Save as numpy .npy
                np.save(npy_path,log_spectrogram)

                # # MFCCs
                # # extract 13 MFCCs
                # MFCCs = librosa.feature.mfcc(signal, sample_rate, n_fft=n_fft, hop_length=hop_length, n_mfcc=13)

                # show plots
                # plt.show()
