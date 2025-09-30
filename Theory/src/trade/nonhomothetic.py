"""Stone–Geary (non-homothetic) demand system utilities."""

from __future__ import annotations

import numpy as np

_EPS = 1e-12


def sg_expenditure(p, u, alpha, gamma):
    """Stone–Geary expenditure function ``e(p, u)``."""

    u_arr = np.asarray(u, dtype=float).reshape(-1)
    p_b, alpha_b, gamma_b = _broadcast_params(p, alpha, gamma, households=u_arr.size)
    if u_arr.size == 1:
        u_arr = np.repeat(u_arr, p_b.shape[0])

    log_term = np.sum(alpha_b * (np.log(p_b + _EPS) - np.log(alpha_b + _EPS)), axis=1)
    price_index = np.exp(log_term)
    subsistence = np.sum(p_b * gamma_b, axis=1)
    return subsistence + u_arr * price_index


def sg_demands(y, p, alpha, gamma):
    """Household demands under Stone–Geary preferences."""

    y_arr = np.asarray(y, dtype=float).reshape(-1)
    p_b, alpha_b, gamma_b = _broadcast_params(p, alpha, gamma, households=y_arr.size)
    if y_arr.size == 1:
        y_arr = np.repeat(y_arr, p_b.shape[0])

    subsistence_cost = np.sum(p_b * gamma_b, axis=1)
    residual = np.maximum(y_arr - subsistence_cost, 0.0)
    scaled = (residual[:, None] * alpha_b) / (p_b + _EPS)
    return gamma_b + scaled


def welfare_ev_ratio(y0, p0, p1, alpha, gamma):
    """Equivalent-variation income ratio for households ``y0`` under price change ``p1``."""

    y0_arr = np.asarray(y0, dtype=float).reshape(-1)
    q0 = sg_demands(y0_arr, p0, alpha, gamma)
    p0_b, alpha_b, gamma_b = _broadcast_params(p0, alpha, gamma, households=q0.shape[0])
    util = np.prod(np.maximum(q0 - gamma_b, _EPS) ** alpha_b, axis=1)
    exp_new = sg_expenditure(p1, util, alpha, gamma)
    if y0_arr.size == 1:
        y0_arr = np.repeat(y0_arr, exp_new.shape[0])
    return exp_new / y0_arr


def check_luxury_share(y_grid, p, alpha, gamma, good_index=1):
    """Monotonicity check: expenditure share of ``good_index`` rises with income."""

    demands = sg_demands(y_grid, p, alpha, gamma)
    total_exp = np.sum(demands * np.asarray(p, dtype=float), axis=1)
    share = (demands[:, good_index] * p[good_index]) / np.maximum(total_exp, _EPS)
    return np.all(np.diff(share) >= -1e-12)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _broadcast_params(p, alpha, gamma, households=None):
    p_arr = np.asarray(p, dtype=float)
    if p_arr.ndim == 1:
        p_arr = p_arr.reshape(1, -1)
    alpha_arr = np.asarray(alpha, dtype=float)
    if alpha_arr.ndim == 1:
        alpha_arr = alpha_arr.reshape(1, -1)
    gamma_arr = np.asarray(gamma, dtype=float)
    if gamma_arr.ndim == 1:
        gamma_arr = gamma_arr.reshape(1, -1)

    K = p_arr.shape[1]
    if alpha_arr.shape[1] != K or gamma_arr.shape[1] != K:
        raise ValueError("Prices, alpha, and gamma must share the same number of goods.")

    rows = [p_arr.shape[0], alpha_arr.shape[0], gamma_arr.shape[0]]
    target = max(rows)
    if households is not None:
        target = max(target, households)

    def _repeat_if_needed(arr):
        if arr.shape[0] == target:
            return arr
        if arr.shape[0] == 1:
            return np.repeat(arr, target, axis=0)
        raise ValueError("Cannot broadcast Stone–Geary parameters to common household count.")

    p_arr = _repeat_if_needed(p_arr)
    alpha_arr = _repeat_if_needed(alpha_arr)
    gamma_arr = _repeat_if_needed(gamma_arr)

    row_sums = alpha_arr.sum(axis=1, keepdims=True)
    row_sums[row_sums <= 0] = 1.0
    alpha_arr = alpha_arr / row_sums

    return p_arr, alpha_arr, gamma_arr
