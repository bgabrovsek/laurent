# laurent
Multivariate Laurent polynomial module

Example of usage:

laurent.set_vars("xy")
print laurent("x^2y^-1 - y^-1") * laurent("x^8 - xy^-4") + laurent("x + 8") + 9

For more examples see demo.py.
