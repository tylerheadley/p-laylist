#!/usr/bin/env python3
"""
knn_lookup.py: Given a JSON dataset of projected audio features,
find the K nearest neighbours to a query WAV file using hard-coded paths.
"""

import json
import numpy as np
import os

# Make sure this file is in the same directory (or on PYTHONPATH) as rfm_iterate_folder.py
from rfm_iterate_folder import (
    extract_mfcc_features,
    extract_chroma_features,
    extract_spectrogram,
    extract_tempogram,
    extract_rhythm,
    random_feature_map,
)

# ─── USER CONFIG ───────────────────────────────────────────────────────────────
DATASET_PATH = "song_vectors_dataset.json"           # path to your JSON feature dump
QUERY_PATH   = "genres_original/blues/blues.00000.wav"      # path to the WAV file you want to search
K            = 3                        # how many neighbours to print
# ────────────────────────────────────────────────────────────────────────────────

def load_dataset(json_path):
    """Load list of feature records from JSON."""
    with open(json_path, 'r') as f:
        return json.load(f)

def compute_projected_features(wav_path, target_dim, random_state=42):
    """
    Extract and project all five feature types from a single WAV file
    into a concatenated vector of length 5 * target_dim.
    """
    mfcc   = extract_mfcc_features(wav_path, n_mfcc=16)
    mfcc_p = random_feature_map(mfcc, target_dim=target_dim, random_state=random_state)

    chroma   = extract_chroma_features(wav_path, n_chroma=12)
    chroma_p = random_feature_map(chroma, target_dim=target_dim, random_state=random_state)

    spec       = extract_spectrogram(wav_path, n_fft=2048, hop_length=1024)
    spec_flat  = spec.flatten()
    spec_p     = random_feature_map(spec_flat, target_dim=target_dim, random_state=random_state)

    tempo       = extract_tempogram(wav_path, hop_length=512)
    tempo_flat  = tempo.flatten()
    tempo_p     = random_feature_map(tempo_flat, target_dim=target_dim, random_state=random_state)

    rhythm       = extract_rhythm(wav_path, hop_length=512)
    rhythm_flat  = rhythm.flatten()
    rhythm_p     = random_feature_map(rhythm_flat, target_dim=target_dim, random_state=random_state)

    return np.concatenate([mfcc_p, chroma_p, spec_p, tempo_p, rhythm_p])

def main():
    # Load dataset
    data = load_dataset(DATASET_PATH)
    if not data:
        print("❗ Dataset is empty.")
        return

    # Determine projection size
    target_dim = len(data[0]['mfcc'])

    # Project query file
    try:
        query_vec = compute_projected_features(QUERY_PATH, target_dim)
    except Exception as e:
        print(f"❗ Error processing query file: {e}")
        return

    # Compute distances
    neighbours = []
    for entry in data:
        vec = np.concatenate([
            np.array(entry['mfcc']),
            np.array(entry['chroma']),
            np.array(entry['spectrogram']),
            np.array(entry['tempogram']),
            np.array(entry['spectral_rhythm']),
        ])
        dist = np.linalg.norm(vec - query_vec)
        neighbours.append((entry['file_path'], dist))

    # Sort & print top-K
    neighbours.sort(key=lambda x: x[1])
    top_k = neighbours[:K]

    print(f"\nTop {K} nearest neighbours to {QUERY_PATH}:\n")
    for i, (path, d) in enumerate(top_k, 1):
        print(f"{i}. {path}  (distance = {d:.4f})")

if __name__ == "__main__":
    main()