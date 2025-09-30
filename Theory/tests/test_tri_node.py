import numpy as np

from src.trade.tri_node import ces_gravity, tri_node_welfare, tri_node_welfare_sever

def test_reroute_bounds():
    productivities = np.array([1.0, 1.0, 0.1])
    taus = np.array([[1.0, 1.2, 2.0], [1.2, 1.0, 2.0], [2.0, 2.0, 1.0]])
    epsilon = 4.0
    alpha_k = np.array([1.0])
    epsilon_k = np.array([epsilon])

    Pi0 = ces_gravity(productivities, taus, epsilon)

    # Check kappa=0
    w_reroute_0, _ = tri_node_welfare(alpha_k, epsilon_k, Pi0, taus, 0.0, productivities)
    assert np.allclose(w_reroute_0, 1.0)

    # Check reroute vs sever
    kappas = np.linspace(0, 1, 5)
    for kappa in kappas:
        w_reroute, _ = tri_node_welfare(alpha_k, epsilon_k, Pi0, taus, kappa, productivities)
        w_sever = tri_node_welfare_sever(alpha_k, epsilon_k, Pi0)
        assert np.all(w_reroute >= w_sever - 1e-8)