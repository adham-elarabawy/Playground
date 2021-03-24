import numpy as np
def masking_noise(X, v):
    """ Apply masking noise to data in X, in other words a fraction v of elements of X
    (chosen at random) is forced to zero.
    X is of size [batch_size, features]
    """

    X_noise = X.clone().detach()
    n_samples = X.shape[0]
    n_features = X.shape[1]

    for i in range(n_samples):
        mask = np.random.choice(n_features, (int) (v * n_features))
        for m in mask:
            X_noise[i][m] = 0.
    return X_noise
