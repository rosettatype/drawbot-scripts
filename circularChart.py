#-------------------------------------------------------------------------------------------
# Quick and dirty script to draw fancy circular charts with proportional sections
#
# This is a script for DrawBot (http://drawbot.readthedocs.org)
# Requires Git command-line tools installed

import math
from collections import OrderedDict

#totalCaption = "Glyphs"
#unitCaption = "glyphs"
sections = OrderedDict()
sections["Latin"] = 1144
sections["Cyrillic"] = 255
sections["Greek"] = 639
sections["Figures & symbols"] = 332
colors = {}
colors["Latin"] = 127/256, 200/256, 21/256
colors["Cyrillic"] = 72/256, 122/256, 126/256
colors["Greek"] = 69/256, 142/256, 205/256
colors["Figures & symbols"] = 216/256, 216/256, 216/256

outerRadius = 160
innerRadius = 100
gap = 6
margin = 10
thickness=outerRadius-innerRadius
width=outerRadius*2+margin*2
center=(width/2,width/2)
total = sum(sections.values())
print total, sections.values()

newPage(width, width)
last=(outerRadius*2+margin, width/2)
lastAngle=0
for name, number in sections.items():
    save()
    angle=number/total*360
    print name, angle
    
    # path
    path = BezierPath()
    path.moveTo(center)
    path.lineTo(last)
    path.arc(center, outerRadius, lastAngle, lastAngle+angle, clockwise=False)
    path.closePath()
    
    clipPath(path)
    stroke(None)
    fill(*colors[name])
    oval(margin, margin, outerRadius*2, outerRadius*2)
    fill(1)
    oval(margin+thickness, margin+thickness, innerRadius*2, innerRadius*2)
    restore()
    
    stroke(1)
    strokeWidth(gap)
    fill(None)
    drawPath(path)
    last=path.onCurvePoints[-2]
    lastAngle+=angle
    

stroke(None)
fill(1)
oval(margin+thickness, margin+thickness, innerRadius*2, innerRadius*2)