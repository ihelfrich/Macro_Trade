# Theory Module Outline

## Environment
- **Agents**: Set of regions $\mathcal{R}$ (size $R$) and sectors $\mathcal{S}$; representative households per region with Stone--Geary preferences; competitive firms with intermediate input requirements.
- **Preferences**: Households maximise
  $$
  U_r = \left( \sum_{s \in \mathcal{S}} eta_{rs}^{rac{1}{\sigma_r}} \left( C_{rs} - \gamma_{rs} ight)^{rac{\sigma_r - 1}{\sigma_r}} ight)^{rac{\sigma_r}{\sigma_r - 1}},
  $$
  with Armington composite $C_{rs}$ across origins governed by elasticity $	heta_s$.
- **Armington structure**: Destination $r$ and sector $s$ aggregate origin supplies as
  $$
  C_{rs} = \left( \sum_{o \in \mathcal{R}} lpha_{ors}^{rac{1}{	heta_s}} c_{ors}^{rac{	heta_s-1}{	heta_s}} ight)^{rac{	heta_s}{	heta_s-1}},
  $$
  where $c_{ors}$ is absorption of output from origin $o$.
- **Production**: Firms employ fixed-coefficient IO technology with matrix $A$, value-added share $1-\sum_{s'} A_{s's}$, iceberg costs $	au_{ors}$, and potential capacity ceilings $\kappa_{os}$.
- **Equilibrium**: Prices $p$, value-added vector $v$ satisfy $(I - A(	au)^{	op})p = v$ and market-clearing; assume $ho(A(	au)) < 1$.

## Proposition Statements (draft)
- **Proposition 1 (Reroute weakly dominates Sever)**: Under the above CES/Armington environment with non-binding capacity constraints, welfare under rerouting (allowing reallocations within $\kappa_{os}$) is weakly higher than severing bilateral links. Equality occurs when substitution elasticities or capacities prevent reallocation; provide counterexample when $\kappa$ binds.
- **Proposition 2 (IO amplification bound)**: For small wedges $w$, aggregate welfare obeys $|\Delta \log W| \leq \|\omega\|_1 \cdot \|L\|_{\infty} \cdot \|w\|_{\infty}$ with $L = (I - A^{	op})^{-1}$. The second-order error is bounded by $	frac{1}{2} \kappa(ho(A), arepsilon) \|w\|_2^2$.
- **Proposition 3 (Granular convexity)**: With Stone--Geary demand and small firm-level shocks, the welfare loss as a function of exposure concentration $H = \sum_i s_i^2$ is convex; curvature coefficient depends on luxury-share parameters and elasticities.
- **Baqaee--Farhi error bound**: Establish $|\Delta \log W - \Delta \log W^{(1)}| \leq 	frac{1}{2} \lambda_{\max}(H) \|\Delta \log p\|_2^2$ with $H = L^{	op}\operatorname{diag}(arepsilon)L$.

## Proof Roadmap
1. Formulate capacity-constrained Armington problem; apply CES monotonicity for Proposition 1.
2. Use Neumann series and operator norms to bound amplification and truncation (Proposition 2).
3. Expand welfare to second order in exposure shocks; compute second derivative with respect to the HHI (Proposition 3).
4. Apply matrix norm inequalities (Gershgorin) for FO vs SO bounds.

## Next Steps
- Enumerate assumptions (A1--A6) covering elasticities, capacity feasibility, and regularity.
- Draft appendix proofs using the above roadmap.
- Derive closed-form curvature expressions for quantitative calibration.
