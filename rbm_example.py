import numpy as np
import os
from models import RestrictedBoltzmannMachine
import bindata as bd
import matplotlib.pyplot as plt

# set seed
np.random.seed(1)


def random_covariance_matrix(n):
    # generate two random vectors and compute their covariance
    samples = np.random.randn(2, n)
    covariance_matrix = np.cov(samples, rowvar=False)
    return covariance_matrix


def gaussian_copula(n_samples, n_features, covariance_matrix, thresholds=None):
    """
    Generate correlated binary data using a Gaussian copula.
    :param n_samples: Number of samples to generate
    :param n_features: Number of binary features
    :param correlation_matrix: Correlation matrix (n_features x n_features)
    :param thresholds: Thresholds for binarization (default: 0 for all features)
    :return: Correlated binary data (n_samples x n_features)
    """
    # Step 1: Generate multivariate Gaussian data
    mean = np.zeros(n_features)
    gaussian_data = np.random.multivariate_normal(mean, covariance_matrix, size=n_samples)

    # Step 2: Apply thresholds to convert to binary data
    if thresholds is None:
        thresholds = np.zeros(n_features)  # Default threshold is 0
    binary_data = (gaussian_data > thresholds).astype(int)

    return binary_data


n_train = 1000  # Number of training samples
n_visible = 6  # Number of visible units
n_hidden = 3  # Number of hidden units
epochs = 20000
learning_rate = 0.01

covariance_matrix = random_covariance_matrix(n_visible)
thresholds = np.random.rand(n_visible)
print("Correlation Matrix:\n", covariance_matrix)
print("Thresholds:\n", thresholds)

sample_data = lambda n_samples: gaussian_copula(n_samples, n_visible, covariance_matrix, thresholds=thresholds)

training_data = sample_data(n_train)

# Initialize the RBM
rbm = RestrictedBoltzmannMachine(n_visible, n_hidden, learning_rate)

# Train the RBM using Contrastive Divergence
input("Press Enter to start training...")
for epoch in range(epochs):
    rbm.contrastive_divergence(training_data, k=1)  # CD-1
    # Calculate reconstruction error for monitoring
    reconstructed_data = rbm.reconstruct(training_data)
    error = np.mean((training_data - reconstructed_data) ** 2)
    print(f"Epoch {epoch + 1}/{epochs}, Reconstruction Error: {error:.4f}")

# Test the RBM by reconstructing some data
n_test = 5  # Number of test samples
test_data = sample_data(n_test)
print("\nOriginal Test Data:")
print(test_data)

reconstructed_test_data = rbm.reconstruct(test_data)
print("\nReconstructed Test Data:")
print(np.round(reconstructed_test_data, 2))  # Round for better readability

# plot test and reconstruction side by side
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Original Test Data")
plt.imshow(test_data, cmap="gray", aspect="auto")
plt.colorbar()
plt.subplot(1, 2, 2)
plt.title("Reconstructed Test Data")
plt.imshow(reconstructed_test_data, cmap="gray", aspect="auto")
plt.colorbar()
plt.show()
