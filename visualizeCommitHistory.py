#-------------------------------------------------------------------------------------------
# Script to visualize commit history in a colour-coded graph (one colour per contributor)
# with years and project milestones as labels
#
# This is a script for DrawBot (http://drawbot.readthedocs.org)
# Requires Git command-line tools installed


import os, os.path, sys, time
from collections import OrderedDict
from subprocess import check_output


#-------------------------------------------------------------------------------------------
# Requires Git command-line tools installed


#-------------------------------------------------------------------------------------------
# Settings

# path to repo
repopath = "~/Rosetta/Typefaces (retail)/SkolarSans/"

# commit square grid
rows = 10
side = 12
gutter = 2
margin = side

# colour palette used
colors = {}
colors["A"] = 74/256, 144/256, 226/256
colors["B"] = 189/256, 16/256, 224/256
colors["C"] = 245/256, 166/256, 35/256

legend = "Skolar Sans designers and their Git commits (versions) in time:"
legendWidth = 24 # number of columns

labelFont = "InputMonoCompressed-Medium"

# author -> colour mapping
authors = {}
authors["david"] = colors["A"]
authors["slava"] = colors["B"]
authors["rafael"] = colors["C"]

# real names
realAuthors = OrderedDict()
realAuthors["david"] = "David Březina"
realAuthors["slava"] = "Sláva Jevčinová"
realAuthors["rafael"] = "Rafael Saraiva"

# list of milestones shown as labels above the years(not optimized for collisions, sorry)
milestones = {}
milestones["Latin"] = ("23 Oct 2012", "17 Dec 2014")
milestones["Cyrillic"] = ("17 Dec 2014", "28 Sep 2015")
milestones["Greek"] = ("16 Mar 2015", "20 Dec 2015")



#-------------------------------------------------------------------------------------------
# Main act


for label, (start, end) in milestones.items():
    milestones[label] = (time.strptime(start, '%d %b %Y'), time.strptime(end, '%d %b %Y'))

def coord(x):
    return x * side + x * gutter + margin
    
def drawCommit(x, y, author):
    """
    Draws rectangle corresponsing to a commit by an author.
    """

    x = coord(x)
    y = coord(y)
    for name in authors:
        if name in author:
            color = authors[name]
    fill(*color)
    rect(x, y, side, side)

def drawLabel(x1, x2, y=0, label="", color=(0.5)):
    """
    Draws line and a label
    """

    x1 = coord(x1)
    x2 = coord(x2)
    y = coord(y)
    stroke(*color)
    strokeWidth(2)
    fill(*color)
    line((x1, y), (x2, y))
    stroke(None)
    fill(*color)
    font(labelFont)
    fontSize(9)
    textBox(label, (x1, y, x2-x1, 15), align="center")   

def getCommits(path):
    """
    Returns a list of commits for a Git repo on given path.
    """

    f = check_output(["cd '%s'; git rev-list --all --date-order --pretty" % os.path.expanduser(path)], shell=True)
    print f
    commits = []
    commitRecord = []
    for line in f.split("\n"):
        if "Author" in line:
            if len(commitRecord) > 1:
                commits.append(tuple(commitRecord))
            commitRecord = [line.replace("Author:","").strip().lower()]
        elif "Date:" in line:
            dateString = line.replace("Date:","").strip()
            commitRecord.append(time.strptime(dateString[:-6], '%a %b %d %H:%M:%S %Y'))
    if commitRecord:
        commits.append(tuple(commitRecord))

    return commits

def main():
        i = 0
        records = []
        years = {}
        labels = {}
            
        # analyse commits
        commits = getCommits(repopath)
        for author, tm in sorted(commits, key=lambda r: r[1]):
            x = int(i / rows)
            i += 1
            # track label positions
            years[tm[0]] = x
            for ln in milestones:
                if tm >= milestones[ln][0] and (ln not in labels):
                    labels[ln] = (x, 0)
                if tm <= milestones[ln][1] and (ln in labels):
                    labels[ln] = (labels[ln][0], x)
        
        pageWidth = len(commits)/rows*(side+gutter)-gutter+2*margin
        pageHeight = (rows+len(milestones)+7)*(side+gutter)-gutter+2*margin
        newPage(pageWidth, pageHeight)
        # draw legend
        x = 0
        font(labelFont)
        fontSize(9)
        fill(.3)
        box = textSize(legend)
        textBox(legend, (coord(0), margin, box[0], box[1]))
        x = legendWidth
        for author in realAuthors:
            drawCommit(x, 0, author)
            box = textSize(realAuthors[author])
            stroke(None)
            textBox(realAuthors[author], (coord(x)+side+gutter*2, margin, box[0], box[1])) 
            x += 8 # distance between commit squares and names in grid units
        # draw commits
        i = 0
        for author, tm in sorted(commits, key=lambda r: r[1]):
            x = int(i / rows)
            y = 2 + i % rows
            drawCommit(x, y, author)
            i += 1       
        # draw year labels
        x_old = 0
        i = 0
        for year, x in sorted(years.items(), key=lambda r: r[0]):
            i += 1
            drawLabel(x_old, x+1, 2+rows+1+i%2, str(year), colors["A"])
            x_old = x
        # draw milestone labels
        i = 3
        for ln in labels:
            i += 1
            drawLabel(*labels[ln], y=2+rows+i, label=ln, color=colors["B"])

if __name__ == "__main__":
    main()
