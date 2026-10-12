# -*- coding: utf-8 -*-
"""Example worksheet: horizontal launch, built to the physics-doc-kit standards.

    python3 build.py        # writes worksheet.html next to this file

One file holds the blank printable AND its answer key. Answers are `.ans`
elements hidden until `body.key`; the Answer key button (or ?key in the URL)
turns them on. Edit this builder, never the generated HTML.
"""
import importlib.util
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, "..", "..", "tools")
sys.path.insert(0, TOOLS)
import svgarrow  # noqa: E402
from mathml import M as MI  # noqa: E402
from mathml import (CSS as MATHCSS, EQ, DEL, HALF, NEG, PLUS, TIMES,  # noqa: E402
                    frac, mi, mn, mo, mtext, paren, row, sqrt, sub, sup)
SPAREN = lambda *p: row("<mo>(</mo>", *p, "<mo>)</mo>")   # stretches around a fraction
BAR = '<mo fence="true" stretchy="false">|</mo>'
ATAN = sup(mi("tan"), mn("&#x2212;1")) + mo("&#8289;")
TH = mi("&#x3B8;")

_spec = importlib.util.spec_from_file_location(
    "add_key_toggle", os.path.join(TOOLS, "add-key-toggle.py"))
toggle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(toggle)

OUT = os.path.join(HERE, "worksheet.html")
G = 9.80                                   # m/s^2, magnitude, directed downward

# ------------------------------------------------------------ math helpers
NB = "&#xA0;"
XI, YI = row(mi("x"), mo(","), mi("i")), row(mi("y"), mo(","), mi("i"))
VXI = sub(mi("v"), XI); VYI = sub(mi("v"), YI)
VX, VY = sub(mi("v"), mi("x")), sub(mi("v"), mi("y"))
VYF = sub(mi("v"), row(mi("y"), mo(","), mi("f")))
AX, AY = sub(mi("a"), mi("x")), sub(mi("a"), mi("y"))
DX, DY, T = DEL + mi("x"), DEL + mi("y"), mi("t")
SQ = lambda s: sup(s, mn("2"))
MPS2 = sup(mtext(NB + "m/s"), mn("2"))


def q(n, unit, neg=False, sq=False):
    """A parenthesised value with its unit attached, for the plug-in step."""
    u = MPS2 if unit == "m/s2" else mtext(NB + unit)
    return paren((NEG if neg else "") + mn(n) + u)


PLUSS = '<mo form="prefix" lspace="0" rspace="0">+</mo>'


def res(n, unit, word, neg=False, pos=False):
    """The final value, highlighted, with its direction word."""
    u = MPS2 if unit == "m/s2" else mtext(("" if unit.startswith("&#xB0;") else NB) + unit)
    return ('<span class="fill">%s</span>'
            % M((NEG if neg else PLUSS if pos else "") + mn(n) + u + (mtext(NB + "(" + word + ")") if word else "")))


def M(*p):
    """Inline MathML in display style, so fractions in radicals and arguments stay full size."""
    return '<math display="inline"><mstyle displaystyle="true">%s</mstyle></math>' % "".join(p)


def step(label, *inner):
    return '<span class="steplab">%s</span><div class="calc">%s</div>' % (label, "".join(inner))


def calc(label, math_html, tail=""):
    return step(label, M(math_html) + tail)


# --------------------------------------------------------------- the physics
def solve(vx, h, rng=None):
    """Everything both the figures and the key quote, from one set of numbers."""
    t = math.sqrt(2 * h / G)
    vy = G * t
    return dict(vx=vx, h=h, t=t, vy=vy, R=vx * t, speed=math.hypot(vx, vy),
                ang=math.degrees(math.atan2(vy, vx)))


def f3(x):
    """Three significant figures, trailing zeros kept (12.0, not 12)."""
    return "{:#.3g}".format(x).rstrip(".")


# -------------------------------------------------------------------- SVG
CSS_SVG = """
svg text{font:9.5px Arial;fill:#111;paint-order:stroke;stroke:#fff;stroke-width:2.6px;stroke-linejoin:round}
.gl{stroke:#e2e2e2;stroke-width:.6}.ax{stroke:#222;stroke-width:1.4}.gm{stroke:#bdbdbd;stroke-width:.9}
.pg{stroke:#9a9a9a;stroke-width:1.4;fill:none;stroke-dasharray:5 4}
.vec{stroke:#1F5FBF;stroke-width:2.1;stroke-linecap:butt}
.acc{stroke:#2E8B57;stroke-width:2.4;stroke-linecap:butt}
.pos{stroke:#222;stroke-width:1.6;stroke-linecap:butt}
.vx{stroke:#11AC33;stroke-width:2.2;stroke-dasharray:6 3;fill:none}
.vyl{stroke:#A60156;stroke-width:2.2;fill:none}
.vdrop{stroke:#fff;stroke-width:1.2;stroke-dasharray:5 5;fill:none}
svg text.mut{font-size:8px;fill:#555}svg text.tk{fill:#555}
svg.sit{width:3.4in}svg.sit text{font-size:11px}svg.sit text.mut{font-size:9.5px}svg.md{width:4.75in;height:3in}svg.vt{width:4in;height:2.63in}
"""
VEL = svgarrow.Head("ahv", fill="#1F5FBF", length=9, half=3.5, units="userSpaceOnUse")
ACC = svgarrow.Head("aha", fill="#2E8B57", length=9, half=3.5, units="userSpaceOnUse")
POS = svgarrow.Head("ahp", fill="#222", length=8, half=3, units="userSpaceOnUse")
DEFS = svgarrow.defs(VEL, ACC, POS) + (
    '<pattern id="hat%s" width="6" height="6" patternUnits="userSpaceOnUse" '
    'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#999" '
    'stroke-width="1"/></pattern>')
def SUB(base, sub_, rest=""):
    """SVG label with a subscript; the step back up sits on the text that follows."""
    return '%s<tspan dy="2" font-size="8">%s</tspan><tspan dy="-2">%s</tspan>' % (base, sub_, rest or "&#8203;")
_n = [0]


def ticks_y(v):
    return ("&#8722;%g" % abs(v)) if v < 0 else "%g" % v


def situation_fig(d, tag, vlabel, with_range):
    """The blank-state figure: cliff, launch arrow, height marker, optional range."""
    _n[0] += 1; k = "s%d" % _n[0]
    H = 172 if with_range else 150
    ox, top, gnd = 78, 34, 134
    rx = ox + (gnd - top) * d["R"] / d["h"]          # to scale: range : height as in the problem
    s = ['<svg viewBox="0 0 260 %d" class="sit" style="height:%.2fin" data-fig-role="diagram">'
         % (H, 3.4 * H / 260), DEFS % k]
    s.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#hat%s)"/>' % (top, ox, gnd - top + 8, k))
    s.append('<rect x="%d" y="%d" width="%d" height="8" fill="url(#hat%s)"/>' % (ox, gnd, 250 - ox, k))
    s.append('<polyline points="0,%d %d,%d %d,%d 250,%d" fill="none" class="ax"/>'
             % (top, ox, top, ox, gnd, gnd))
    pts = ["%.1f,%.1f" % (ox + (rx - ox) * u / 40, top + (gnd - top) * (u / 40) ** 2) for u in range(41)]
    s.append('<polyline class="pg" points="%s"/>' % " ".join(pts))
    s.append('<circle cx="%d" cy="%d" r="4" fill="#111"/>' % (ox, top))
    s.append('<circle cx="%d" cy="%d" r="4" fill="#fff" stroke="#111" stroke-width="1.4"/>' % (rx, gnd))
    s.append(VEL.line(ox + 6, top - 12, ox + 52, top - 12, 2.1, cls="vec"))
    s.append('<text x="%d" y="%d">%s</text>' % (ox + 6, top - 18, vlabel))
    mid = (top + gnd) / 2
    s.append(POS.line(ox + 14, mid, ox + 14, top, 1.6, cls="pos"))
    s.append(POS.line(ox + 14, mid, ox + 14, gnd, 1.6, cls="pos"))
    s.append('<text x="%d" y="%d">%.1f m</text>' % (ox + 20, mid + 3, d["h"]))
    if with_range:
        yb = gnd + 20
        for x in (ox, rx):
            s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#999" stroke-dasharray="2 2"/>'
                     % (x, gnd + 8, x, yb + 4))
        s.append(POS.line((ox + rx) / 2, yb, ox, yb, 1.6, cls="pos"))
        s.append(POS.line((ox + rx) / 2, yb, rx, yb, 1.6, cls="pos"))
        s.append('<text x="%d" y="%d" text-anchor="middle">%.1f m</text>' % ((ox + rx) / 2, yb + 13, d["R"]))
    s.append('<text x="4" y="%d" class="mut">%s</text></svg>' % (top - 6, tag))
    return "".join(s)


def motion_diagram(d, what):
    """Dots at equal time steps, a velocity arrow on each, a separate acceleration."""
    _n[0] += 1; k = "m%d" % _n[0]
    vx, h, R, T_ = d["vx"], d["h"], d["R"], d["t"]
    sc, varr, ox, oy = min(160 / R, 140 / h), 1.2, 50, 34
    gy = oy + h * sc
    X = lambda m: ox + m * sc
    Y = lambda m: oy - m * sc            # y in metres, up is positive
    s = ['<svg viewBox="0 0 380 240" class="md" data-fig-role="diagram">', DEFS % k]
    s.append('<rect x="%d" y="%.1f" width="%.1f" height="8" fill="url(#hat%s)"/>' % (ox - 40, gy, R * sc + 80, k))
    s.append('<rect x="%d" y="%d" width="40" height="%.1f" fill="url(#hat%s)"/>' % (ox - 40, oy, gy - oy, k))
    s.append('<polyline points="%d,%d %d,%d %.1f,%.1f" fill="none" class="ax"/>'
             % (ox - 40, oy, ox, oy, ox, gy))
    s.append('<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" class="ax"/>' % (ox, gy, ox + R * sc + 40, gy))
    path = ["%.1f,%.1f" % (X(vx * T_ * u / 60), Y(-0.5 * G * (T_ * u / 60) ** 2)) for u in range(61)]
    s.append('<polyline class="pg" points="%s"/>' % " ".join(path))
    dots = []
    if d.get("dropped"):                     # second column: the car dropped from rest, straight down
        cx = ox + 12
        s.append('<text x="%d" y="%d">dropped: v = 0</text>' % (ox - 34, oy - 8))
        for i in range(1, 5):               # dot 0 is the shared launch point
            t = T_ * i / 5
            py, vy = Y(-0.5 * G * t * t), G * t
            s.append(VEL.line(cx, py + 4.5, cx, py + vy * varr, 2.1, cls="vec"))
            dots.append('<circle cx="%d" cy="%.1f" r="3.4" fill="#777" stroke="#fff" stroke-width="1.2"/>' % (cx, py))
        s.append('<text x="%d" y="%.1f">dropped car</text>' % (cx + 8, Y(-0.5 * G * (0.8 * T_) ** 2) + 3))
    for i in range(5):                      # t = 0, T/5, ..., 4T/5: every dot clears the ground
        t = T_ * i / 5
        px, py, vy = X(vx * t), Y(-0.5 * G * t * t), -G * t
        ux, uy = vx * varr, -vy * varr
        n = math.hypot(ux, uy)
        sx, sy = px + 4.5 * ux / n, py + 4.5 * uy / n
        s.append(VEL.line(sx, sy, px + ux, py + uy, 2.1, cls="vec"))
        dots.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="#111" stroke="#fff" stroke-width="1.2"/>' % (px, py))
        if i == 4:
            s.append('<text x="%.1f" y="%.1f">v</text>' % (px + ux + 5, py + uy + 3))
    s += dots
    s.append('<text x="%d" y="%.1f" class="mut">%s</text>' % (ox - 38, gy + 20, what))
    lx = 300                                 # right panel: chosen directions, then acceleration
    s.append(POS.line(lx, 70, lx, 44, 1.4, cls="pos")); s.append(POS.line(lx, 70, lx + 26, 70, 1.4, cls="pos"))
    s.append('<text x="%d" y="38" text-anchor="middle">+y (up)</text>' % lx)
    s.append('<text x="%d" y="74">+x (right)</text>' % (lx + 30))
    s.append('<text x="%d" y="88" class="mut" text-anchor="middle">directions I chose</text>' % lx)
    s.append('<text x="%d" y="118" text-anchor="middle">%s</text>' % (lx, SUB("a", "y", " = &#8722;9.80 m/s&#178;")))
    s.append('<text x="%d" y="130" text-anchor="middle">(downward)</text>' % lx)
    s.append(ACC.line(lx, 138, lx, 184, 2.4, cls="acc"))
    s.append('<text x="%d" y="204" text-anchor="middle">%s</text>' % (lx, SUB("a", "x", " = 0")))
    s.append('<text x="%d" y="216" class="mut" text-anchor="middle">same at every dot</text></svg>' % lx)
    return "".join(s)


def vt_graph(d, tmax, vmin, vmax, vstep):
    """v_x and v_y against time; both axes numbered with units."""
    w, h, ml, mt, mr, mb = 320, 210, 46, 14, 14, 30
    pw, ph = w - ml - mr, h - mt - mb
    X = lambda t: ml + pw * t / tmax
    Y = lambda v: mt + ph * (1 - (v - vmin) / (vmax - vmin))
    s = ['<svg viewBox="0 0 %d %d" class="vt" data-fig-role="graph">' % (w, h)]
    for i in range(int(tmax / 0.5) + 1):
        t = i * 0.5
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" class="gl"/>' % (X(t), mt, X(t), mt + ph))
        s.append('<text x="%.1f" y="%d" class="tk" text-anchor="middle">%g</text>' % (X(t), mt + ph + 12, t))
    v = vmin
    while v <= vmax + 1e-9:
        s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" class="gl"/>' % (ml, Y(v), ml + pw, Y(v)))
        s.append('<text x="%d" y="%.1f" class="tk" text-anchor="end">%s</text>' % (ml - 4, Y(v) + 3.5, ticks_y(v)))
        v += vstep
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="ax"/>' % (ml, mt, ml, mt + ph))
    s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" class="ax"/>' % (ml, Y(0), ml + pw, Y(0)))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="vx"/>' % (X(0), Y(d["vx"]), X(d["t"]), Y(d["vx"])))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="vyl"/>' % (X(0), Y(0), X(d["t"]), Y(-d["vy"])))
    if d.get("dropped"):                     # same v_y line: drawn dashed on top, labeled apart
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="vdrop"/>' % (X(0), Y(0), X(d["t"]), Y(-d["vy"])))
        s.append('<text x="%.1f" y="%.1f">%s</text>' % (X(d["t"] / 2) + 8, Y(-d["vy"] / 2) - 6, SUB("v", "y", ", dropped car")))
    s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#999" stroke-dasharray="2 3"/>'
             % (X(d["t"]), mt, X(d["t"]), mt + ph))
    s.append('<text x="%.1f" y="%.1f">%s</text>' % (X(0.1), Y(d["vx"]) - 6, SUB("v", "x", " = +%s m/s (right)" % f3(d["vx"]))))
    s.append('<text x="%.1f" y="%.1f" text-anchor="end">%s</text>' % (X(d["t"] / 2) - 6, Y(-d["vy"] / 2) + 6, SUB("v", "y", ", launched car" if d.get("dropped") else "")))
    s.append('<text x="%.1f" y="%d" text-anchor="end">lands, t = %s s</text>' % (X(d["t"]) - 4, mt + 10, f3(d["t"])))
    s.append('<text x="%d" y="%d" text-anchor="middle">time t (s)</text>' % (ml + pw / 2, h - 3))
    s.append('<text x="10" y="%.1f" text-anchor="middle" transform="rotate(-90 10 %.1f)">velocity (m/s)</text>'
             % (mt + ph / 2, mt + ph / 2))
    return "".join(s) + "</svg>"


# ------------------------------------------------------------- page pieces
def sp(lines, trim=0.0):
    """Blank work space: 0.30 in per line + 0.25 in, rounded up to 0.1 in. A negative
    trim hands the page's leftover room to the space; a positive trim is the margin allowance."""
    inches = math.ceil((0.30 * lines + 0.25) * 10 - 1e-9) / 10 - trim
    return '<span class="sp" style="height:%.1fin"></span>' % inches


def part(letter, text, space, answer):
    return ('<div class="part"><p><b>(%s)</b> %s</p>%s<div class="ans"><b class="t">Answer (%s)</b>%s</div></div>'
            % (letter, text, space, letter, answer))


CHOICE = "I chose right as positive for x and up as positive for y."
HLINE = lambda *a: "".join(a)


def E(*p):
    return MI(*p)


def mval(n, unit, word=None, neg=False, pos=False):
    """An inline quantity for prose: number, unit, direction word."""
    u = MPS2 if unit == "m/s2" else mtext(NB + unit)
    return (NEG if neg else PLUSS if pos else "") + mn(n) + u + (mtext(NB + "(" + word + ")") if word else "")


AYV = lambda: E(AY, EQ, mval("9.80", "m/s2", "downward", True))
DYV = lambda d: E(DY, EQ, mval(f3(d["h"]), "m", "downward", True))
ZERO = lambda sym: E(sym, EQ, mn("0"))
TSOL = sqrt(frac(mn("2") + DY, AY))


def fall_time(d):
    return (calc("equation", DY + EQ + VYI + T + PLUS + HALF + AY + SQ(T))
            + "<p>The object leaves horizontally, so %s and the first term is zero.</p>" % ZERO(VYI)
            + calc("solve for the unknown", DY + EQ + HALF + AY + SQ(T) + mo("&#x21D2;") + T + EQ + TSOL)
            + "<p>Plug in %s and %s.</p>" % (DYV(d), AYV())
            + step("plug-in", M(T, EQ, sqrt(frac(mn("2") + q(f3(d["h"]), "m", True), q("9.80", "m/s2", True))), EQ),
                   res(f3(d["t"]), "s", ""))
            + "<p>Both %s and %s are negative, so the ratio is positive. In %s the launch speed %s never appears: "
              "it does not change the fall time.</p>" % (E(DY), E(AY), E(T, EQ, TSOL), E(VXI)))


def key_q1(d):
    t, vy = f3(d["t"]), f3(d["vy"])
    return {
        "a": ("<p>%s The landing point is %s from the launch point, and %s.</p>" % (CHOICE, DYV(d), AYV()))
              + fall_time(d),
        "b": ("<p>%s</p>" % CHOICE
              + calc("equation", DX + EQ + VXI + T + PLUS + HALF + AX + SQ(T))
              + "<p>Nothing pushes the ball sideways, so %s and the equation reduces to %s. It already solves for %s, "
                "so no rearrangement is needed.</p>" % (ZERO(AX), E(DX, EQ, VXI, T), E(DX))
              + step("plug-in", M(DX, EQ, q(f3(d["vx"]), "m/s"), q(t, "s"), EQ), res(f3(d["R"]), "m", "right", pos=True))),
        "c": ("<p>%s The vertical and horizontal motions are separate, so I find each landing component, then "
              "combine them.</p>" % CHOICE
              + calc("equation", VYF + EQ + VYI + PLUS + AY + T)
              + "<p>With %s this already solves for %s.</p>" % (ZERO(VYI), E(VYF))
              + "<p>Plug in %s.</p>" % AYV()
              + step("plug-in", M(VYF, EQ, q("9.80", "m/s2", True), q(t, "s"), EQ), res(vy, "m/s", "downward", True))
              + "<p>The horizontal component is unchanged: %s.</p>" % E(sub(mi("v"), row(mi("x"), mo(","), mi("f"))), EQ,
                                                                      mval(f3(d["vx"]), "m/s", "right", pos=True))
              + calc("equation", mi("v") + EQ + sqrt(SQ(VX) + PLUS + SQ(VY)))
              + "<p>Plug in %s and %s.</p>" % (E(VX, EQ, mval(f3(d["vx"]), "m/s", "right", pos=True)),
                                              E(VY, EQ, mval(vy, "m/s", "downward", True)))
              + step("plug-in", M(mi("v"), EQ, sqrt(SQ(q(f3(d["vx"]), "m/s")) + PLUS + SQ(q(vy, "m/s", True))), EQ),
                     res(f3(d["speed"]), "m/s", ""))
              + "<p>The angle is measured below the horizontal. The vertical leg is opposite that angle and the "
                "horizontal leg is adjacent to it.</p>"
              + calc("equation", mi("tan") + mo("&#8289;") + TH + EQ + frac(mtext("opposite"), mtext("adjacent")))
              + calc("solve for the unknown", TH + EQ + ATAN + SPAREN(frac(BAR + VY + BAR, BAR + VX + BAR)))
              + step("plug-in", M(TH, EQ, ATAN, SPAREN(frac(mn(vy) + mtext(NB + "m/s"), mn(f3(d["vx"])) + mtext(NB + "m/s"))), EQ),
                     res(f3(d["ang"]), "&#xB0;", "below the horizontal, toward the right"))),
    }


def key_q2(d):
    t = f3(d["t"])
    return {
        "a": ("<p>%s The landing point is %s from the launch point, and %s.</p>" % (CHOICE, DYV(d), AYV()))
              + fall_time(d),
        "b": ("<p>%s</p>" % CHOICE
              + calc("equation", DX + EQ + VXI + T + PLUS + HALF + AX + SQ(T))
              + "<p>Nothing pushes the car sideways, so %s and the equation reduces to %s.</p>" % (ZERO(AX), E(DX, EQ, VXI, T))
              + calc("solve for the unknown", VXI + EQ + frac(DX, T))
              + step("plug-in", M(VXI, EQ, frac(q("32.0", "m"), q(t, "s")), EQ), res(f3(d["vx"]), "m/s", "right", pos=True))),
        "c": ("<p>%s The second car starts from rest, so %s. It falls %s with %s: the same numbers as in (a).</p>"
              % (CHOICE, ZERO(VYI), DYV(d), AYV())
              + calc("equation", DY + EQ + VYI + T + PLUS + HALF + AY + SQ(T))
              + "<p>With %s the first term is zero.</p>" % ZERO(VYI)
              + calc("solve for the unknown", DY + EQ + HALF + AY + SQ(T) + mo("&#x21D2;") + T + EQ + TSOL)
              + "<p>Plug in %s and %s.</p>" % (DYV(d), AYV())
              + step("plug-in", M(T, EQ, sqrt(frac(mn("2") + q(f3(d["h"]), "m", True), q("9.80", "m/s2", True))), EQ),
                     res(t, "s", ""))
              + "<p>The two fall times are equal. The time depends only on %s and %s, and both cars have the same values "
                "of each, so sideways motion adds no time in the air.</p>" % (E(DY), E(AY))),
    }


def figs(d, what, tmax, vmin, vmax, vstep, extra=""):
    return ('<div class="figs"><div class="figrow"><div>%s<p class="cap">Motion diagram: one dot every '
            '%s s, from launch to just before landing. %s</p></div><div>%s<p class="cap">Velocity-time graph for the whole flight.</p>'
            '</div></div></div>' % (motion_diagram(d, what), f3(d["t"] / 5), extra,
                                    vt_graph(d, tmax, vmin, vmax, vstep)))


# ------------------------------------------------------------------- build
d1 = solve(12.0, 45.0)
d2 = solve(32.0 / math.sqrt(2 * 20.0 / G), 20.0)   # launch speed from the 32.0 m range
d2["R"] = 32.0
d2["dropped"] = True
assert f3(d1["R"]) == "36.4" and f3(d1["vy"]) == "29.7" and f3(d2["vx"]) == "15.8"
assert f3(32.0 / float(f3(d2["t"]))) == f3(d2["vx"])      # the rounded plug-in line gives the same answer
k1, k2 = key_q1(d1), key_q2(d2)

EQROW = lambda *a: '<div class="eq">%s</div>' % M(*a)
VI, VF = sub(mi("v"), mi("i")), sub(mi("v"), mi("f"))
VLAB = lambda s: SUB("v", "i", " = " + s)

INTRO = (
    '<div class="hdr"><div><h1>Horizontal Launch</h1><p class="sub">Two motions, one clock</p></div>'
    '<div class="nm">Name <span class="line"></span> &nbsp; Date <span class="line s"></span>'
    ' &nbsp; Period <span class="line s"></span></div></div>'
    '<h2 class="first">What a horizontal launch is</h2>'
    '<p>An object is <b>launched horizontally</b> when it leaves a surface moving sideways with no upward or '
    'downward velocity at the start. After that, gravity is the only thing acting on it. The path is a curve, '
    'but the physics is two simple motions that share one clock, the time <i>t</i>.</p>'
    '<table class="tb"><tr><th></th><th>horizontal (x)</th><th>vertical (y)</th></tr>'
    '<tr><td>Starting velocity</td><td>the launch speed, %s</td><td>zero, %s</td></tr>'
    '<tr><td>Acceleration</td><td>zero, %s</td><td>%s, directed downward</td></tr>'
    '<tr><td>Kind of motion</td><td>constant velocity</td><td>free fall from rest</td></tr></table>'
    '<p>The motions are independent; only the time is shared. Find <i>t</i> in one direction, then use it in the other.</p>'
    '<h3>Equations</h3>'
    '<p>The kinematic equations apply separately to each direction. Replace <i>x</i> with <i>y</i> for vertical motion.</p>'
    % (M(VXI), M(VYI), M(AX), M(mval("9.80", "m/s2")))
    + EQROW(DX, EQ, VXI, T, PLUS, HALF, AX, SQ(T))
    + EQROW(VF, EQ, VI, PLUS, mi("a"), T)
    + EQROW(SQ(VF), EQ, SQ(VI), PLUS, mn("2"), mi("a"), DX)
    + '<p>Near Earth&rsquo;s surface, %s, directed downward. A velocity from its components, '
      'and its direction as an angle &theta; from the horizontal:</p>' % M(mi("g"), EQ, mval("9.80", "m/s2"))
    + EQROW(mi("v"), EQ, sqrt(SQ(VX) + PLUS + SQ(VY)))
    + EQROW(mi("tan"), mo("&#8289;"), mi("&#x3B8;"), EQ, frac(mtext("opposite"), mtext("adjacent")))
    + '<h3>How to write a calculation</h3>'
      '<p>Choose a positive direction for each axis and write both at the top of your work. Every value you use '
      'gets its direction in words next to the sign.</p>'
      '<ol><li><b>Equation:</b> the general relationship, in symbols only.</li>'
      '<li><b>Solve for the unknown:</b> rearrange, still in symbols.</li>'
      '<li><b>Plug-in:</b> put each value in with its units, then give the result.</li></ol>'
      '<p>Example: a cart moves at 3.0 m/s to the right for 5.0 s. How far does it go?</p>'
      '<div class="eq">%s</div><div class="eq">%s</div>'
    % (M(DX, EQ, mi("v"), T),
       M(DX, EQ, q("3.0", "m/s"), q("5.0", "s"), EQ, mn("15"), mtext(NB + "m" + NB + "(right)"))))
body = [INTRO]

stem1 = ('<p class="stem">A ball rolls off the edge of a cliff 45.0 m above level ground. It leaves the edge moving '
         'horizontally at 12.0 m/s. It lands on the ground below.</p>')
fig1 = situation_fig(d1, "", VLAB("12.0 m/s"), False)
body.append('<h2>Part 1: a ball off a cliff</h2><div class="qbox"><div class="row"><div>%s</div>%s</div>%s%s%s%s</div>' % (
    stem1, fig1,
    figs(d1, "ground", 3.5, -30, 20, 10),
    part("a", "Find the time the ball is in the air.", sp(4, 0.0), k1["a"]),
    part("b", "Find how far from the base of the cliff the ball lands.", sp(4, 0.0), k1["b"]),
    part("c", "Find the ball&rsquo;s velocity just before it lands: its speed, and its angle and direction in words. "
              "Show the vertical component first.", sp(13, 0.5), k1["c"])))

stem2 = ("<p class=\"stem\">A stunt car drives off a horizontal platform 20.0 m above the ground and lands 32.0 m from the "
         "base of the platform, measured along the ground.</p>")
fig2 = situation_fig(d2, "", VLAB("?"), True)
body.append('<h2>Part 2: a stunt car</h2><div class="qbox"><div class="row"><div>%s</div>%s</div>%s%s%s%s</div>' % (
    stem2, fig2, figs(d2, "ground", 2.5, -20, 20, 10),
    part("a", "Find the time the car is in the air.", sp(4, -0.3), k2["a"]),
    part("b", "Find the speed at which the car left the platform.", sp(4, -0.3), k2["b"]),
    part("c", "A second car is dropped from rest off the same platform at the same instant. It should reach the "
              "ground at the same time as the first car. Check: find its fall time.", sp(4, -0.3), k2["c"])))

CSS = '''
:root{--band:#f2f2f2;--mut:#555}
*{box-sizing:border-box}
body{font:11pt/1.4 "Helvetica Neue",Arial,sans-serif;color:#111;max-width:7.6in;margin:0 auto;padding:.35in .4in;background:#fff}
h1{font-size:15pt;margin:0}.sub{color:var(--mut);font-size:9.5pt;margin:0}
.hdr{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #111;padding-bottom:6px;margin-bottom:10px}
.nm{font-size:10pt}.line{display:inline-block;border-bottom:1px solid #111;min-width:1.7in}.line.s{min-width:.8in}
h2{font-size:11.5pt;margin:0 0 5px;break-before:page;break-after:avoid;padding:3px 7px;background:var(--band);border-left:3px solid #333;text-transform:uppercase;letter-spacing:.04em}
h2.first{break-before:auto;margin-top:6px}
h2+p,h2+div{margin-top:6px}
h3{font-size:11pt;margin:10px 0 3px;text-transform:uppercase;letter-spacing:.04em;border-bottom:1px solid #999}
.qbox{break-inside:avoid}
.row{display:flex;gap:16px;align-items:flex-start}.row>div:first-child{flex:1}
.stem{background:#f7f7f7;padding:8px 11px;border-left:3px solid #888;margin:6px 0}
.part p{margin:6px 0 0}
.sp{display:block}
table.tb{border-collapse:collapse;width:100%;font-size:10pt;margin:8px 0}
.tb th,.tb td{border:1px solid #999;padding:5px 8px;text-align:center}.tb th{background:var(--band)}
.eq{text-align:center;margin:2px 0}.eq math{font-size:12.4pt}
@page{margin:.45in}
@media print{h2,.tb th,.stem,.ans .fill,body.key .ans,#bar button.on{print-color-adjust:exact;-webkit-print-color-adjust:exact}
h2,.tb th{background:#eee!important}}
.ans,.figs{display:none}
body.key .ans{display:block;border-left:3px solid #1a5c3a;background:#f2f8f4;padding:8px 12px;margin:12px 0 20px;color:#14452f;font-size:12pt;line-height:1.6}
body.key .figs{display:block;margin:14px 0 18px}
body.key .sp{display:none}
body.key .part{margin:14px 0}
.ans b.t{display:block;font-size:9.5pt;letter-spacing:.06em;text-transform:uppercase;color:#1a5c3a;margin-bottom:5px}
.ans p{margin:10px 0}
.ans .steplab{display:block;font-size:9pt;letter-spacing:.06em;text-transform:uppercase;color:#6b8f7d;margin:14px 0 1px}
.ans .calc{margin:10px 0;padding:2px 0 2px 10px;border-left:2px solid #cfe3d7;line-height:1.75}
.ans math{font-size:13pt}.ans .calc+.calc{margin-top:12px}
.ans .fill{background:#dcefe3;padding:1px 6px;border-radius:3px;font-weight:700}
.figrow{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}
.cap{font-size:9.5pt;color:#555;margin:3px 0 0;max-width:4.4in}
@media print{.ans,.figs{display:none!important}}
'''
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
        '<title>Horizontal Launch</title><style>%s%s%s</style></head><body>%s</body></html>'
        % (CSS, CSS_SVG, MATHCSS, "".join(body)))
page = toggle.inject(page)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(page)
print("wrote", OUT, "(%d bytes)" % len(page))
