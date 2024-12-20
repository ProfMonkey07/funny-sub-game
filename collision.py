#a line is a set of two points in the format [(x1,y1),(x2,y2)]
#c1 and c2 are both distinct lines
#make sure that x1, y1 is the leftmost point just incase
def collides(c1, c2):
    #calculate the slope and start of each line
    m1 = (c1[1][1]-c1[0][1])/(c1[1][0]-c1[0][0])
    b1 = c1[0][1]


    m2 = (c2[1][1]-c2[0][1])/(c2[1][0]-c2[0][0])
    b2 = c2[0][1]

    #returns the x value of their collision if it occurs
    #print(m1, m2)
    #print(b1, b2)
    pt = (b2-b1)/(m1-m2)
    if pt <= c1[1][0] and pt >= c1[0][0] and pt <= c2[1][0] and pt >= c2[0][0]:
        return True
    else:
        return False
