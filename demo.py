from laurent import laurent
# initialize multivariate laurent variables    

# define some laurent polynomials
poly_p = laurent("x^2y^-3 - y^-1")
poly_q = laurent("1+3y^-1")
poly_r = laurent("-2x^5y^2+1")
poly_s = laurent("1")
poly_t = laurent("A^3x^2y - 2y^-1 +2x +2A x + 5A^1x^2y - yx +A")

print("Polynomial:",poly_p)

# binary operations
print("(",poly_p, ") + (", poly_q, ") =", poly_p + poly_q)
print("(",poly_p, ") - (", poly_q, ") =", poly_p - poly_q)
print("(",poly_p, ") * (", poly_q, ") =", poly_p * poly_q)
print("(",poly_q, ") + 7 =", poly_q + 7)
print("(",poly_p, ") * 7 =", poly_p * 7)
print("(",poly_p, ") ** 2 =", poly_p ** 2)
print("(",poly_p, ") // (", poly_r, ") =", poly_p // poly_r)
print("(",poly_p, ") % (", poly_r, ") =", poly_p % poly_r)

# unary operations
print("- (",poly_p, ") =", -poly_p)
print("abs(",poly_p, ") =", abs(poly_p))
print("~ (",poly_p, ") =", ~poly_p)

# query methods
print("monomialQ:", poly_p, '('+str(poly_p.monomialQ())+'),', poly_s,'('+str(poly_s.monomialQ())+')')
print("intQ:", poly_p, '('+str(poly_p.intQ())+'),', poly_s,'('+str(poly_s.intQ())+')')
print("oneQ:", poly_p, '('+str(poly_p.oneQ())+'),', poly_s,'('+str(poly_s.oneQ())+')')
print("zeroQ:", poly_p, '('+str(poly_p.zeroQ())+'),', laurent('0x'),'('+str(laurent('0x').zeroQ())+')')

# degrees, spans
print("Maximal degrees in", poly_p, "are", poly_p.max_deg())
print("Maximal degree of y in", poly_p, "is", poly_p.max_deg("y"))
print("Minimal degrees in", poly_p, "are", poly_p.min_deg())
print("Minimal degree of y in", poly_p, "is", poly_p.min_deg("y"))
print("Spans in",poly_p, "are", poly_p.span())
print("Span of y in",poly_p,"is", poly_p.span("y"))

# evaluation
print(poly_p, "evaluated at x=3, y=4 is", poly_p({"x":3, "y":4}))
print(poly_p, "evaluated at y=2 is", poly_p({"y":2}))

# float coefficients and degrees
print("Polynomial with floats:", laurent("0.5x + 0.75y^0.5 + 0.1x^0.25y"))


print(poly_t," = ",poly_t.collect('xy'))

"""
OUTPUT:

Polynomial: x^2y^-3 - y^-1
( x^2y^-3 - y^-1 ) + ( 1 + 3y^-1 ) = 1 + x^2y^-3 + 2y^-1
( x^2y^-3 - y^-1 ) - ( 1 + 3y^-1 ) = - 1 + x^2y^-3 - 4y^-1
( x^2y^-3 - y^-1 ) * ( 1 + 3y^-1 ) = 3x^2y^-4 + x^2y^-3 - 3y^-2 - y^-1
( 1 + 3y^-1 ) + 7 = 8 + 3y^-1
( x^2y^-3 - y^-1 ) * 7 = 7x^2y^-3 - 7y^-1
( x^2y^-3 - y^-1 ) ** 2 = - 2x^2y^-4 + x^4y^-6 + y^-2
( x^2y^-3 - y^-1 ) // ( 1 - 2x^5y^2 ) = x^2y^-3 + 2x^7y^-1
( x^2y^-3 - y^-1 ) % ( 1 - 2x^5y^2 ) = 4x^12y - y^-1
- ( x^2y^-3 - y^-1 ) = - x^2y^-3 + y^-1
abs( x^2y^-3 - y^-1 ) = x^2y^-3 + y^-1
~ ( x^2y^-3 - y^-1 ) = x^-2y^3 - y
monomialQ: x^2y^-3 - y^-1 (False), 1 (True)
intQ: x^2y^-3 - y^-1 (False), 1 (True)
oneQ: x^2y^-3 - y^-1 (False), 1 (True)
zeroQ: x^2y^-3 - y^-1 (False), 0 (True)
Maximal degrees in x^2y^-3 - y^-1 are {'x': 2, 'y': -1}
Maximal degree of y in x^2y^-3 - y^-1 is -1
Minimal degrees in x^2y^-3 - y^-1 are {'x': 0, 'y': -3}
Minimal degree of y in x^2y^-3 - y^-1 is -3
Spans in x^2y^-3 - y^-1 are {'x': 2, 'y': 2}
Span of y in x^2y^-3 - y^-1 is 2
x^2y^-3 - y^-1 evaluated at x=3, y=4 is - 0.109375
x^2y^-3 - y^-1 evaluated at y=2 is - 0.5 + 0.125x^2
Polynomial with floats: 0.1x^0.25y + 0.5x + 0.75y^0.5
A + 2Ax + 5Ax^2y + A^3x^2y + 2x - xy - 2y^-1  =  A + (2A + 2)x + (5A + A^3)x^2y - xy - 2y^-1
"""