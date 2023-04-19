import time
import numpy as np
from collections import defaultdict
from sklearn.mixture import GaussianMixture
from sklearn.metrics import adjusted_rand_score
from sklearn.cluster import KMeans, SpectralClustering, \
    AffinityPropagation, DBSCAN, AgglomerativeClustering


class ClusteringEstimators:

    def __init__(self, algorithm_name, n_clusters, n_init):

        self.estimator = None
        self.algorithm_name = algorithm_name.lower()
        self.n_clusters = n_clusters
        self.n_init = n_init

        self.ari = None
        self.inertia = None
        self.clusters = None
        self.centroids = list()
        self.data_scatter = None

    @staticmethod
    def compute_data_scatter(m):
        return np.sum(np.power(m, 2))

    def compute_inertia(self, m, ):
        return sum(
            [np.sum(np.power(m[np.where(self.clusters == k)] - self.centroids[k], 2)) for k in range(self.n_clusters)]
        )

    def instantiate_estimator_with_parameters(self, ):

        # Methods based on given n_clusters:
        # K-Means:
        if self.algorithm_name == "km_clu":
            self.estimator = KMeans(
                n_clusters=self.n_clusters,
                init="random", max_iter=100, n_init=self.n_init,
            )
            print(
                "Instantiate K-Means Clustering."
            )

        # Gaussian Mixture:
        elif self.algorithm_name == "gm_clu":
            self.estimator = GaussianMixture(
                n_components=self.n_clusters,
                covariance_type="full",
                init_params="random",
            )
            print(
                "Instantiate Gaussian Mixture Clustering."
            )

        # Spectral (no predict() method to tune hyperparams):
        elif self.algorithm_name == "s_clu":
            self.estimator = SpectralClustering(
                n_clusters=self.n_clusters,
                n_init=self.n_init, gamma=1.0, affinity="rbf",
            )
            print(
                "Instantiate Spectral Clustering."
            )

        # Agglomerative (no predict() method to tune hyperparams):
        elif self.algorithm_name == "a_clu":
            self.estimator = AgglomerativeClustering(
                n_clusters=self.n_clusters,
                affinity="l2", linkage="average",
            )
            print(
                "Instantiate Agglomerative Clustering."
            )

        # Methods based on automatic determination of n_clusters:
        # DBSCAN (no predict() method to tune hyperparams):
        elif self.algorithm_name == "dbs_clu":
            self.estimator = DBSCAN(
                eps=5e-1, min_samples=5, p=2,
            )
            print(
                "Instantiate DBSCAN Clustering."
            )
        else:
            assert False, "Undefined clustering model."

        return self.estimator

    def fit_estimator(self, x, y):

        print(
            "Fitting and testing of " + self.algorithm_name
        )

        self.clusters = self.estimator.fit_predict(x, y)
        self.centroids = [x[np.where(self.clusters == k)].mean(axis=0) for k in range(self.n_clusters)]
        self.centroids = np.asarray(self.centroids)
        self.inertia = self.compute_inertia(m=x)
        self.data_scatter = self.compute_data_scatter(m=x)
        if y is not None:
            self.ari = adjusted_rand_score(y, self.clusters)
        print(
            f"\n ARI = {self.ari:.3f} Inertia = {self.inertia:.3f} \n"
        )
        return self.clusters




