# -*- coding: utf-8 -*-
"""Portable MathML helpers for HTML deliverables.

Dependency-free. Every function returns an HTML string; compose them and wrap
the result in M() (inline) or MB() (block).

    >>> M(mi("a"), EQ, frac(DEL + mi("v"), DEL + mi("t")))
"""

# ---------- atoms ----------
def mi(s):  return "<mi>%s</mi>" % s              # identifier / variable
def mn(s):  return "<mn>%s</mn>" % s              # number
def mo(s):  return "<mo>%s</mo>" % s              # operator
def mtext(s): return "<mtext>%s</mtext>" % s      # words inside math
def upright(s): return "<mi mathvariant='normal'>%s</mi>" % s
def space(em="0.15em"): return "<mspace width='%s'/>" % em

# ---------- structure ----------
def row(*p):    return "<mrow>%s</mrow>" % "".join(p)
def sub(b, s):  return "<msub>%s%s</msub>" % (b, s)
def sup(b, s):  return "<msup>%s%s</msup>" % (b, s)
def subsup(b, s, p): return "<msubsup>%s%s%s</msubsup>" % (b, s, p)
def frac(n, d): return "<mfrac>%s%s</mfrac>" % (row(n), row(d))
def sqrt(x):    return "<msqrt>%s</msqrt>" % row(x)
def root(x, n): return "<mroot>%s%s</mroot>" % (row(x), row(n))

def fn(name):
    """Upright function name with invisible-apply, e.g. fn('sin') + TH."""
    return "<mi>%s</mi><mo>&#8289;</mo><mspace width='0.12em'/>" % name

def vec(sym):
    """Arrow accent over a symbol."""
    return "<mover accent='true'>%s<mo stretchy='false'>&#x2192;</mo></mover>" % sym

def mag(sym):
    """|v-with-arrow|, magnitude of a vector."""
    bar = "<mo stretchy='false' lspace='0' rspace='0'>|</mo>"
    return bar + vec(sym) + bar

def paren(*p):
    # wrapped in an mrow so paren(...) is ONE element: msup/msub/mfrac take a
    # fixed child count, and a bare LP+body+RP silently drops the exponent.
    return "<mrow>%s</mrow>" % (LP + "".join(p) + RP)

# ---------- wrappers ----------
def M(*p):  return '<math display="inline">%s</math>' % "".join(p)
def MB(*p): return '<math display="block">%s</math>' % "".join(p)

# ---------- common tokens ----------
EQ    = mo("=")
PLUS  = mo("+")
MIN   = mo("&#x2212;")                 # U+2212 true minus, never a hyphen
NEG   = '<mo form="prefix" lspace="0" rspace="0">&#x2212;</mo>'
TIMES = mo("&#xD7;")
CDOT  = mo("&#x22C5;")
PROP  = mo("&#x221D;")
APPROX= mo("&#x2248;")
LE, GE = mo("&#x2264;"), mo("&#x2265;")
LP, RP = '<mo stretchy="false">(</mo>', '<mo stretchy="false">)</mo>'

DEL   = upright("&#x394;")             # Delta, upright, it is an operator
TH    = mi("&#x3B8;")                  # theta
PI    = mi("&#x3C0;")
MU    = mi("&#x3BC;")
OMEGA = mi("&#x3C9;")
ALPHA = mi("&#x3B1;")
HALF  = frac(mn("1"), mn("2"))

SIN, COS, TAN = fn("sin"), fn("cos"), fn("tan")

# ---------- stylesheet fragment ----------
CSS = """
math { font-family:"Latin Modern Math","STIX Two Math","Cambria Math","Times New Roman",serif;
       font-size:11.2pt; line-height:1; }
.eqrow { display:flex; align-items:center; gap:7px; min-height:30px;
         padding:1px 0; break-inside:avoid; }
.lbl { font-size:7.3pt; color:#5a6470; line-height:1.15; }
"""

def eqrow(math_html, label=""):
    lab = '<span class="lbl">%s</span>' % label if label else ""
    return '<div class="eqrow">%s%s</div>' % (math_html, lab)
