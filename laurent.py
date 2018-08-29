import re
import operator
from collections import defaultdict
from functools import reduce

# compile RegEx's for parsing
re_insert_plus = re.compile(r'^(?=\w)') # start of line with no alphanumerical
re_insert_ones = re.compile(r'([-+](?!\d))') # +-char
re_insert_carets = re.compile(r'([A-Z|a-z](?!\^))') # char without a following caret
re_insert_whitespace = re.compile(r'(?<=\d)([-+])(?=\d)') # +- with decimals on both sides
re_insert_star = re.compile(r'([A-Z|a-z])') # char
re_whitespace = re.compile(r'\s') # whitespace
re_star = re.compile(r'\*') # star
re_brackets = re.compile(r'[()\[\]{}]') # bracketss
re_star_star = re.compile(r'\*\*') # star
re_star_caret = re.compile(r'[*^]') # star or carets


#def sign_char(i):
   # '''returns + is i non-negative and - otherwise '''
 #   return '+' if i >= 0 else '-'

#def numerical(s):
  #  'puts string s to int or float, depending on what s represents'
 #   return float(s) if 'x' in s else int(s)

class term:
    '''class representing a single multivariate term in laurent'''
    
    # Initialization, deletion, representation
     
    #def __new__(self, arg): N/A
    
    def __init__(self, s = None, parent = None):
        ''' initializes the multivariate laurent term, argument may be either:
        a term (makes a copy),
        integer (makes a term with degrees 0),
        string (of the form '+ x^ay^bz^c...'),
        or empty (makes an empty term) '''

        # by default laurent has variable one x



        if isinstance(s, term):
            self.coef = s.coef
            self.degree = dict(s.degree)

        elif s == None:
            # make empty term
            self.coef = 0
            pass
            
        elif isinstance(s, str):
            s_split = re_star_caret.split(s)
            self.coef = float(s_split[0]) if '.' in s_split[0] else int(s_split[0])
            self.degree = {} # empty dict


            for i in range(len(s_split)//2):
                self.degree[s_split[i*2+1]] = float(s_split[i*2+2]) if '.' in s_split[i*2+2] else int(s_split[i*2+2])

        elif isinstance(s, int) or isinstance(s, float):
            self.coef = s
            self.degree = {}

        else: raise ValueError('Term called with wrong argument.')

        self.canonical()

    #def __del__(self, arg): N/A

    def __repr__(self):
        ''' term to readable string '''
        
        if self.zeroQ(): return '0'
        if self.intQ(): return ('- ' if self.coef < 0 else '') + str(abs(self.coef))

        # coefficient
        s = ('- ' if self.coef < 0 else '') + (str(abs(self.coef)) if abs(self.coef) != 1 else '')

        # variables
        for v in self.degree:
            s += v + (('^'+str(self.degree[v])) if self.degree[v] != 1 else '')
        return s
        
        
    #def __str__(self, arg): N/A
     
    # Comparison operators

    def __eq__(self, t):
        ''' == operator '''
     #   return self.__cmp_split() == t.__cmp_split()
        return (tuple(self.degree.items()), self.coef) == (tuple(self.degree.items()), self.coef)

    def __ne__(self, t):
        ''' != operator'''
        return (tuple(self.degree.items()), self.coef) != (tuple(self.degree.items()), self.coef)

    def __lt__(self, t):
        ''' < operator, compares first variables, then degrees and then by coefficient '''
        return (tuple(self.degree.items()), self.coef) < (tuple(self.degree.items()), self.coef)

    def __le__(self, t):
        ''' <= operator '''
        return (tuple(self.degree.items()), self.coef) <= (tuple(self.degree.items()), self.coef)

    def __gt__(self, t):
        ''' > operator '''
        return (tuple(self.degree.items()), self.coef) > (tuple(self.degree.items()), self.coef)

    def __ge__(self, t):
        ''' >= operator '''
        return (tuple(self.degree.items()), self.coef) >= (tuple(self.degree.items()), self.coef)

    def __nonzero__(self):
        ''' False if term is 0, True otherwise '''
        return not self.zeroQ()


    #def __hash__(self, arg): N/A
   
    # Call emulator

    def __call__(self, d):
        ''' evaluate term at values specified in dictionary,
         e.g. dict = {'x':3, 'y': 4} avaluates the polynomial at x=3, y=4.'''
        
        t = term(self)
        for v in d:
            if v in t.degree:
                t *= d[v] ** t.degree[v]
                del t.degree[v]

        if isinstance(self.coef, int) and all(isinstance(e, int) for e in d.values()) and all(abs(e) == 1 for e in d.values()):
            t.coef = int(round(t.coef)) # make int
        t.canonical()
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

    def __add__(self, other):
        t = term(self)
        t += other
        return t

    def __sub__(self, other):
        t = term(self)
        t -= other
        return t
        
    def __mul__(self, t):
        ''' * operator '''
        new_t = term(self)
        new_t *= t
        return new_t
    
    def __pow__(self, exponent):
        ''' ** operator '''
        new_t = term(self)
        new_t **= exponent
        return new_t
        
    #def __divmod__(self, arg): N/A
     
    def __floordiv__(self, t):
        ''' / operator '''
        new_t = term(self)
        new_t //= t
        return new_t

    #def __truediv__(self, arg): N/A
    #def __floordiv__(self, arg): N/A
    #def __mod__(self, arg): N/A
     
    # Arithemrics (logic)

    #def __lshift__(self, arg): N/A
    #def __rshift__(self, arg): N/A
    #def __and__(self, arg): N/A
    
    def __xor__(self, t):
        ''' ^ operator, True if term similar (ie. degrees match), False otherwise '''
        return self.degree == t.degree
    
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

    def __iadd__(self, other):
        if not self ^ other: raise ValueError("Cannot add non-similar terms.")
        self.coef += other.coef
        self.canonical()
        return self
    
    def __isub__(self, other):
        if not self ^ other: raise ValueError("Cannot add non-similar terms.")
        self.coef -= other.coef
        self.canonical()
        return self

    def __imul__(self, other):
        ''' *= operator '''

        if isinstance(other,int) or isinstance(other, float): # division by integer
            self.coef *= other

            
        elif isinstance(other, term):
            self.coef *= other.coef
            for v in other.degree:
                self.degree[v] = (self.degree[v] + other.degree[v]) if v in self.degree else other.degree[v]

        else:
            raise ValueError('Multiplication of term by unsupported type.')
        
        self.canonical()
        return self
        
        
    def __ipow__(self, exponent):
        ''' **= operator '''
        self.coef **= exponent
        for v in self.degree:
            self.degree[v] += exponent
        self.canonical()
        return self


    def __ifloordiv__(self, other):
        ''' /= operator '''
        
        if isinstance(other,int) or isinstance(other, float): # division by integer
            self.coef //= other
            
        elif isinstance(other, term):
            self.coef //= other.coef
            for v in other.degree:
                self.degree[v] = (self.degree[v] - other.degree[v]) if v in self.degree else -other.degree[v]

        else:
            raise ValueError('Division of term by unsupported type.')
        
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
        ''' negate, - unary operator '''
        new_t = term(self)
        new_t.coef = -new_t.coef
        return new_t

    def __pos__(self):
        ''' + unary operator (returns a copy) '''
        return term(self)

    def __abs__(self):
        ''' turns all coefficient to their absolute value '''
        new_t = term(self)
        new_t.coef = abs(new_t.coef)
        return new_t
        
    def __invert__(self):
        ''' ~, raplaces each var v with v^-1 '''
        new_t = term(self)
        for v in new_t.degree:
            new_t.degree[v] *= -1
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
        '''puts in canonical form: if zero coeff, zero out term as well, remove variables with power 0'''

        if self.coef == 0: self.degree = {}
        self.degree = {v: exponent for v, exponent in sorted(self.degree.items()) if exponent != 0}

    # Custom methods (Queries)
    
    def intQ(self):
        ''' True if the term an integer, False othwerwise '''
        return all(v == 0 for v in self.degree)
    
    def zeroQ(self):
        ''' True if the term is 0, False othwerwise '''
      #  print("test(",self.coef,self.coef == 0,")")
        return self.coef == 0
    
    def oneQ(self):
        ''' True if the term is 1, False othwerwise '''
        return self.coef == 1 and self.intQ()
    
    def minusoneQ(self):
        ''' True if the term is 1, False othwerwise '''
        return self.coef == -1 and self.intQ()



class laurent:
    '''class representing a multivariate laurent polynomials, an ordered list of terms'''
    
    # Initialization, deletion, representation
    
    #def __new__(self, arg): N/A
     
    def __init__(self, s = None):
        ''' initializes the multivariate laurent polynomial, argument may be either:
        a laurent polynomial (makes a copy),
        integer (makes poly with one 0 degrees term),
        string (of the form 'x+2y^3 -4y^-1 + z^(-3)y**5'),
        or empty (makes a polynomial without terms, ie. polynomial 0)
        In vars we should provide a list (or string) of variables used
        (otherwise they are extracted from the string).'''

        # self.laurent_vars = {0: 'x'}
        # self.laurent_vars_inverse = {'x': 0}

        if isinstance(s, laurent):
            # make a copy
            self.term = [ term(t) for t in s.term ]
        
        elif s == None:
            self.term = []
    
        elif isinstance(s, str):

            #variable_list = sorted(set(re.sub(r'[^a-zA-Z]+','',s))) # set of variables usef in polynomial

            ''' accepts strings like 'x+2y^3 -4y^-1 + z^(-3)y**5' '''
            s = re_whitespace.sub('',s) # remove whitespace
            s = re_star_star.sub('^',s) # replace ** -> ^
            s = re_brackets.sub('',s) # remove brackets
            s = re_insert_plus.sub('+',s) # put + in front if missing
            s = re_insert_ones.sub('\g<1>1',s) # insert 1s in front of term starting with a variable
            s = re_insert_carets.sub('\g<1>^1',s) # insert ^1's after variables
            s = re_insert_whitespace.sub(' \g<1>',s) # insert whitespace between term
            s = re_insert_star.sub('*\g<1>',s) # insert *'s between elements
            s_split = re_whitespace.split(s) # split into a list of term

            self.term = [ term(st) for st in s_split ]


        elif isinstance(s, int) or isinstance(s, float):
#            raise ValueError('Not yet supported.') #TODO: variable tables
            self.term = [ term(s) ]

        self.canonical()

    #def __del__(self, arg): N/A

    def __repr__(self):

        ''' outputs the polynomial in human readable form '''
        if self.zeroQ(): return '0'
        return ' '.join( ('+ ' if i != 0 and s[0] != '-' else '') + s for i, s in enumerate(map(str,self.term)) )

    #def __str__(self, arg): N/A
    
    # Comparison

    def __eq__(self, p):
        ''' == operator '''
        return len(self.term) == len(p.term) and all(t0 == t1 for t0,t1 in zip(self.term, p.term))

        
    def __ne__(self, p):
        ''' != operator '''
        return not self == p

    def __lt__(self, p):
        ''' < operator '''
        return self.term < p.term

    def __le__(self, p):
        ''' <= operator '''
        return self.term <= p.term

    def __gt__(self, p):
        ''' > operator '''
        return self.term > p.term

    def __ge__(self, p):
        ''' >= operator '''
        return self.term >= p.term

    #def __cmp__(self, arg):
     
    def __nonzero__(self):
        ''' False if polynomial is 0, True othwerwise '''
        return not self.zeroQ()

    #def __hash__(self, arg): N/A
   
    # Call emulator

    def __call__(self, dic):
        ''' evaluates the polynomial at values specified in dictionary, e.g. {x:4, y:3} evaluates at x=4, y=3'''
        p = laurent()
        for t in self.term: p += t(dic)
        p.canonical()
        return p

    # Container emulator

    def __len__(self):
        ''' returns number of terms '''
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
        ''' + operator '''
        new_p = laurent(self) # make a copy
        new_p += p
        return new_p

    def __sub__(self, p):
        ''' - operator '''
        new_p = laurent(self) # make a copy
        new_p -= p
        return new_p

    def __mul__(self, p):
        ''' * operator '''
        
        new_p = laurent()

        if isinstance(p, laurent): # TODO: O(n ln(n))
            new_p.term = [ t0 * t1 for t0 in self.term for t1 in p.term]

        
        elif isinstance(p, int) or isinstance(p, float) or isinstance(p, term):
            new_p.term = [term(t) * p for t in self.term]
            
        new_p.canonical()
        
        return new_p

    def __pow__(self, i):
        ''' ** operator '''
        new_p = laurent(1)
        for n in range(i): # TODO: use map/reduce
            new_p *= self
        return new_p

    def __divmod__(self, p):
        ''' returns [self/p, 0] if p divides self, otherwise returns [self/p, sel/p] after len(self) steps '''
        # trivials
        if p.zeroQ(): raise ZeroDivisionError
        if self.zeroQ(): return [ laurent(0), laurent(p)]
        
        q, r = laurent(), laurent(self) # quotient and reminder
        
        for _ in self.term:
            t0 = r.term[0] // p.term[0]
            q += t0 
            r -= (p * t0)
            r.canonical()
            if r.zeroQ(): return [q, r] 
    
        return [q,r]
    
    def __floordiv__(self, p):
        ''' / operator, see __divmod__ '''
        return divmod(self, p)[0]

    #def __truediv__(self, arg): N/A
    #def __floordiv__(self, arg): N/A
     
    def __mod__(self, p):
        ''' mod operator, see __divmod__'''
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
        ''' += operator '''
                
        if isinstance(p,laurent):
            #self.term += [ term(t) for t in p.term] # makes copies
            self.term += list(map(term, p.term))

        elif isinstance(p,term) or isinstance(p, int) or isinstance(p, float):
            self.term.append(term(p)) # makes a copy

        else:
            raise ValueError("Adding unsupported type.")

        self.canonical()
        return self
        
        
    def __isub__(self, p):
        ''' -= operator '''
        
        if isinstance(p,laurent):
            self.term +=  [-t for t in p.term]  # makes copies


        elif isinstance(p,term) or isinstance(p, int) or isinstance(p,float):
            self.term += [-p]  # makes a copy


        self.canonical()

        return self
        
    def __imul__(self, p):
        ''' *= operator '''
        self.term = (self * p).term
        return self
    
    def __ipow__(self, n):
        ''' **= operator '''
        self.term = (self ** n).term
        return self

    def __ifloordiv__(self, p):
        ''' /= operator '''
        self.term = (self // p).term
        return self

    #def __itruediv__(self, arg): N/A
    #def __ifloordiv__(self, arg): N/A
         
    def __imod__(self, p):
        ''' %= operator '''
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
        ''' - unary operator '''
        new_p = laurent(self)
        for t in new_p.term:
            t.coef *= -1
        return new_p

    def __pos__(self):
        ''' + unary operator, makes a copy'''
        return laurent(self)

    def __abs__(self):
        ''' replaces all coefficients with their absolute value '''
        new_p = laurent(self)
        for t in new_p.term:
            t.coef = abs(t.coef)
        return new_p

    def __invert__(self):
        ''' replaces all variables v with v^-1 '''
        new_p = laurent()
        new_p.term = [~t for t in self.term]
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
        ''' orders the polynomial and adds up coefficients of similar terms '''

        # add similar terms in canonical form
        split_terms = defaultdict(list)
        for t in self.term:
            split_terms[tuple(sorted(t.degree.items()))].append(t)

        self.term = list(filter(lambda t: not t.zeroQ(), [reduce(operator.add,split_terms[tnc]) for tnc in sorted(split_terms)]))

        for t in self.term: t.canonical()



    # Custom method (degrees, spans)

    def vars(self):
        ''' returns set of all vars used in any of the terms '''
        return sorted(v for t in self.term for v in t.degree)

    def max_deg(self, v = None):
        ''' returns maximal degree of variable v, or a dictionary of maximal degrees if v not supplied '''
        if v is None:
            return {v: max((t.degree[v] if v in t.degree else 0) for t in self.term ) for v in self.vars()}
        return max((t.degree[v] if v in t.degree else 0) for t in self.term if v in t.degree)
           
        
    def min_deg(self, v = None):
        ''' returns maximal degree of variable v, or a dictionary of maximal degrees if v not supplied '''
        if v is None:
            return {v: min((t.degree[v] if v in t.degree else 0) for t in self.term ) for v in self.vars()}
        return min((t.degree[v] if v in t.degree else 0) for t in self.term)

    def min_max_deg(self, v = None):
        ''' returns a list of max/min digrees of variable v, or a dictionary if v not supplied '''
        if v is None:
            min_degs, max_degs = self.min_deg(), self.max_deg()
            return {u: (min_degs[u], max_degs[u]) for u in min_degs}
        return (self.min_deg(v), self.max_deg(v))
        
    def span(self, v = None):
        ''' returns the span of variable v, or a dictionary of spans if v not supplied '''
        if v is None:
            minmax = self.min_max_deg(v)
            return {u: minmax[u][1] - minmax[u][0] for u in minmax}
        return self.max_deg(v) - self.min_deg(v)
        
    # Custom methods (queries)
    
    def monomialQ(self):
        ''' True if polynomial is a monomial (has one term), False otherwise '''
        return len(self.term) == 1
            
    def intQ(self):
        ''' True if polynomial is an integer, False otherwise  '''
        return self.monomialQ() and self.term[0].intQ()
        
    def zeroQ(self):
        ''' True if polynomial is 0, False otherwise '''
        return len(self.term) == 0
        
    def oneQ(self):
        ''' True if polynomial is 1, False otherwise '''
        return self.monomialQ() and self.term[0].oneQ()

    def minusoneQ(self):
        ''' True if polynomial is -1, False otherwise '''
        return self.monomialQ() and self.term[0].minusoneQ()


    def collect(self, s):
        ''' collect vars in s, e.g. s = "xy", we collect x & y's, (a+a^2)x + (3+a)xy^3 '''

        ev_dict = {v:1 for v in s}
        groups = defaultdict(list)

        for t in self.term:
            groups[tuple( (v, t.degree[v] if v in t.degree else 0) for v in s )].append(t(ev_dict))

        s = ''
        for i, (g, poly) in enumerate(groups.items()):
            abs1 = False
            if len(poly) == 1:
                sp, abs1 = str(poly[0]), abs(poly[0]).oneQ()
            else:
                sp =  '('+' '.join(('+ ' if i != 0 and s[0] != '-' else '') + s for i, s in enumerate(map(str, poly)))+')'
            sg = ''.join( [ (v if e else '') + ( ('^'+str(e)) if e not in (0,1) else '' ) for v,e in g  ] )
            s += (' + ' if i and sp[0] != '-' else (' ' if i else '')) + (sp[:-1] if abs1 and sg else sp) + sg

        return s

