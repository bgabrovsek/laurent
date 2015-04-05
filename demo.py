from laurent import laurent
# initialize multivariate laurent variables    
laurent.set_vars("xy")

poly_p = laurent("x^2y^-1 - y^-1")
poly_q = laurent("1+3y^-1")
poly_r = laurent("x-1")
poly_s = laurent("1")

print poly_p

# binary operations
print "(",poly_p, ") + (", poly_q, ") =", poly_p + poly_q
print "(",poly_p, ") - (", poly_q, ") =", poly_p - poly_q
print "(",poly_p, ") * (", poly_q, ") =", poly_p * poly_q
print "(",poly_p, ") + 7 =", poly_p + 7
print "(",poly_p, ") * 7 =", poly_p * 7
print "(",poly_p, ") ** 2 =", poly_p ** 2
print "(",poly_p, ") / (", poly_r, ") =", poly_p / poly_r
print "(",poly_p, ") % (", poly_r, ") =", poly_p % poly_r

# unary operations
print "- (",poly_p, ") =", -poly_p
print "abs(",poly_p, ") =", abs(poly_p)
print "~ (",poly_p, ") =", ~poly_p

# query methods
print "monomialQ:", poly_p.monomialQ(), poly_s.monomialQ()
print "intQ:", poly_p.intQ(), poly_s.intQ()
print "oneQ:", poly_p.oneQ(), poly_s.oneQ()
print "zeroQ:", poly_p.zeroQ(), poly_s.zeroQ()    

# degrees, spans
print "Maximal degrees:", poly_p.max_deg()
print "Maximal degree of x:", poly_p.max_deg("x")
print "Minimal degrees:", poly_p.min_deg()
print "Minimal degree of x:", poly_p.min_deg("x")
print "Spans:", poly_p.span()
print "Span of x:", poly_p.span("x")

# evaluation
print poly_p, "at x=3, y=4 is", poly_p({"x":3, "y":4})
print poly_p, "at y=2 is", poly_p({"y":2})

# float coefficients and degrees
print laurent("0.5x + 0.75y^0.5 + 0.1x^0.25y")

"""
OUTPUT:

- y^-1 + x^2y^-1
( - y^-1 + x^2y^-1 ) + ( 3y^-1 + 1 ) = 2y^-1 + 1 + x^2y^-1
( - y^-1 + x^2y^-1 ) - ( 3y^-1 + 1 ) = - 4y^-1 - 1 + x^2y^-1
( - y^-1 + x^2y^-1 ) * ( 3y^-1 + 1 ) = - 3y^-2 - y^-1 + 3x^2y^-2 + x^2y^-1
( - y^-1 + x^2y^-1 ) + 7 = - y^-1 + 7 + x^2y^-1
( - y^-1 + x^2y^-1 ) * 7 = - 7y^-1 + 7x^2y^-1
( - y^-1 + x^2y^-1 ) ** 2 = y^-2 - 2x^2y^-2 + x^4y^-2
( - y^-1 + x^2y^-1 ) / ( - 1 + x ) = y^-1 + xy^-1
( - y^-1 + x^2y^-1 ) % ( - 1 + x ) = 0
- ( - y^-1 + x^2y^-1 ) = y^-1 - x^2y^-1
abs( - y^-1 + x^2y^-1 ) = y^-1 + x^2y^-1
~ ( - y^-1 + x^2y^-1 ) = x^-2y - y
monomialQ: False True
intQ: False True
oneQ: False True
zeroQ: False False
Maximal degrees: {'y': -1, 'x': 2}
Maximal degree of x: 2
Minimal degrees: {'y': -1, 'x': 0}
Minimal degree of x: 0
Spans: {'y': 0, 'x': 2}
Span of x: 2
- y^-1 + x^2y^-1 at x=3, y=4 is 2.0
- y^-1 + x^2y^-1 at y=2 is - 0.5 + 0.5x^2
0.75y^0.5 + 0.1x^0.25y + 0.5x

"""
