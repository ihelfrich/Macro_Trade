Fragmented Globalization: Theory and Welfare in a Two-Bloc Trade Model
Model Setup in the ACR Framework

We consider a world economy with a set of countries 
i=1,2,…,N
i=1,2,…,N, partitioned into two trading blocs (say Bloc A and Bloc B). Let 
A
A denote the set of countries in Bloc A and 
B
B those in Bloc B (with 
A∪B={1,…,N}
A∪B={1,…,N} and 
A∩B=∅
A∩B=∅). The model belongs to the Arkolakis–Costinot–Rodríguez-Clare (ACR) class
nber.org
, incorporating the following standard assumptions:

Preferences: Each country 
i
i is populated by a representative agent with CES preferences over a continuum of differentiated varieties (or equivalently, over country-specific goods in an Armington formulation). The agent’s utility is

Ui=(∑j=1N∫v∈Ωj[qij(v)]σ−1σdv)σσ−1,

where 
qij(v)
q
ij
	​

(v) is consumption by country i of variety 
v
v produced in country j, 
Ωj
Ω
j
	​

 is the set (measure) of varieties produced by j, and 
σ>1
σ>1 is the elasticity of substitution across varieties (a constant). This CES demand system yields a constant trade elasticity 
ϵ=σ−1
ϵ=σ−1 for trade flows
nber.org
. Preferences are assumed homothetic (so expenditure shares depend only on prices and total expenditure, not on income level, unless stated otherwise in extensions).

Technology and Endowments: Each country j produces a differentiated good (or continuum of goods) using a single factor (labor) with constant returns to scale. One unit of the numéraire input produces one unit of output (we normalize marginal cost to 1 for simplicity, abstracting from absolute cost differences). Countries may differ in productivity or variety mass, but for now we assume any such differences are reflected in country j’s productivity parameter or mass of varieties 
Tj
T
j
	​

. Under the ACR class assumptions, these differences will affect trade shares but not the functional form of welfare results
nber.org
. Each country is endowed with 
Li
L
i
	​

 units of labor, so its total output/income in equilibrium will be 
Yi=wiLi
Y
i
	​

=w
i
	​

L
i
	​

, with 
wi
w
i
	​

 the wage (price of labor).

Trade Costs: Trade is subject to iceberg costs. For any good shipped from country j to country i, a fraction melts away: delivering 1 unit requires sending 
τij≥1
τ
ij
	​

≥1 units from j. We assume 
τii=1
τ
ii
	​

=1 (no cost in domestic trade). Fragmentation in this model refers to an increase in trade costs specifically between the two blocs. In the initial integrated equilibrium (benchmark of “globalization”), we may have relatively low trade costs worldwide (e.g. 
τij=1
τ
ij
	​

=1 for all i,j, or uniformly low tariffs). The fragmented equilibrium will be characterized by higher cross-bloc trade costs. For analytical tractability, we often consider the extreme case of fragmentation where within each bloc trade remains frictionless (
τij=1
τ
ij
	​

=1 if 
i,j
i,j are in the same bloc) while cross-bloc trade becomes prohibitive (
τij→∞
τ
ij
	​

→∞ if 
i∈A,j∈B
i∈A,j∈B or vice versa). This extreme case yields a two-bloc autarky scenario, illuminating the maximal impacts of fragmentation. Later, we will also analyze small or finite increases in 
τij
τ
ij
	​

 between blocs.

Market Structure: We assume either perfect competition or monopolistic competition with a large number of firms in each country. Under our assumptions (CES demand, constant marginal cost, Dixit-Stiglitz love-of-variety), the market structure does not affect the aggregate trade flow equations or welfare formulas
nber.org
. Prices will equal marginal costs (times markup 1 under perfect competition, or a constant markup under monopolistic competition), which we normalize so that the factory-gate price of one unit from j is 
cj=1
c
j
	​

=1. Thus delivered price to i from j is 
pij=τijcj=τij
p
ij
	​

=τ
ij
	​

c
j
	​

=τ
ij
	​

. All income 
Yi
Y
i
	​

 is distributed to the representative consumer in i.

Trade Imbalances: We allow for the possibility of trade imbalances. Let 
Ei
E
i
	​

 denote country i’s total expenditure (absorption). We write

Ei=Yi+Fi,
E
i
	​

=Y
i
	​

+F
i
	​

,

where 
Fi
F
i
	​

 is a net transfer or imbalance term (if 
Fi<0
F
i
	​

<0, country i runs a trade deficit financed by an inflow of goods or borrowing; if 
Fi>0
F
i
	​

>0, i runs a surplus or net outflow). These transfers are assumed exogenous and fixed in nominal terms for the comparative statics we consider (we later discuss how endogenously adjusting imbalances would affect welfare). By world clearing, 
∑iFi=0
∑
i
	​

F
i
	​

=0. Balanced trade is the special case 
Fi=0
F
i
	​

=0 for all i, in which 
Ei=Yi
E
i
	​

=Y
i
	​

. Our main theoretical results will first assume balanced trade; we then generalize to 
Fi≠0
F
i
	​


=0.

Demand and Multilateral Resistance

Given CES preferences and prices, country i’s ideal price index (unit-cost of utility) is:

Pi  =  (∑j=1N∫v∈Ωj[pij(v)]1−σdv)1/(1−σ).

Under the constant marginal cost and iceberg cost assumptions, all varieties from country j have identical delivered cost 
τij
τ
ij
	​

. If country j offers a mass 
Tj
T
j
	​

 of varieties (or an equivalent productivity index in a continuum Ricardian model), we can simplify the price index to:

Pi  =  (∑j=1NTj[τijcj] 1−σ)1/(1−σ).

This formulation yields a structural gravity equation for trade shares. Let 
Xij
X
ij
	​

 be the value of imports by country i from country j. Using standard expenditure minimization and the CES demand, we have:

Xij=Tj[τijcj] 1−σ∑k=1NTk[τikck] 1−σ  Ei.

In words, 
Xij
X
ij
	​

 equals i’s total expenditure 
Ei
E
i
	​

 times the fraction of varieties (adjusted for prices) that i sources from j. Define 
πij=XijEi
π
ij
	​

=
E
i
	​

X
ij
	​

	​

 as the expenditure share of country i on goods from j. Then:

πij  =  Tj(τijcj) 1−σ∑k=1NTk(τikck) 1−σ .

Equivalently, trade shares satisfy a gravity equation with multilateral resistance terms. We can rewrite the above as:

πij  =  Tjcj 1−σ (τij)1−σΦi,

where 
Φi=∑kTkck 1−σ(τik) 1−σ
 is an inward multilateral resistance index for importer i. Similarly, an outward multilateral resistance for exporter j can be defined as 
Ψj=∑mTjcj 1−σ(τmj)1−σEmEworld

 (up to a normalization by world expenditure). In the special case of balanced trade and full CES gravity, these resistance terms correspond to the solution of the system introduced by Anderson and van Wincoop (2003): intuitively, 
Pi 1−σ=Φi

 measures the “average difficulty” of importing into i, and 
Ψj 1−σ
Ψ
j
1−σ
	​

 measures the average difficulty of j reaching world markets. Formally, 
Pi
P
i
	​

 solves

Pi 1−σ=∑j=1N(τijcj) 1−σEjEworld,

and 
Ψj
Ψ
j
	​

 satisfies a dual condition for exporters (these ensure all trade flows add up consistently). Multilateral resistances thus adjust endogenously to any change in trade costs, guaranteeing that supply equals demand globally and that each country’s expenditure is allocated across suppliers according to relative costs.

Income Balance (Market Clearing): In equilibrium, each country’s income equals the total expenditure on its goods worldwide plus any net transfer. That is:

Yj  =  ∑i=1NXij+Fj,

for each country j. If 
Fj=0
F
j
	​

=0 (balanced trade), income from sales equals spending on domestic goods plus exports. If 
Fj<0
F
j
	​

<0 (deficit), country j is importing more than it exports, financing the difference by the transfer 
−Fj
−F
j
	​

 from foreign sources. We assume any such transfers are lump-sum to the representative consumer and do not directly affect production or preferences (aside from providing additional purchasing power if positive).

General Equilibrium Existence: Under the above structure (CES demand, continuous goods, iceberg costs, and either fixed labor or monopolistic competition with free entry ensuring zero profits), a unique equilibrium set of wages 
wi
w
i
	​

 (hence incomes 
Yi=wiLi
Y
i
	​

=w
i
	​

L
i
	​

) and price indices 
Pi
P
i
	​

 exists that clears all markets. We omit a detailed proof of existence/uniqueness (which follows standard gravity-model arguments) and instead focus on characterizing the equilibrium before and after fragmentation.

Fragmentation Scenario and Equilibrium Conditions

We now formalize the scenario of trade fragmentation into two blocs. Initially, countries trade under the cost matrix 
{τij(0)}
{τ
ij
(0)
	​

}. In the fragmented world, trade costs become 
{τij(1)}
{τ
ij
(1)
	​

}. The defining feature of fragmentation is that trading across blocs becomes significantly more costly:

If 
i,j
i,j are in the same bloc, 
τij(1)
τ
ij
(1)
	​

 remains relatively low (we consider the benchmark of no change for within-bloc trade: 
τij(1)=τij(0)
τ
ij
(1)
	​

=τ
ij
(0)
	​

, often 
≈1
≈1). Members of a bloc continue to trade freely among themselves.

If 
i∈A
i∈A and 
j∈B
j∈B (or vice versa), then 
τij(1)
τ
ij
(1)
	​

 is much larger than 
τij(0)
τ
ij
(0)
	​

. In the extreme case, take 
τij(1)→∞
τ
ij
(1)
	​

→∞, meaning no trade between blocs in equilibrium (complete decoupling). More generally, one might consider 
τij(1)=Δ>1
τ
ij
(1)
	​

=Δ>1 (a large finite increase) or an ad-valorem tariff 
t
t applied between blocs. For theoretical clarity, we analyze the autarky-between-blocs case first, then consider small increases 
Δτ
Δτ.

Under fragmentation, each bloc essentially forms an internal trade network separated by a high barrier from the other bloc. The general equilibrium in the fragmented world must satisfy the same conditions as before (utility maximization, goods market clearing, income/budget balance), but with the modified trade cost matrix. In particular, within each bloc the allocation of production and consumption still obeys the gravity equation with low internal costs, whereas cross-bloc trade flows 
πij
π
ij
	​

 will be near zero (or zero in the limit 
τ→∞
τ→∞). The multilateral resistance terms adjust: intuitively, each bloc becomes a self-contained market, so countries’ price indices will reflect only suppliers within their own bloc (when 
τ
τ across blocs is prohibitive, foreign goods from the other bloc drop out of the price index). Likewise, wages adjust so that supply = demand within each bloc plus any net transfers (which now must also presumably come from within bloc if trade between blocs is impossible—though one could imagine financial transfers continuing, but those would not translate into actual goods movement if goods cannot cross blocs).

To formalize the fragmented equilibrium, consider any country 
i∈A
i∈A. Its expenditure shares in the fragmented regime (
1
1) versus initial regime (
0
0) are:

Initially (0): 
πij(0)
π
ij
(0)
	​

 for 
j∈A
j∈A and 
πik(0)
π
ik
(0)
	​

 for 
k∈B
k∈B were determined by low trade costs. Define

ψi  =  ∑k∈Bπik(0) ,

the share of country i’s expenditure on goods from the other bloc (Bloc B). Similarly, 
∑j∈Aπij(0)=1−ψi
∑
j∈A
	​

π
ij
(0)
	​

=1−ψ
i
	​

 is the within-bloc expenditure share for i initially (this includes both domestic purchases and imports from other A countries). We will call 
1−ψi
1−ψ
i
	​

 the intra-bloc share for country i. In a symmetric integrated equilibrium (to be defined shortly), all countries in a bloc might have the same 
ψ
ψ, but for now we keep 
ψi
ψ
i
	​

 country-specific.

Under fragmentation (1): if cross-bloc trade is cut off, then country i can only consume domestic and bloc-A goods. Thus for all 
k∈B
k∈B, 
πik(1)=0
π
ik
(1)
	​

=0. Country i reallocates that expenditure towards domestic and other A suppliers. Let 
π~ij(1)
π
~
ij
(1)
	​

 for 
j∈A
j∈A denote the new shares on Bloc A goods. Naturally, 
∑j∈Aπ~ij(1)=1
∑
j∈A
	​

π
~
ij
(1)
	​

=1. If the fragmentation shock is complete autarky between blocs, the intra-bloc share for i jumps to 100%.

The general equilibrium conditions in the fragmented regime are then (for each bloc handled separately):

Within each bloc, gravity holds: For 
i,j∈A
i,j∈A, 
π~ij(1)=Tj(τij(1))1−σ∑ℓ∈ATℓ(τiℓ(1))1−σ. The price index for 
i
i becomes 
Pi(1)=(∑j∈ATj[τij(1)] 1−σ)1/(1−σ)
 (taking 
cj=1
c
j
	​

=1). This reflects only goods from within A. Similarly for countries in Bloc B with their own index.

No cross-bloc imports: For 
i∈A,k∈B
i∈A,k∈B, 
Xik(1)=0
X
ik
(1)
	​

=0 (if 
τik(1)→∞
τ
ik
(1)
	​

→∞, the model implies zero demand for those goods as they are infinitely expensive). In practice, if 
τ
τ is large but finite, 
Xik(1)
X
ik
(1)
	​

 will be very small; here we focus on the limiting autarky case for clarity. This means in i’s budget, the fraction 
ψi
ψ
i
	​

 that was formerly spent on Bloc B must be redistributed within A. One can think of it as i facing a budget constraint 
Ei(1)=∑j∈AXij(1)
E
i
(1)
	​

=∑
j∈A
	​

X
ij
(1)
	​

 (since cross-bloc terms are zero, ignoring net transfer which we handle in income).

Income and market clearing within blocs: Each country’s income must equal expenditures on its goods by partners in the same bloc, plus any net transfer. For a country 
j∈A
j∈A:

Yj(1)  =  ∑i∈AXij(1)  +  Fj ,

with the analogous condition for 
k∈B
k∈B. In other words, Bloc A’s goods market clears internally (Bloc B no longer participates in A’s goods market, and vice versa). If transfers 
Fj
F
j
	​

 were zero initially and remain zero, then each bloc’s trade is balanced internally.

Multilateral resistance in fragmented equilibrium: The inward multilateral resistance for i in Bloc A simplifies to

Pi(1) 1−σ=∑j∈ATj(τij(1)) 1−σ,

dropping any terms 
j∈B
j∈B which no longer contribute. Compared to the integrated equilibrium, the price index 
Pi
P
i
	​

 generally rises, as the summation is now over a subset of suppliers (fewer varieties or higher costs). One can similarly define an outward resistance for exporters in each bloc, but effectively each bloc’s general equilibrium is like a closed economy (or a smaller open economy) solving its own gravity system in isolation.

With this setup, we are ready to derive results for welfare under trade fragmentation. We first define our welfare metric. Since preferences are homothetic and utility is increasing in real consumption, we can use real income (real GDP) as the welfare indicator for each country. Let 
Wi
W
i
	​

 denote country i’s welfare, which can be expressed as indirect utility 
Wi=EiPi
W
i
	​

=
P
i
	​

E
i
	​

	​

 (nominal spending divided by the cost-of-living index) for the representative agent. Equivalently, if 
Yi
Y
i
	​

 is income and 
Fi
F
i
	​

 a transfer, 
Wi=Yi+FiPi
W
i
	​

=
P
i
	​

Y
i
	​

+F
i
	​

	​

. We will often discuss proportional changes in welfare between equilibria, which are invariant to numéraire. In particular, the welfare change due to fragmentation for country i can be written as a ratio or percentage change:

Welfare Changei=Wi(1)Wi(0)−1,

where 0 denotes the initial (integrated world) value and 1 the fragmented world value. A negative value indicates a welfare loss.

Welfare Analysis Under Two-Bloc Fragmentation

We now present a series of theoretical results characterizing welfare in the fragmented two-bloc equilibrium. We proceed from special symmetric cases (yielding simple “sufficient statistic” formulas) to general results, and then we extend the model to relax some assumptions (trade imbalances, non-homothetic preferences, asymmetric sizes, heterogeneous elasticities).

Symmetric Fragmentation: Exact Welfare Change (“ψ-Rule”)

To build intuition, we first analyze a highly symmetric scenario and derive an exact welfare formula for fragmentation.

Symmetric Case Assumptions: Suppose that all countries are ex-ante identical (same technology 
Ti=T
T
i
	​

=T, same size 
Li
L
i
	​

, etc.) and that the two blocs are of equal size. Specifically, let Bloc A and Bloc B each contain 
N/2
N/2 countries, and assume initially there are no trade costs (
τij(0)=1
τ
ij
(0)
	​

=1 for all pairs). By symmetry, in the initial integrated equilibrium every country spends an equal fraction on every other country’s goods. In particular, each country’s cross-bloc import share is



and its within-bloc share (including home) is 
1−ψ=1/2
1−ψ=1/2. (More generally, if blocs have unequal size, 
ψ
ψ would be the relative size of the other bloc; we return to that in the asymmetric analysis.) Now consider complete fragmentation (no cross-bloc trade). By symmetry, in the fragmented equilibrium each country will reallocate expenditure that was formerly on Bloc B goods to domestic and Bloc A goods evenly. The new expenditure shares become: domestic + intra-A = 100%, extra-bloc = 0%.

Proposition 1 (Symmetric Welfare Loss from Fragmentation). Under the above symmetric conditions, the welfare impact of splitting the world into two autarkic blocs can be exactly quantified by a simple “ψ-rule.” In particular, each country’s real income falls by a factor equal to 
(1−ψ)1/ϵ
(1−ψ)
1/ϵ
, where 
ψ
ψ is the initial fraction of expenditure on the other bloc’s goods and 
ϵ=σ−1
ϵ=σ−1 is the trade elasticity. Equivalently, the proportional welfare loss for any country is

W(1)W(0)  =  (1−ψ) 1/ϵ,

so that 
W(1)<W(0)
W
(1)
<W
(0)
 whenever 
ψ>0
ψ>0. In the symmetric two-bloc case with equal bloc size, 
ψ=1/2
ψ=1/2, hence 
W(1)/W(0)=(1/2)1/ϵ
W
(1)
/W
(0)
=(1/2)
1/ϵ
. For example, if 
ϵ=5
ϵ=5, fragmentation into two equal halves implies each country’s real income falls to 
(0.5)1/5≈0.8706
(0.5)
1/5
≈0.8706 of its initial level (a ~13% welfare loss).

Proof (Sketch): In the symmetric integrated equilibrium, by the ACR formula
nber.org
 the welfare gain from having access to bloc-B goods (as opposed to autarky from B) can be measured by the share of spending on those goods. When that access is cut off, symmetry implies the exact change in the CES price index can be computed. Initially, the price index for a representative country i was

Pi(0)=[ N⋅(1) 1−σ ]1/(1−σ)=N1/(1−σ)c,

with 
c
c a common unit cost, say 
c=1
c=1. After fragmentation, country i in Bloc A can only access 
N/2
N/2 varieties (those in A). The new price index is

Pi(1)=(N/2)1/(1−σ)⋅1.

Taking the ratio,

Pi(1)Pi(0)=(N/2N)1/(1−σ)=(1/2)1/(1−σ)=(1−ψ)−1/(σ−1),

since 
1−ψ=1/2
1−ψ=1/2 for equal halves. Therefore, the welfare ratio (inverse ratio of price indices, since nominal incomes $Y_i$ are unchanged aside from price effects in this symmetric case) is

Wi(1)Wi(0)=Pi(0)Pi(1)=(1−ψ)1/(σ−1)=(1−ψ)1/ϵ.

This matches the stated ψ-rule. Another way to see this result is to apply the general formula for welfare gains from trade in an ACR model
nber.org
: the gain from access to foreign varieties is governed by the domestic (or intra-bloc) expenditure share. Here, moving to fragmentation effectively makes “rest of world” inaccessible, so Bloc A behaves like a closed economy for its members. The welfare loss of fragmentation is the same as the welfare gain that those countries enjoyed from cross-bloc trade initially. That gain, by ACR, equals 
(1/home+intra-bloc share)1/ϵ−1
(1/home+intra-bloc share)
1/ϵ
−1. Since home+intra-bloc share = $1-\psi$, the loss is $(1-\psi)^{-1/\epsilon} - 1$, and the remaining welfare level is $(1-\psi)^{1/\epsilon}$ of the initial.
nber.org
 It is worth noting this formula is exact under symmetry – no approximations needed.* □

Interpretation: The “ψ-rule” means that in a symmetric world, one only needs to know a country’s initial dependence on the other bloc (ψ) and the trade elasticity ε to compute exactly how much welfare falls when globalization is fragmented. For instance, if 30% of a country’s spending was on goods from the other bloc (ψ = 0.3) and the trade elasticity is ε = 4, then fragmentation (cutting off that 30%) reduces welfare by a factor $(1-0.3)^{1/4} ≈ 0.7^{0.25} ≈ 0.914$, i.e. an 8.6% drop in real income. Larger ψ (greater global integration) or smaller ε (goods less substitutable) lead to bigger welfare losses.

Corollary 1 (Bloc Size Asymmetry): If the two blocs differ in total economic size or number of countries, the formula generalizes to 
Wi(1)/Wi(0)=(1−ψi)1/ϵ
W
i
(1)
	​

/W
i
(0)
	​

=(1−ψ
i
	​

)
1/ϵ
 for a country i in Bloc A, where 
ψi
ψ
i
	​

 now corresponds to i’s initial expenditure share on Bloc B goods. In an asymmetric setting, countries in the smaller bloc will typically have a higher ψ (they relied more on the larger foreign market) and thus suffer a larger welfare hit, whereas those in the larger bloc had lower ψ and lose relatively less. For example, if Bloc B is twice the size of A, a country in A might have $\psi = 2/3$ (two-thirds of its expenditure went to B pre-fragmentation), yielding $W^{(1)}/W^{(0)} = (1/3)^{1/\epsilon}$ (a very large drop), while a country in B might have $\psi = 1/3$ (only one-third on A), yielding $(2/3)^{1/\epsilon}$.

General Equilibrium Welfare Bounds with Endogenous Price Effects

The exact “ψ-rule” derived above relies on strong symmetry. In a general two-bloc model without symmetry, we typically cannot get a closed-form welfare change for each country without detailed data on trade flows and elasticities. However, we can establish bounds on the welfare loss from fragmentation that apply in any case. These bounds clarify how general equilibrium adjustments (endogenous price changes) influence the welfare outcome.

Proposition 2 (Bounds on Welfare Loss): Consider any country 
i
i in Bloc A. Let 
ψi=∑k∈Bπik(0)
ψ
i
	​

=∑
k∈B
	​

π
ik
(0)
	​

 be the initial cross-bloc import share of country i. Then the following bounds hold when Bloc A and Bloc B become completely segmented (cross-bloc trade costs $\to \infty$):

(Upper bound – no substitution or price adjustment): The maximum possible welfare loss for country i (in percentage terms) does not exceed 
ψi×100%
ψ
i
	​

×100%. In other words, 
Wi(1)/Wi(0)≥1−ψi
W
i
(1)
	​

/W
i
(0)
	​

≥1−ψ
i
	​

. This bound corresponds to a (hypothetical) worst-case scenario in which goods from Bloc B are completely lost and cannot be substituted at all by domestic or intra-bloc alternatives. In reality, consumers will reallocate spending to other goods, mitigating the loss, so actual welfare stays above this floor.

(Lower bound – perfect substitution): The minimum possible welfare loss is zero in the limit of very high substitutability or alternative supply. Specifically, as the trade elasticity $\epsilon \to \infty$ (goods become perfect substitutes), $W_i^{(1)} / W_i^{(0)} \to 1$. With perfectly substitutable goods, country i can replace imports from Bloc B with identical products from Bloc A at negligible cost, so fragmentation causes virtually no welfare decline. For any finite $\epsilon$, the welfare loss will be strictly positive if $\psi_i>0$, but small if $\epsilon$ is large.

(Monotonicity): For a given $\psi_i$, the welfare loss $1 - W_i^{(1)}/W_i^{(0)}$ is monotonic in the trade elasticity $\epsilon$. All else equal, a lower elasticity (goods are more differentiated or harder to replace) leads to a larger welfare hit from fragmentation, and vice versa. For example, holding $\psi_i=0.3$, if $\epsilon=2$ the loss might be around 15–20%, whereas if $\epsilon=8$ the loss might shrink to ~4–5%. This is consistent with the $\psi$-rule in the symmetric case and holds generally: $\frac{\partial}{\partial \epsilon}(W_i^{(1)}/W_i^{(0)}) > 0$.

Proof Sketch: The upper bound can be understood by noting that initially, a fraction $\psi_i$ of consumption came from Bloc B. If those goods disappear, a naive upper estimate of utility loss is that $\psi_i$ fraction of consumption is gone. More rigorously, consider the Divisia price index formula for a small change: $d\ln P_i \approx \sum_j \pi_{ij}, d\ln p_{ij}$. In the move to fragmentation, effectively the price of Bloc B goods faced by i goes from $p_{ij}=1$ to $p_{ij}\to \infty$, an infinite percentage increase. However, the effect on the cost of living is tempered because i will not actually pay infinite prices—i will drop $j$ from its consumption bundle. The worst-case scenario is if i could not substitute at all and still needed to spend $\psi_i E_i$ on Bloc B goods despite their price going to infinity. In that (extreme and infeasible) case, $P_i$ would rise in proportion to that price increase, and $W_i$ would drop by at most $\psi_i$ proportion (since $\psi_i E_i$ worth of consumption becomes unavailable). Thus, $W_i^{(1)}/W_i^{(0)}$ cannot be less than $1-\psi_i$. In any realistic scenario, i reallocates that expenditure internally, achieving higher utility than the no-substitution worst case.

For the lower bound, if $\epsilon$ is extremely large, goods from different sources are almost perfect substitutes. Country i can respond to the loss of Bloc B goods by buying more from Bloc A producers with only a tiny loss in utility (since marginal utility of an extra unit of a close substitute good is almost the same as the lost good). Formally, as $\sigma \to \infty$, the CES utility approaches the Leontief/perfect-substitute limit where the consumer buys only the cheapest goods. Before fragmentation, all goods cost the same (by symmetry or assumption), and after fragmentation, Bloc B goods become more expensive, so the consumer in i drops them entirely and buys from bloc A with negligible utility loss (because those goods are nearly identical). Thus $P_i^{(1)} \approx P_i^{(0)}$, implying $W_i^{(1)} \approx W_i^{(0)}$. For any finite $\sigma$, one can show $P_i^{(1)} > P_i^{(0)}$ if $\psi_i>0$, so some loss occurs. The monotonicity of loss in $1/\sigma$ (or in $\epsilon$) can be verified by implicit differentiation of the exact welfare formulas in special cases or by intuitive arguments: a smaller $\sigma$ (more love-of-variety or less substitutability) means i values the lost Bloc B varieties more and suffers a bigger utility drop when they vanish.
nber.org

In summary, even without symmetry, we know 
Wi(1)/Wi(0)
W
i
(1)
	​

/W
i
(0)
	​

 lies between 
1−ψi
1−ψ
i
	​

 (worst plausible case) and 1 (best case, achieved as $\epsilon \to \infty$). In practice, for empirically relevant elasticities (say $\epsilon$ in the range 4–8 for many goods), the actual welfare ratio will be much closer to 1 than to 
1−ψi
1−ψ
i
	​

. The naive loss $\psi_i$ (treating lost imports as lost consumption) overstates the true welfare loss because consumers re-optimize and domestic prices adjust. Endogenous price effects (general equilibrium adjustments) further buffer the impact: for instance, if country i was a large importer of Bloc B goods, in autarky from B it will redirect demand internally, potentially increasing demand for home goods and raising local wages/output, which can improve i’s income. Such income adjustments (terms-of-trade effects) can partially offset the loss from higher prices. Our bounds encapsulate these forces without requiring a full solution: actual outcomes will lie in between the no-adjustment and infinite-adjustment extremes.

First-Order Welfare Impact of Small Fragmentation Shocks

The previous analysis considered the extreme of complete bloc decoupling. We now examine small increases in cross-bloc trade costs and derive first-order (infinitesimal) effects on welfare. This will yield a simple expression linking the marginal welfare impact to pre-shock observables (namely, the initial trade shares). The result parallels the differential approach used by Arkolakis et al. (2012)
nber.org
 for small changes in trade costs.

Suppose that initially the world is integrated with some finite trade cost $\tau_{ij}^{(0)}$ between blocs (possibly $\tau=1$, free trade). Consider a small increase in all cross-bloc iceberg costs: for instance, $\tau_{ij}$ between blocs rises by a differential amount (say from 1 to $1 + d\tau$ for $i\in A, j\in B$, with $d\tau$ small). We wish to find the first-order change in $\ln W_i$ for a country in Bloc A.

Proposition 3 (First-Order Welfare Change). The first-order (infinitesimal) impact on welfare of a small symmetric increase in cross-bloc trade costs is given by the country’s initial cross-bloc import share. Formally, for a country $i\in A$:

∂ln⁡Wi∂ln⁡τAB∣τAB=τ0  =  − ψi ,
