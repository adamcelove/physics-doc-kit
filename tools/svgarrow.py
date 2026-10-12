# -*- coding: utf-8 -*-
"""Canonical SVG arrowheads for vector figures. Dependency-free.

Two rules make an arrow look right, and both are easy to get wrong:

1. **The head is symmetric about its own axis.** Base from (0,0) to (0,2h),
   tip at (len,h), and `refY = h`. If the tip's y and the base's midpoint
   disagree, one barb comes out longer than the other.

2. **The shaft stops at the base of the head.** A shaft drawn all the way to
   the vector's endpoint still carries its full stroke width where the triangle
   has tapered to nothing, so its blunt end pokes out around the point and the
   arrow looks hooked or spiked. `refX = 0` puts the head's base on the line's
   endpoint and projects the point forward, and `Head.line()` shortens the
   shaft by exactly the head's length so the two meet flush.

Give any stroke that carries a head `stroke-linecap: butt`; a round cap adds a
blob past the point.

    head = Head("ah")
    svg += "<defs>%s</defs>" % head.defs()
    svg += head.line(x0, y0, x1, y1, stroke_w=2.6, cls="vec")

The arrow spans the full vector: shaft plus head equals the true length, so the
point lands exactly on (x1, y1) and the figure stays measurable.
"""

LENGTH = 3.6      # arrowhead length, in stroke widths
HALF = 1.4        # arrowhead half-width, in stroke widths


class Head(object):
    """One arrowhead marker definition and the shafts that feed it."""

    def __init__(self, mid, fill="#111", length=LENGTH, half=HALF,
                 units="strokeWidth"):
        self.mid = mid
        self.fill = fill
        self.length = float(length)
        self.half = float(half)
        self.units = units          # "strokeWidth" (scales with the line) or
                                    # "userSpaceOnUse" (a fixed size)

    def defs(self):
        return ('<marker id="%s" markerUnits="%s" markerWidth="%.2f" '
                'markerHeight="%.2f" refX="0" refY="%.2f" orient="auto">'
                '<path d="M0,0 L%.2f,%.2f L0,%.2f z" fill="%s"/></marker>'
                % (self.mid, self.units, self.length, 2 * self.half, self.half,
                   self.length, self.half, 2 * self.half, self.fill))

    def head_len(self, stroke_w):
        """Length of the head in user units."""
        return self.length * stroke_w if self.units == "strokeWidth" else self.length

    def base(self, x0, y0, x1, y1, stroke_w):
        """Where the shaft must stop: the base of the head."""
        dx, dy = x1 - x0, y1 - y0
        seg = (dx * dx + dy * dy) ** 0.5
        if seg == 0:
            return x1, y1
        head = self.head_len(stroke_w)
        if head >= seg:             # arrow shorter than its own head
            head = seg * 0.9
        return x1 - head * dx / seg, y1 - head * dy / seg

    def line(self, x0, y0, x1, y1, stroke_w, cls=None, extra=""):
        """A vector whose point lands exactly on (x1, y1)."""
        bx, by = self.base(x0, y0, x1, y1, stroke_w)
        return ('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"%s%s '
                'marker-end="url(#%s)"/>'
                % (x0, y0, bx, by,
                   ' class="%s"' % cls if cls else '',
                   (' ' + extra) if extra else '', self.mid))


_serial = [0]


def auto(prefix="ah", **kw):
    """A Head with an id unique to this run, so several figures in one document
    never collide on a marker id."""
    _serial[0] += 1
    return Head("%s%d" % (prefix, _serial[0]), **kw)


def defs(*heads):
    """Wrap any number of Head definitions in a single <defs> block."""
    return '<defs>%s</defs>' % ''.join(h.defs() for h in heads)
