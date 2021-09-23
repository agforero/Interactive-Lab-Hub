def getColors():
    ret = []
    
    WHI = "#FFFFFF"
    RED = "#FF0000"
    ORA = "#FFA500"
    YEL = "#FFFF00"
    GRE = "#00FF00"
    BLU = "#0000FF"
    PUR = "#AA00AA"

    # white
    ret.append([WHI for _ in range(6)])

    # red
    ret.append([RED for _ in range(6)])

    # orange
    ret.append([ORA for _ in range(6)])

    # yellow
    ret.append([YEL for _ in range(6)])
    
    # green
    ret.append([GRE for _ in range(6)])
    
    # blue
    ret.append([BLU for _ in range(6)])
    
    # purple
    ret.append([PUR for _ in range(6)])

    # rainbow
    ret.append([RED, ORA, YEL, GRE, BLU, PUR])

    return ret
