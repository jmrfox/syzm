import numpy as np


class RestrictedBoltzmannMachine:
    def __init__(self, n_visible, n_hidden, learning_rate=0.1):
        """
        Initialize the RBM with the given number of visible and hidden units.
        :param n_visible: Number of visible units
        :param n_hidden: Number of hidden units
        :param learning_rate: Learning rate for training
        """
        self.n_visible = n_visible
        self.n_hidden = n_hidden
        self.learning_rate = learning_rate

        # Initialize weights and biases
        self.weights = np.random.normal(0, 0.1, (n_visible, n_hidden))  # Weight matrix
        self.visible_bias = np.zeros(n_visible)  # Bias for visible units
        self.hidden_bias = np.zeros(n_hidden)  # Bias for hidden units

    def sigmoid(self, x):
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-x))

    def sample_hidden(self, visible):
        """Sample hidden units given visible units."""
        activation = np.dot(visible, self.weights) + self.hidden_bias
        probabilities = self.sigmoid(activation)
        return probabilities, np.random.binomial(1, probabilities)

    def sample_visible(self, hidden):
        """Sample visible units given hidden units."""
        activation = np.dot(hidden, self.weights.T) + self.visible_bias
        probabilities = self.sigmoid(activation)
        return probabilities, np.random.binomial(1, probabilities)

    def contrastive_divergence(self, data, k=1):
        """
        Perform Contrastive Divergence (CD-k) to update weights and biases.
        :param data: Input data (batch of visible units)
        :param k: Number of Gibbs sampling steps
        """
        # Positive phase
        pos_hidden_probs, pos_hidden_states = self.sample_hidden(data)
        pos_associations = np.dot(data.T, pos_hidden_probs)

        # Negative phase
        visible = data
        for _ in range(k):
            hidden_probs, hidden_states = self.sample_hidden(visible)
            visible_probs, visible_states = self.sample_visible(hidden_states)
            visible = visible_states

        neg_hidden_probs, _ = self.sample_hidden(visible)
        neg_associations = np.dot(visible.T, neg_hidden_probs)

        # Update weights and biases
        self.weights += self.learning_rate * (pos_associations - neg_associations) / data.shape[0]
        self.visible_bias += self.learning_rate * np.mean(data - visible, axis=0)
        self.hidden_bias += self.learning_rate * np.mean(pos_hidden_probs - neg_hidden_probs, axis=0)

    def reconstruct(self, data):
        """
        Reconstruct visible units from input data.
        :param data: Input data (batch of visible units)
        :return: Reconstructed visible units
        """
        hidden_probs, _ = self.sample_hidden(data)
        visible_probs, _ = self.sample_visible(hidden_probs)
        return visible_probs
