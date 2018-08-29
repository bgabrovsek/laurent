# laurent
Multivariate Laurent polynomial module (updated)

Example of usage:

poly1 = laurent("x^2y^-3 - y^-1")
poly2 = laurent("1+3y^-1")
poly3 = poly1 + poly2 + 3

See demo.py for more examples.

Changes:
- removed variable initialization
