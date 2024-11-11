import numpy as np
import librosa, librosa.display
import matplotlib.pyplot as plt
import json
import kagglehub

# Download latest version
path = kagglehub.dataset_download("andradaolteanu/gtzan-dataset-music-genre-classification")

print("Path to dataset files:", path)

# You probably need to install ffmpeg (brew install ffmpeg on mac) to load .mp3 files
# For the random samples, I'm using the gtzan/marysas genre dataset https://huggingface.co/datasets/marsyas/gtzan
# TODO: load in gtzan dataset and complete the random samples dataset.

FIG_SIZE = (15,10)

song_id = {2, 3, 4, 5}

for id in song_id:
    file = f"test_songs/song_{id}.mp3" # path to the song to convert to spectrogram
    npy_path = f"test_dataset/song_{id}.npy" # path to save the .npy nparray spectrogram
    # load audio file with Librosa
    signal, sample_rate = librosa.load(file, sr=8000)

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
    plt.show()


