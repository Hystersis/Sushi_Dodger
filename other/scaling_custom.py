def scalingx(screen,screen_width = None,screen_height = None):
    # Details form https://tanalin.com/en/articles/integer-scaling/#h-algorithm
    screen = pygame.surfarray.pixels2d(screen)
    print('Inital screen size:',screen.shape[0], screen.shape[1])
    screen = np.array(screen) # This line doesn't create the error
    print('Np screen size:',screen.shape[0], screen.shape[1])
    print("Start screen:",screen)
    w, h = screen.shape[0], screen.shape[1]
    print('w & h',w,h)
    info = pygame.display.Info()
    sw = info.current_w if screen_width == None else screen_width
    sh = info.current_h if screen_height == None else screen_height # This line and above don't make error
    print('sw & sh',sw,sh)
    mrx, mry = int(np.floor(sw / w)), int(np.floor(sh / h)) # One error in this line
    print(mrx,mry)
    r = min(mrx,mry)
    uw, uh = w * r, h * r
    nscreen = np.zeros((uw,uh))
    for y in enumerate(screen):
        # print('Y:',y[1],y[0])
        for x in enumerate(y[1]):
            fx = m(x[0],r)
            fy = m(y[0],r)
            # print(x[1],"\'s x value:",x[0],"\tFx value:",fx,"\tFy value:",fy)
            nscreen[y[0]+fy:y[0]+r+fy,x[0] + fx:x[0]+r+fx] = x[1]
            print(y[0]+fy,y[0]+r+fy,x[0] + fx,x[0]+r+fx,x[1])
    print("Scaled screen:",screen)
    screen = pygame.surfarray.make_surface(nscreen)
    return screen

def m(xy,r):
    return r - 1  if xy > 0 else 0
