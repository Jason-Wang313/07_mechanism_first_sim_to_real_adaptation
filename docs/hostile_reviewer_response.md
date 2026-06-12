# Hostile Reviewer Response

The strongest hostile review is that the paper's mechanism-first adapter succeeds because the diagnostic probes are hand-designed and noiseless. The v2 response is to measure that assumption directly. With Gaussian noise added to diagnostic residual features, mechanism accuracy remains 1.000 at sigma 0.01, drops to 0.830 at sigma 0.04, and falls to 0.503 at sigma 0.12. Mean final error rises from 0.0017 clean to 0.0294 and 0.1098.

This narrows the paper: mechanism-first repair coordinates are useful only when probe residuals reliably separate repair-equivalence classes. The paper does not solve probe synthesis, robust sensing, hardware transfer, or open-world mechanism discovery.

The correct immediate venue decision is workshop-only.
