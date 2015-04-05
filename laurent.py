"""
A multivariate Laurent polynomial python module
Created by Bostjan Gabrovsek on 05/04/15.

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
"""

import re

# compile RegEx's for parsing
re_insert_plus = re.compile(r"^(?=\w)") # start of line with no alphanumerical
re_insert_ones = re.compile(r"([-+](?!\d))") # +-char
re_insert_carets = re.compile(r"([A-Z|a-z](?!\^))") # char without a following caret
re_insert_whitespace = re.compile(r"(?<=\d)([-+])(?=\d)") # +- with decimals on both sides
re_insert_star = re.compile(r"([A-Z|a-z])") # char
re_whitespace = re.compile(r"\s") # whitespace
re_star = re.compile(r"\*") # star
re_brackets = re.compile(r"[()\[\]{}]") # bracketss
re_star_star = re.compile(r"\*\*") # star
re_star_caret = re.compile(r"[*^]") # star or carets

# by default laurent has variable one x
laurent_vars = {0:"x"}
laurent_vars_inverse = {"x":0}

def sign_char(i):
    """returns + is i non-negative and - otherwise """
    if i >= 0: return "+"
    return "-"

def numerical(s):
    "puts string s to int or float, depending on what s represents"
    if "." in s: return float(s)
    else: return int(s)
    
class term:
    """class representing a single multivariate term in laurent"""
    
    # Initialization, deletion, representation
     
    #def __new__(self, arg): N/A
    
    def __init__(self, s = None):
        """ initializes the multivariate laurent term, argument may be either:
        a term (makes a copy),
        integer (makes a term with degrees 0),
        string (of the form "+ x^ay^bz^c..."),
        or empty (makes an empty term) """
        
        if isinstance(s, term):
            self.coef = s.coef
            self.deg = [ s.deg[v] for v in laurent_vars ]
            
        elif s == None:
            # make empty term
            pass
            
        elif isinstance(s, str):
            s_split = re_star_caret.split(s)
            self.coef = numerical(s_split[0])
            self.deg = [0 for v in laurent_vars] # list of 0's
            
            for i in range(len(s_split)/2):
                self.deg[laurent_vars_inverse[s_split[i*2+1]]] = numerical(s_split[i*2+2]) 
                
        elif isinstance(s, int) or isinstance(s, float):
            self.coef = s
            self.deg = [ 0 for v in laurent_vars]
        
        else: raise ValueError('Term called with wrong argument.')

        self.canonical()
        
    #def __del__(self, arg): N/A
    
    def __repr__(self):
        """ term to readable string """
        
        if self.zeroQ(): return " + 0"
        if self.intQ(): return " " + sign_char(self.coef) + " " + str(abs(self.coef))
        
        s = " " + sign_char(self.coef) + " " # sign
        if self.coef not in [1,-1]: s += str(abs(self.coef)) # coefficient
        
        # variables
        for v in laurent_vars:
            if self.deg[v]:
                s += laurent_vars[v]
                if self.deg[v] != 1: s += "^" + str(self.deg[v])
        return s
        
        
    #def __str__(self, arg): N/A
     
    # Comparison operators

    def __eq__(self, t):
        """ == operator """        
        return (self.coef == t.coef) and (self.deg == t.deg)

    def __ne__(self, t):
        """ != operator"""
        return (self.coef != t.coef) or (self.deg != t.deg)

    def __lt__(self, t):
        """ < operator, compares first by degrees and secondly by coefficient """
        if self.deg == t.deg: return self.coef < t.coef
        return self.deg < t.deg

    def __le__(self, t):
        """ <= operator """
        if self.deg == t.deg: return self.coef <= t.coef
        return self.deg <= t.deg
 
    def __gt__(self, t):
        """ > operator """
        if self.deg == t.deg: return self.coef > t.coef
        return self.deg > t.deg

    def __ge__(self, t):
        """ >= operator """
        if self.deg == t.deg: return self.coef >= t.coef
        return self.deg >= t.deg

    def __nonzero__(self):
        """ False if term is 0, True otherwise """
        return not self.zeroQ()

    #def __hash__(self, arg): N/A
   
    # Call emulator

    def __call__(self, dict):
        """ evaluate term at values specified in dictionary """
        
        t = term(self)
        
        for v in dict:
            t *= (dict[v] ** t.deg[laurent_vars_inverse[v]])
            t.deg[laurent_vars_inverse[v]] = 0
        return t
            
    # Container emulator

    #def __len__(self, arg): N/A
    #def __getitem__(self, arg): N/A
    #def __missing__(self, arg): N/A
    #def __setitem__(self, arg): N/A
    #def __delitem__(self, arg): N/A
    #def __iter__(self, arg): N/A
    #def __reversed__(self, arg): N/A
    #def __contains__(self, arg): N/A
    
    # Sequence emulator

    #def __getslice__(self, arg): N/A
    #def __setslice__(self, arg): N/A
    #def __delslice__(self, arg): N/A

    # Binary arithemrics

    #def __add__(self, arg): N/A
    #def __sub__(self, arg): N/A
        
    def __mul__(self, t):
        """ * operator """
        new_t = term(self)
        new_t *= t
        return new_t
    
    def __pow__(self, i):
        """ ** operator """
        new_t = term(self)
        new_t **= t
        return new_t
        
    #def __divmod__(self, arg): N/A
     
    def __div__(self, t):
        """ / operator """
        new_t = term(self)
        new_t /= t
        return new_t

    #def __truediv__(self, arg): N/A
    #def __floordiv__(self, arg): N/A
    #def __mod__(self, arg): N/A
     
    # Arithemrics (logic)

    #def __lshift__(self, arg): N/A
    #def __rshift__(self, arg): N/A
    #def __and__(self, arg): N/A
    
    def __xor__(self, t):
        """ ^ operator, True if term similar (ie. degrees match), False otherwise """
        return (self.deg == t.deg)
    
    #def __or__(self, arg): N/A
    
    # Right arithemrics

    #def __radd__(self, arg): N/A
    #def __rsub__(self, arg): N/A
    #def __rmul__(self, arg): N/A
    #def __rpow__(self, arg): N/A
    #def __rdivmod__(self, arg): N/A
    #def __rdiv__(self, arg): N/A
    #def __rtruediv__(self, arg): N/A
    #def __rfloordiv__(self, arg): N/A
    #def __rmod__(self, arg): N/A
    
    # Right arithemrics (logic)

    #def __rlshift__(self, arg): N/A
    #def __rrshift__(self, arg): N/A
    #def __rand__(self, arg): N/A
    #def __rxor__(self, arg): N/A
    #def __ror__(self, arg): N/A
    
    # Arithmeric assignment

    #def __iadd__(self, arg): N/A
    
    #def __isub__(self, arg): N/A
     
    def __imul__(self, t):
        """ *= operator """

        if isinstance(t,int) or isinstance(t, float): # division by integer
            self.coef *= t
            
        elif isinstance(t, term):
            self.coef *= t.coef
            for v in laurent_vars:
                self.deg[v] += t.deg[v]
        
        else:
            raise ValueError("Multiplication of term by unsupported type.")
        
        self.canonical()
        return self
        
        
    def __ipow__(self, i):
        """ **= operator """
        self.coef **= i
        for v in laurent_vars: self.deg[v] += i
        return self

    def __idiv__(self, t):
        """ /= operator """
        
        if isinstance(t,int) or isinstance(t, float): # division by integer
            self.coef //= t
            
        elif isinstance(t, term):
            self.coef //= t.coef
            for v in laurent_vars:
                self.deg[v] -= t.deg[v]
        
        else:
            raise ValueError("Division of term by unsupported type.")
        
        self.canonical()
        return self
        
    #def __itruediv__(self, arg): N/A
    #def __ifloordiv__(self, arg): N/A
    #def __imod__(self, arg): N/A
     
    # Arithmeric assignment (logic)    

    #def __ilshift__(self, arg): N/A
    #def __irshift__(self, arg): N/A
    #def __iand__(self, arg): N/A
    #def __ixor__(self, arg): N/A
    #def __ior__(self, arg): N/A
    
    # Unary arithemtics

    def __neg__(self):
        """ negate, - unary operator """
        new_t = term(self)
        new_t.coef = -new_t.coef
        return new_t

    def __pos__(self):
        """ + unary operator (returns a copy) """
        return term(self)

    def __abs__(self):
        """ turns all coefficient to their absolute value """
        new_t = term(self)
        new_t.coef = abs(new_t.coef)
        return new_t
        
    def __invert__(self):
        """ raplaces each var v with v^-1 """
        new_t = term()
        new_t.coef = self.coef
        new_t.deg = [-a for a in self.deg]
        return new_t
        
    # Conversion

    #def __complex__(self, arg): N/A
    #def __int__(self, arg): N/A
    #def __long__(self, arg): N/A
    #def __float__(self, arg): N/A
    #def __oct__(self, arg): N/A
    #def __hex__(self, arg): N/A
    #def __index__(self, arg): N/A
    
    # Coercion rules

    #def __coerce__(self, arg): N/A
     
    # With statement context managers

    #def __enter__(self, arg): N/A
    #def __exit__(self, arg): N/A
    
    # Unicode

    #def __unicode__(self, arg): N/A
     
    # Attribute access

    #def __getattr__(self, arg): N/A
    #def __setattr__(self, arg): N/A
    #def __delattr__(self, arg): N/A
    #def __getattribute__(self, arg): N/A
    
    # Descriptors

    #def __get__(self, arg): N/A
    #def __set__(self, arg): N/A
    #def __delete__(self, arg): N/A
    #def __slots__(self, arg): N/A
    
    # Custom methods
    
    def canonical(self):
        "puts in canonical form: if zero coeff, zero out term as well"
        if self.coef == 0:
            for v in laurent_vars: self.deg[v] = 0
        
    # Custom methods (Queries)
    
    def intQ(self):
        """ True if the term an integer, False othwerwise """
        return all(v == 0 for v in self.deg)
    
    def zeroQ(self):
        """ True if the term is 0, False othwerwise """
        return self.coef == 0
    
    def oneQ(self):
        """ True if the term is 1, False othwerwise """
        return self.coef == 1 and self.intQ()
    
    
    

class laurent:
    """class representing a multivariate laurent polynomials, an ordered list of terms"""
    
    # Initialization, deletion, representation
    
    #def __new__(self, arg): N/A
     
    def __init__(self, s = None):
        """ initializes the multivariate laurent polynomial, argument may be either:
        a laurent polynomial (makes a copy),
        integer (makes poly with one 0 degrees term),
        string (of the form 'x+2y^3 -4y^-1 + z^(-3)y**5'),
        or empty (makes a polynomial without terms, ie. polynomial 0) """
        
        if isinstance(s, laurent):
            self.term = [ term(t) for t in s.term ]
        
        elif s == None:
            self.term = []
    
        elif isinstance(s, str):
            """ accepts strings like 'x+2y^3 -4y^-1 + z^(-3)y**5' """
            s = re_whitespace.sub("",s) # remove whitespace
            s = re_star_star.sub("^",s) # replace ** -> ^
            s = re_brackets.sub("",s) # remove brackets
            s = re_insert_plus.sub("+",s) # put + in front if missing
            s = re_insert_ones.sub("\g<1>1",s) # insert 1s in front of term starting with a variable
            s = re_insert_carets.sub("\g<1>^1",s) # insert ^1's after variables
            s = re_insert_whitespace.sub(" \g<1>",s) # insert whitespace between term
            s = re_insert_star.sub("*\g<1>",s) # insert *'s between elements
            s_split = re_whitespace.split(s) # split into a list of term
            
            self.term = [ term(st) for st in s_split ]
            
        elif isinstance(s, int) or isinstance(s, float):
            self.term = [ term(s)] 
            
        self.canonical()
        
    #def __del__(self, arg): N/A
    
    def __repr__(self):
        """ outputs the polynomial in human readable form """
        if self.zeroQ(): return "0"
        s = ""
        for t in self.term: s += str(t)
        s = s[1:] # remove leading whitespace
        if s[0] == "+": s = s[2:] # remove leading "+ "
        return s
    
    #def __str__(self, arg): N/A
    
    # Comparison

    def __eq__(self, p):
        """ == operator """
        if (len(self.term) != len(p.term)): return False
        for t0,t1 in zip(self.term, p.term):
            if t0 != t1: return False
        return True
        
    def __ne__(self, p):
        """ != operator """
        return not self == p

    def __lt__(self, p):
        """ < operator """
        for t0,t1 in zip(self.term, p.term):
            if t0 != t1: return t0 < t1 
        return len(self.term) < len(p.term)

    def __le__(self, p):
        """ <= operator """
        for t0,t1 in zip(self.term, p.term):
            if t0 != t1: return t0 < t1 
        return len(self.term) <= len(p.term)
 
    def __gt__(self, p):
        """ > operator """
        for t0,t1 in zip(self.term, p.term):
            if t0 != t1: return t0 > t1 
        return len(self.term) > len(p.term)

    def __ge__(self, p):
        """ >= operator """
        for t0,t1 in zip(self.term, p.term):
            if t0 != t1: return t0 > t1 
        return len(self.term) >= len(p.term)

    #def __cmp__(self, arg):
     
    def __nonzero__(self):
        """ False if polynomial is 0, True othwerwise """
        return not self.zeroQ()

    #def __hash__(self, arg): N/A
   
    # Call emulator

    def __call__(self, dic):
        """ evaluates the polynomial at values specified in dictionary """
        p = laurent()
        for t in self.term: p += t(dic)
        return p

    # Container emulator

    def __len__(self):
        """ returns number of terms """
        return len(self.term)

    #def __getitem__(self, arg): N/A
    #def __missing__(self, arg): N/A
    #def __setitem__(self, arg): N/A
    #def __delitem__(self, arg): N/A
    #def __iter__(self, arg): N/A
    #def __reversed__(self, arg): N/A
    #def __contains__(self, arg): N/A
    
    # Sequence emulator

    #def __getslice__(self, arg): N/A
    #def __setslice__(self, arg): N/A
    #def __delslice__(self, arg): N/A

    # Binary arithemrics

    def __add__(self, p):
        """ + operator """
        new_p = laurent(self) # make a copy
        new_p += p
        return new_p

    def __sub__(self, p):
        """ - operator """
        new_p = laurent(self) # make a copy
        new_p -= p
        return new_p

    def __mul__(self, p):
        """ * operator """
        
        new_p = laurent()
        
        if isinstance(p, laurent): # TODO: O(n ln(n))
            for t0 in self.term:
                for t1 in p.term:
                    new_p.term += [ t0 * t1 ]
            
        
        elif isinstance(p, int) or isinstance(p, float) or isinstance(p, term):
            new_p.term = [term(t) * p for t in self.term]
            
        new_p.canonical()
        
        return new_p
        
        
        
        new_p = laurent(self) # make a copy
        new_p *= p
        return new_p
    
    def __pow__(self, i):
        """ ** operator """
        new_p = laurent(1)
        for n in range(i):
            new_p *= self
        return new_p

    def __divmod__(self, p):
        """ returns [self/p, 0] if p divides self, otherwise returns [self/p, sel/p] after len(self) steps """
        # trivials
        if p.zeroQ(): raise ZeroDivisionError
        if self.zeroQ(): return [ laurent(0), laurent(p)]
        
        q = laurent() # quotient
        r = laurent(self) # reminder
        
        for n in self.term:
            t0 = r.term[0] / p.term[0]
            q += t0 
            r -= (p * t0)
            r.canonical()
            if r.zeroQ(): return [q, r] 
    
        return [q,r]
    
    def __div__(self, p):
        """ / operator, see __divmod__ """
        return divmod(self, p)[0]

    #def __truediv__(self, arg): N/A
    #def __floordiv__(self, arg): N/A
     
    def __mod__(self, p):
        """ mod operator, see __divmod__"""
        return divmod(self, p)[1]
    
    # Arithemrics (logic)

    #def __lshift__(self, arg): N/A
    #def __rshift__(self, arg): N/A
    #def __and__(self, arg): N/A
    #def __xor__(self, arg): N/A
    #def __or__(self, arg): N/A
    
    # Right arithemrics

    #def __radd__(self, arg): N/A
    #def __rsub__(self, arg): N/A
    #def __rmul__(self, arg): N/A
    #def __rpow__(self, arg): N/A
    #def __rdivmod__(self, arg): N/A
    #def __rdiv__(self, arg): N/A
    #def __rtruediv__(self, arg): N/A
    #def __rfloordiv__(self, arg): N/A
    #def __rmod__(self, arg): N/A
    
    # Right arithemrics (logic)

    #def __rlshift__(self, arg): N/A
    #def __rrshift__(self, arg): N/A
    #def __rand__(self, arg): N/A
    #def __rxor__(self, arg): N/A
    #def __ror__(self, arg): N/A
    
    # Arithmeric assignment

    def __iadd__(self, p):
        """ += operator """
                
        if isinstance(p,laurent):
            self.term +=  [ term(t) for t in p.term] # makes copies
            
        elif isinstance(p,term) or isinstance(p, int) or isinstance(p, float):
            self.term += [ term(p) ] # makes a copy
            
        self.canonical()
        return self
        
        
    def __isub__(self, p):
        """ -= operator """
        
        if isinstance(p,laurent):
            self.term +=  [ -t for t in p.term] # makes copies
            
        elif isinstance(p,term) or isinstance(p, int) or isinstance(p,float):
            self.term += [ -p ] # makes a copy
            
        self.canonical()
        return self
        
    def __imul__(self, p):
        """ *= operator """
        self.term = (self * p).term
        return self
    
    def __ipow__(self, n):
        """ **= operator """
        self.term = (self ** n).term
        return self

    def __idiv__(self, p):
        """ /= operator """
        self.term = (self / p).term
        return self

    #def __itruediv__(self, arg): N/A
    #def __ifloordiv__(self, arg): N/A
         
    def __imod__(self, p):
        """ %= operator """
        self.term = (self % p).term
        return self
    
    # Arithmeric assignment (logic)    

    #def __ilshift__(self, arg): N/A
    #def __irshift__(self, arg): N/A
    #def __iand__(self, arg): N/A
    #def __ixor__(self, arg): N/A
    #def __ior__(self, arg): N/A
    
    # Unary arithemtics

    def __neg__(self):
        """ - unary operator """
        new_p = laurent(self)
        for t in new_p.term:
            t.coef = - t.coef
        return new_p

    def __pos__(self):
        """ + unary operator, makes a copy"""
        return laurent(self)

    def __abs__(self):
        """ replaces all coefficients with their absolute value """
        new_p = laurent(self)
        for t in new_p.term:
            t.coef = abs(t.coef)
        return new_p

    def __invert__(self):
        """ replaces all variables v with v^-1 """
        new_p = laurent(self)
        for t in new_p.term:
            for v in laurent_vars:
                t.deg[v] = -t.deg[v]
        new_p.canonical()
        return new_p
        
    # Conversion

    #def __complex__(self, arg): N/A
    #def __int__(self, arg): N/A
    #def __long__(self, arg): N/A
    #def __float__(self, arg): N/A
    #def __oct__(self, arg): N/A
    #def __hex__(self, arg): N/A
    #def __index__(self, arg): N/A
    
    # Coercion rules

    #def __coerce__(self, arg): N/A
     
    # With statement context managers

    #def __enter__(self, arg): N/A
    #def __exit__(self, arg): N/A
    
    # Unicode

    #def __unicode__(self, arg): N/A
     
    # Attribute access

    #def __getattr__(self, arg): N/A
    #def __setattr__(self, arg): N/A
    #def __delattr__(self, arg): N/A
    #def __getattribute__(self, arg): N/A
    
    # Descriptors

    #def __get__(self, arg): N/A
    #def __set__(self, arg): N/A
    #def __delete__(self, arg): N/A
    #def __slots__(self, arg): N/A
    
    
    # Custom methods (sorting)
    
    def canonical(self):
        """ orders the polynomial and adds up coefficients of similar terms """
        self.sort()
        i = 0
        while (i < len(self.term)):
            if not self.term[i].coef: # remove 0 terms
                del self.term[i]
            elif i > 0:
                if (self.term[i].deg == self.term[i-1].deg): # add coef to prev if same deg
                    self.term[i-1].coef += self.term[i].coef
                    del self.term[i]
                    i -= 1 # check prev for 0
                else: i += 1
            else: i += 1
            
        
        
    def sort(self):
        """ sort terms by degrees """
        self.term.sort()
        
    # Custom method (degrees, spans)

    def max_deg(self, v = None):
        """ returns maximal degree of variable v, or a dictionary of maximal degrees if v not supplied """
        if v is None:
            return {laurent_vars[va]: max([t.deg[va] for t in self.term]) for va in laurent_vars}
        return max( [ t.deg[ laurent_vars_inverse[v] ] for t in self.term] )    
           
        
    def min_deg(self, v = None):
        """ returns minimal degree of variable v, or a dictionary of minimal degrees if v not supplied """
        if v is None:
            return {laurent_vars[va]: min([t.deg[va] for t in self.term]) for va in laurent_vars}
        return min( [ t.deg[ laurent_vars_inverse[v] ] for t in self.term] )    
        
    def min_max_deg(self, v = None):
        """ returns a list of max/min digrees of variable v, or a dictionary if v not supplied """
        if v is None:
            min_degs, max_degs = self.min_deg(), self.max_deg()
            return { va: ( min_degs[va], max_degs[va] ) for va in laurent_vars_inverse }
            
        return (self.min_deg(v), self.max_deg(v))
        
    def span(self, v = None):
        """ returns the span of variable v, or a dictionary of spans if v not supplied """
        if v is None:
            minmax = self.min_max_deg(v)
            return { va: minmax[va][1] - minmax[va][0] for va in laurent_vars_inverse }
        return self.max_deg(v) - self.min_deg(v)
        
    # Custom methods (queries)
    
    def monomialQ(self):
        """ True if polynomial is a monomial (has one term), False otherwise """
        return len(self.term) == 1
            
    def intQ(self):
        """ True if polynomial is an integer, False otherwise  """
        return self.monomialQ() and self.term[0].intQ()
        
    def zeroQ(self):
        """ True if polynomial is 0, False otherwise """
        return len(self.term) == 0
        
    def oneQ(self):
        """ True if polynomial is 1, False otherwise """
        return self.monomialQ() and self.term[0].oneQ()
    
    # Static methods
    
    @staticmethod
    def set_vars(s):
        """ sets global multiviariate variables """
        global laurent_vars, laurent_vars_inverse
        laurent_vars = {}
        laurent_vars_inverse = {}
        for i, c in enumerate(s):
            if "a" <= c <= "z" or "A" <= c <= "Z":
                laurent_vars[i] = c
                laurent_vars_inverse[c] = i


    
