import pygame


class InputBox:
    def __init__(self, x, y, textlen, value="", size=16, background_color=(255,255,255), is_on=True):
        self.x1 = x
        self.y1 = y
        self.x2 = x + size * textlen
        self.y2 = y + size
        self.text = value
        self.textlen = textlen
        self.size = size
        self.bg_color = background_color
        self.is_on = is_on
    
    def update(self):
        if not self.is_on: return  # If we are not showing this InputBox, just doing nothing
        
        buttons_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] in range(self.x1, self.x2) and mouse_pos[1] in range(self.y1, self.y2) and buttons_pressed[0]:  # Checking for mouseclick on the InputBox
            self.text = inputText(self.x1, self.y1, self.textlen, self.text, size=self.size, background_color=self.bg_color, outline_color=(255,0,0))  # If the box is clicked, going to the input func and updating the text in InputBox
        drawText(self.x1, self.y1, self.text, text_size=self.textlen, size=self.size, background_color=self.bg_color)  # Every iteration (or after text input) drawing the textbox


def keyToSym(key):
    keys_dict = {256: '0', 257: '1', 258: '2', 259: '3', 260: '4', 261: '5', 262: '6', 263: '7', 264: '8', 265: '9', 266: '.', 267: '/', 268: '*', 269: '-', 270: '+', 272: '=', 32: " ", 33: '!', 34: '"', 35: '#', 36: '$', 38: '&', 39: '"', 40: '(', 41: ')', 42: '*', 43: '+', 44: ',', 45: '-', 46: '.', 47: '/', 48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 58: ':', 59: ';', 60: '<', 61: '=', 62: '>', 63: '?', 64: '@', 91: '[', 92: '\\', 93: ']', 94: '^', 95: '_', 96: '`', 97: 'a', 98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f', 103: 'g', 104: 'h', 105: 'i', 106: 'j', 107: 'k', 108: 'l', 109: 'm', 110: 'n', 111: 'o', 112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u', 118: 'v', 119: 'w', 120: 'x', 121: 'y', 122: 'z'}
    if key in keys_dict: return keys_dict[key]  # If the key is in the dict we are returning it's value
    else: return ""  # Else we are returning nothing


def checkShift(sym, shiftPressed=0):
    alph = "abcdefghijklmnopqrstuvwxyz-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_)!@#$%^&*(.,/ "
    withShift = 37  # If shift is pressed and key = a[i] then it will be a[i + withShift]. E.g. "a"->"A", "-"->"_"_
    if sym not in alph or sym == "": return ""
    return alph[alph.index(sym) + withShift * shiftPressed]  # Returning a[i + withShift] is shift is pressed, else - a[i] (sym without changes)


def drawSym(x, y, sym, size, font_path):
    font = pygame.image.load("fonts/" + font_path)  # Opening the font file
    alph = "abcdefghijklmnopqrstuvwxyz-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_)!@#$%^&*(.,/ "
    idx = alph.index(sym)
    font = pygame.transform.scale(font, (len(alph) * size, size))  # Scaling the fonå to size
    screen.blit(font, (x, y), (size * idx, 0, size, size))  # Slicing the font file, so that only one symbol is left


def drawText(x, y, text, text_size=False, outline_width=4, size=16, background_color=(255,255,255), outline_color=(100,100,100), font_path="en.png"):
    text = text.split('\n')  # Spliting text into lines
    if not text_size: text_size = (max([len(text[i].strip()) for i in range(len(text))]), len(text))  # Calc-ing W and H for text box in symblos
    else: text_size = (text_size, 1)  # Or, if text is one line and textlen given, creating text_size with W = textlen and H = 1 (because 1 line)
    
    inner_size = (text_size[0] * size, text_size[1] * size)  # The size of the text background
    outer_size = (inner_size[0] + outline_width * 2, inner_size[1] + outline_width * 2)  # The size of the text+outline background
    
    bg_text = Surface(outer_size)   # Creating the text surface
    bg_text.fill(background_color)  #     and filling it with background_color
    
    draw.rect(bg_text, outline_color, (0, 0, outer_size[0], outer_size[1]), outline_width * 2 - 1)  # Creating the outline
    screen.blit(bg_text, (x - outline_width, y - outline_width))  # Drawing the text surface on the screen

    for line_idx, line in enumerate(text):
        for sym_idx, sym in enumerate(line.strip()):
            drawSym(x + sym_idx * size, y + line_idx * size, sym, size, font_path)  # Drawing a symbol 'sym_idx' on line 'line_idx'
            
    pygame.display.update()  # Updating the display


def inputText(x, y, textlen, value="", outline_width=4, size=16, background_color=(255,255,255), outline_color=(100,100,100), font_path="en.png"):
    cur_text = value  # Sort of a placeholder. The text that is displayed by default.
    while True:
        for e in pygame.event.get(): 
            if e.type == QUIT:
                os._exit(0)
            if e.type == KEYDOWN:
                keys_pressed = key.get_pressed()
                if e.key == K_BACKSPACE:  # If pressed key is backspace, then removing the last symbol from the text
                    cur_text = cur_text[:-1]
                elif e.key == K_RETURN:  # If pressed key is return, then we are stoping the cycle and returning the text.
                    return cur_text
                elif len(cur_text) < textlen:  #Else we are adding symbol to the current text (and checking, if that symbol is pressed with Shift key)
                    cur_text += checkShift(keyToSym(e.key), keys_pressed[K_LSHIFT])
        drawText(x, y, cur_text, textlen, outline_width, size, background_color, outline_color, font_path)  # Each iteration redrawing the text

