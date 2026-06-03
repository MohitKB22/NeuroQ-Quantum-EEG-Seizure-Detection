"""
EEG Signal Processing Module
Advanced preprocessing, feature extraction, and frequency band analysis
"""

import numpy as np
from scipy import signal
from scipy.stats import skew, kurtosis
import random
import time


class EEGProcessor:
    """
    Advanced EEG Signal Processor
    Handles synthetic data generation, signal processing, and feature extraction
    """
    
    # Standard 10-20 EEG electrode positions
    CHANNELS = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4',
                'O1', 'O2', 'F7', 'F8', 'T3', 'T4', 'T5', 'T6', 'Fz', 'Cz', 'Pz']
    
    # Frequency bands (Hz)
    BANDS = {
        'Delta': (0.5, 4),
        'Theta': (4, 8),
        'Alpha': (8, 13),
        'Beta': (13, 30),
        'Gamma': (30, 80)
    }
    
    SAMPLING_RATE = 256  # Hz
    DURATION = 10        # seconds
    
    def __init__(self):
        self.n_channels = len(self.CHANNELS)
        self.n_samples = self.SAMPLING_RATE * self.DURATION
        self.time_axis = np.linspace(0, self.DURATION, self.n_samples)
    
    def generate_synthetic_eeg(self, seizure_type='normal'):
        """
        Generate realistic synthetic EEG data
        
        Parameters:
            seizure_type: 'normal', 'focal', 'generalized', 'absence', 'random'
        
        Returns:
            numpy array of shape (n_channels, n_samples)
        """
        if seizure_type == 'random':
            seizure_type = random.choice(['normal', 'normal', 'focal', 'generalized', 'absence'])
        
        eeg = np.zeros((self.n_channels, self.n_samples))
        t = self.time_axis
        
        for i in range(self.n_channels):
            # Base brain activity: alpha-dominant for normal EEG
            base = (
                3.5 * np.sin(2 * np.pi * 10 * t + np.random.uniform(0, 2*np.pi)) +  # Alpha (dominant)
                1.2 * np.sin(2 * np.pi * 11 * t + np.random.uniform(0, 2*np.pi)) +  # Alpha harmonic
                0.6 * np.sin(2 * np.pi * 20 * t + np.random.uniform(0, 2*np.pi)) +  # Beta
                0.3 * np.sin(2 * np.pi * 2  * t + np.random.uniform(0, 2*np.pi))    # Delta (minimal)
            )
            
            # Add noise
            noise = np.random.normal(0, 0.3, self.n_samples)
            
            if seizure_type == 'focal':
                # Focal seizure: spike-wave in specific channels
                if i in [4, 5, 16]:  # C3, C4, Cz
                    seizure_activity = self._generate_spike_wave(t, freq=3.0, amplitude=8.0)
                    base += seizure_activity
                    
            elif seizure_type == 'generalized':
                # Generalized tonic-clonic: high amplitude, polyspike
                spike_wave = self._generate_spike_wave(t, freq=2.5, amplitude=6.0)
                fast_activity = 4.0 * np.sin(2 * np.pi * 15 * t) * np.exp(-0.1 * t)
                base += spike_wave + fast_activity + np.random.normal(0, 0.5, self.n_samples)
                
            elif seizure_type == 'absence':
                # Absence seizure: classic 3 Hz spike-wave complex
                spike_wave = self._generate_spike_wave(t, freq=3.0, amplitude=8.0)
                # Suppress background alpha, add strong delta+theta
                delta_comp = 4.0 * np.sin(2 * np.pi * 3.0 * t + np.random.uniform(0, 2*np.pi))
                theta_comp = 3.0 * np.sin(2 * np.pi * 6.0 * t + np.random.uniform(0, 2*np.pi))
                base = spike_wave + delta_comp + theta_comp  # Fully replace background
                
            eeg[i] = base + noise
        
        return eeg
    
    def _generate_spike_wave(self, t, freq=3.0, amplitude=5.0):
        """Generate spike-wave complex pattern"""
        spike_wave = amplitude * np.sin(2 * np.pi * freq * t)
        
        # Add sharp spikes
        for spike_time in np.arange(0, self.DURATION, 1/freq):
            spike_idx = int(spike_time * self.SAMPLING_RATE)
            if spike_idx < self.n_samples - 20:
                spike = np.zeros(self.n_samples)
                spike_shape = np.exp(-np.linspace(0, 5, 20)) * amplitude * 2
                spike[spike_idx:spike_idx+20] = spike_shape
                spike_wave += spike
        
        return spike_wave
    
    def process_eeg(self, raw_eeg):
        """
        Full EEG preprocessing pipeline
        
        Steps:
        1. Bandpass filtering (0.5 - 80 Hz)
        2. Notch filtering (50 Hz power line)
        3. Artifact removal
        4. Common average referencing
        """
        processed = raw_eeg.copy()
        
        # 1. Bandpass filter
        b, a = signal.butter(4, [0.5, 80], btype='bandpass', fs=self.SAMPLING_RATE)
        for i in range(processed.shape[0]):
            processed[i] = signal.filtfilt(b, a, processed[i])
        
        # 2. Notch filter (50 Hz)
        b_notch, a_notch = signal.iirnotch(50, 30, fs=self.SAMPLING_RATE)
        for i in range(processed.shape[0]):
            processed[i] = signal.filtfilt(b_notch, a_notch, processed[i])
        
        # 3. Common Average Reference (CAR)
        car = np.mean(processed, axis=0)
        processed -= car
        
        # 4. Normalize
        processed = processed / (np.std(processed) + 1e-8)
        
        return {
            'channels': processed,
            'time_axis': self.time_axis,
            'channel_names': self.CHANNELS,
            'sampling_rate': self.SAMPLING_RATE
        }
    
    def extract_features(self, processed_data):
        """
        Extract comprehensive features from processed EEG
        
        Returns:
            Dictionary of features for classification
        """
        channels = processed_data['channels']
        
        # --- Frequency Band Powers ---
        band_powers = {}
        spectral_data = {'freqs': [], 'psd_mean': []}
        
        for band_name, (low, high) in self.BANDS.items():
            band_power_per_channel = []
            for ch in range(channels.shape[0]):
                freqs, psd = signal.welch(channels[ch], fs=self.SAMPLING_RATE, nperseg=256)
                band_mask = (freqs >= low) & (freqs <= high)
                band_power_per_channel.append(float(np.mean(psd[band_mask])))
            band_powers[band_name] = band_power_per_channel
        
        # Mean band powers for display
        band_powers_mean = {k: float(np.mean(v)) for k, v in band_powers.items()}
        
        # Spectral data for plotting
        freqs, psd_all = signal.welch(channels[0], fs=self.SAMPLING_RATE, nperseg=256)
        mask = freqs <= 80
        spectral_data = {
            'freqs': freqs[mask].tolist(),
            'psd': psd_all[mask].tolist()
        }
        
        # --- Statistical Features ---
        stats_features = {}
        for i, ch_name in enumerate(self.CHANNELS):
            ch_data = channels[i]
            stats_features[ch_name] = {
                'mean': float(np.mean(ch_data)),
                'std': float(np.std(ch_data)),
                'skewness': float(skew(ch_data)),
                'kurtosis': float(kurtosis(ch_data)),
                'rms': float(np.sqrt(np.mean(ch_data**2))),
                'zero_crossings': int(np.sum(np.diff(np.sign(ch_data)) != 0))
            }
        
        # --- Topographic Map (19-channel interpolated values) ---
        topographic_map = self._compute_topographic_map(channels, band_powers)
        
        # --- Hjorth Parameters ---
        hjorth = self._compute_hjorth_parameters(channels)
        
        # --- Connectivity Features ---
        connectivity = self._compute_coherence(channels)
        
        # --- Seizure Index ---
        seizure_index = self._compute_seizure_index(band_powers_mean)
        
        return {
            'frequency_bands': list(self.BANDS.keys()),
            'band_powers': band_powers_mean,
            'band_powers_per_channel': band_powers,
            'statistical_features': stats_features,
            'topographic_map': topographic_map,
            'hjorth': hjorth,
            'connectivity': connectivity,
            'spectral_data': spectral_data,
            'seizure_index': seizure_index,
            'raw_channels': channels
        }
    
    def _compute_topographic_map(self, channels, band_powers):
        """Compute 2D topographic brain map values"""
        # Standard 10-20 positions (normalized to -1 to 1)
        positions = {
            'Fp1': (-0.25, 0.9), 'Fp2': (0.25, 0.9),
            'F7': (-0.7, 0.6), 'F3': (-0.4, 0.6), 'Fz': (0.0, 0.65),
            'F4': (0.4, 0.6), 'F8': (0.7, 0.6),
            'T3': (-0.9, 0.0), 'C3': (-0.5, 0.0), 'Cz': (0.0, 0.0),
            'C4': (0.5, 0.0), 'T4': (0.9, 0.0),
            'T5': (-0.7, -0.6), 'P3': (-0.4, -0.6), 'Pz': (0.0, -0.65),
            'P4': (0.4, -0.6), 'T6': (0.7, -0.6),
            'O1': (-0.25, -0.9), 'O2': (0.25, -0.9)
        }
        
        topo = []
        for ch_name, pos in positions.items():
            if ch_name in self.CHANNELS:
                idx = self.CHANNELS.index(ch_name)
                # Use beta + gamma power as "activity"
                beta_key = 'Beta'
                gamma_key = 'Gamma'
                activity = (
                    band_powers[beta_key][idx] * 0.5 +
                    band_powers[gamma_key][idx] * 0.5
                ) if idx < len(band_powers[beta_key]) else 0
                
                topo.append({
                    'channel': ch_name,
                    'x': pos[0],
                    'y': pos[1],
                    'value': float(activity)
                })
        
        return topo
    
    def _compute_hjorth_parameters(self, channels):
        """Compute Hjorth parameters: Activity, Mobility, Complexity"""
        hjorth = {}
        for i, ch_name in enumerate(self.CHANNELS):
            ch = channels[i]
            d1 = np.diff(ch)
            d2 = np.diff(d1)
            
            activity = float(np.var(ch))
            mobility = float(np.sqrt(np.var(d1) / (np.var(ch) + 1e-8)))
            complexity = float(np.sqrt(np.var(d2) / (np.var(d1) + 1e-8)) / (mobility + 1e-8))
            
            hjorth[ch_name] = {
                'activity': activity,
                'mobility': mobility,
                'complexity': complexity
            }
        return hjorth
    
    def _compute_coherence(self, channels, pairs=None):
        """Compute inter-channel coherence for key pairs"""
        if pairs is None:
            pairs = [
                ('F3', 'F4'), ('C3', 'C4'), ('P3', 'P4'),
                ('Fp1', 'Fp2'), ('O1', 'O2'), ('T3', 'T4')
            ]
        
        coherence = {}
        for ch1, ch2 in pairs:
            if ch1 in self.CHANNELS and ch2 in self.CHANNELS:
                idx1 = self.CHANNELS.index(ch1)
                idx2 = self.CHANNELS.index(ch2)
                
                f, Cxy = signal.coherence(channels[idx1], channels[idx2], 
                                          fs=self.SAMPLING_RATE, nperseg=128)
                coherence[f'{ch1}-{ch2}'] = float(np.mean(Cxy))
        
        return coherence
    
    def _compute_seizure_index(self, band_powers_mean):
        """
        Compute custom seizure index from band power ratios
        High delta+theta relative to alpha+beta suggests seizure activity
        """
        delta = band_powers_mean.get('Delta', 0)
        theta = band_powers_mean.get('Theta', 0)
        alpha = band_powers_mean.get('Alpha', 0)
        beta = band_powers_mean.get('Beta', 0)
        gamma = band_powers_mean.get('Gamma', 0)
        
        total = delta + theta + alpha + beta + gamma + 1e-8
        
        # Seizure index: high when delta+theta+gamma dominate over alpha+beta
        # Absence: delta+theta high; Focal/Gen: gamma+delta high
        epileptic_power = delta + theta + gamma
        background_power = alpha + beta + 1e-8
        # Normalize to 0-1 range using ratio
        ratio = epileptic_power / (epileptic_power + background_power)
        seizure_index = float(np.clip(ratio, 0.0, 1.0))
        return seizure_index
