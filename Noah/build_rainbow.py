def build_rainbow(resolution):
    rainbow = []
    num = int(255/(resolution/3))
    
    for i in range(0, 255, num):
        rainbow.append((255-i, i, 0))
        
    for i in range(0, 255, num):
        rainbow.append((0, 255-i, i))
        
    for i in range(0, 255, num):
        rainbow.append((i, 0, 255-i))
        
    return rainbow
