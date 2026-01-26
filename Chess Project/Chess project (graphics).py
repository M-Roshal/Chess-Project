import pygame as pg
from pygame import mixer
import math
import os

pg.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pg.init()

print('Game log')

# Set base path for all assets relative to script location
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_PATH, 'pieces & board')
MUSIC_PATH = os.path.join(BASE_PATH, 'Music & Sounds')

# global variables catalog creation

figures = {  # all chess pieces
    'Wp1' : 'A2', 'Wp2' : 'B2', 'Wp3' : 'C2', 'Wp4' : 'D2', 'Wp5' : 'E2', 'Wp6' : 'F2', 'Wp7' : 'G2', 'Wp8' : 'H2', # white pawns
    'Bp1' : 'A7', 'Bp2' : 'B7', 'Bp3' : 'C7', 'Bp4' : 'D7', 'Bp5' : 'E7', 'Bp6' : 'F7', 'Bp7' : 'G7', 'Bp8' : 'H7', # black pawns
    'Wr1' : 'A1', 'Wr2' : 'H1', # white rooks
    'Br1' : 'A8', 'Br2' : 'H8', # black rooks
    'Wk1' : 'B1', 'Wk2' : 'G1', # white knights
    'Bk1' : 'B8', 'Bk2' : 'G8', # black knights
    'Wb1' : 'C1', 'Wb2' : 'F1', # white bishops
    'Bb1' : 'C8', 'Bb2' : 'F8', # black bishops
    'Wqn' : 'D1', # white queen
    'Bqn' : 'D8', # black queen
    'Wkg' : 'E1', # white king
    'Bkg' : 'E8'  # black king
}

translation = {  # translation of code symbols to words (used for pictures upload)
    'W' : 'white', 'B' : 'black', # colors
    'p' : 'pawn', 'r' : 'rook', 'k' : 'knight', 'b' : 'bishop', 'q' : 'queen', 'kg' : 'king' # pieces
}

vd = {} # variable dictionary

# images upload

for i in figures:
    if 'kg' not in i:
        vd[i] = pg.image.load(os.path.join(ASSETS_PATH, translation[i[0]] + ' pieces', translation[i[0]] + '_' + translation[i[1]] + '.png'))
    else:
        vd[i] = pg.image.load(os.path.join(ASSETS_PATH, translation[i[0]] + ' pieces', translation[i[0]] + '_king.png'))


text_st = pg.font.Font(None, 50)
game_log = text_st.render('The game begins! White to move (Move 1)', True, 'Black')

# sound upload

move_sound = pg.mixer.Sound(os.path.join(MUSIC_PATH, 'Chess move.mp3'))
move_sound.set_volume(2.0)
pg.mixer.music.load(os.path.join(MUSIC_PATH, 'Epic chess beat.mp3'))
pg.mixer.music.play(-1, 0.0, 5000)

# main functions

def background():
    screen.fill('beige')
    background = pg.image.load(os.path.join(ASSETS_PATH, 'wooden_background.jpeg')).convert_alpha()
    background = pg.transform.scale(background, (1920, 1080))
    screen.blit(background, (0, 0))

    game_desk = pg.image.load(os.path.join(ASSETS_PATH, 'Chess Boards', 'Chess Board (grey stone).jpeg')).convert_alpha()
    game_desk = pg.transform.scale(game_desk, (800, 800))
    screen.blit(game_desk, (1000, 200))

    screen.blit(game_log, (740, 75))

def mouse_click_event():
    pos = pg.mouse.get_pos()
    mouse_x = int(pos[0])
    mouse_y = int(pos[1])

    m_j = math.floor((mouse_x - 1000) / 100)
    m_i = math.floor((mouse_y - 200) / 100)

    for i in figures:
        coordinates = figures[i]
        if coordinates != '-':
            pos_j = int((ord(coordinates[0]) - 65))
            pos_i = 8 - int(coordinates[1])

            if m_j == pos_j and m_i == pos_i:
                print(i, mouse_x, mouse_y, m_j, m_i)
                return(i)
    return('')
            
def mouse_release_event():
    global move
    global selected_piece
    global game_log
    kj = False
    mm = False
    fl = False
    pos = pg.mouse.get_pos()
    mouse_x = int(pos[0])
    mouse_y = int(pos[1])

    m_j = math.floor((mouse_x - 1000) / 100)
    m_i = math.floor((mouse_y - 200) / 100)

    if selected_piece != '':
        np_i = 8 - int(figures[selected_piece][1])
        np_j = int((ord(figures[selected_piece][0]) - 65))
        if 'k' in selected_piece and ('kg' not in selected_piece): kj = True
        if walls_crossing(m_i, m_j, np_i, np_j) == True or kj == True:
            if 'p' in selected_piece: fl = pawn_moves(m_i, m_j, np_i, np_j)
            if 'r' in selected_piece: fl = rook_moves(m_i, m_j, np_i, np_j)
            if 'k' in selected_piece and ('kg' not in selected_piece): fl = knight_moves(m_i, m_j, np_i, np_j)
            if 'b' in selected_piece: fl = bishop_moves(m_i, m_j, np_i, np_j)
            if 'q' in selected_piece: fl = queen_moves(m_i, m_j, np_i, np_j)
            if 'kg' in selected_piece: fl = king_moves(m_i, m_j, np_i, np_j)

            if move % 2 != 0 and selected_piece[0] == 'W': mm = True
            if move % 2 == 0 and selected_piece[0] == 'B': mm = True

            if mm == False:
                game_log = text_st.render('Another player is supposed to move now', True, 'Black')

            if taking_pieces(m_i, m_j) == True and (mouse_x < 1800 and mouse_x > 1000) and (mouse_y < 1000 and mouse_y > 200) and fl == True and mm == True:
                figures[selected_piece] = chr(65 + m_j) + str(8 - m_i)
                move_sound.play()
                print(selected_piece, figures[selected_piece], m_j, m_i)
                move += 1

                if move % 2 != 0: smm = 'White'
                else: smm = 'Black'
                game_log = text_st.render(smm + ' to move (Move ' + str(move) + ' )', True, 'Black')
            
    selected_piece = ''

def position_updates():
    for j in 'ABCDEFGH':
        for i in range(8, 0, -1):
            for ji in figures:
                if figures[ji] == j + str(i):
                    if ji[1] != 'p':
                        c_p = pg.transform.scale(vd[ji], (100, 200))
                        if ji != selected_piece:
                            screen.blit(c_p, ((int((ord(figures[ji][0]) - 65)) * 100 + 1000), ((8 - int(figures[ji][1])) * 100 + 100)))
                        else:
                            pos = pg.mouse.get_pos()
                            mouse_x = int(pos[0])
                            mouse_y = int(pos[1])
                            screen.blit(c_p, (mouse_x - 50, mouse_y - 50))
                    else:
                        c_p = pg.transform.scale(vd[ji], (100, 150))
                        if ji != selected_piece:
                            screen.blit(c_p, ((int((ord(figures[ji][0]) - 65)) * 100 + 1000), ((8 - int(figures[ji][1])) * 100 + 150)))
                        else:
                            pos = pg.mouse.get_pos()
                            mouse_x = int(pos[0])
                            mouse_y = int(pos[1])
                            screen.blit(c_p, (mouse_x - 50, mouse_y - 50))
    
    k_x = 0
    k_y = 600
    for ji in figures:
        if figures[ji] == '-':
            if ji[1] != 'p':
                c_p = pg.transform.scale(vd[ji], (100, 200))
                screen.blit(c_p, (k_x, k_y))
            else:
                c_p = pg.transform.scale(vd[ji], (100, 150))
                screen.blit(c_p, (k_x, k_y))
            
            k_x += 100

            if k_x >= 900:
                k_y += 100
                k_x = 0


def taking_pieces(m_i, m_j):
    for i in figures:
        coordinates = figures[i]
        if coordinates != '-' and i != selected_piece:
            pos_j = int((ord(coordinates[0]) - 65))
            pos_i = 8 - int(coordinates[1])

            if m_i == pos_i and m_j == pos_j:
                if same_color_crossing(i) == True:
                    figures[i] = '-'
                    return True
                else:
                    return False
    return True

# 'Rule' functions
                
def same_color_crossing(a):
    global game_log
    global selected_piece
    if a[0] != selected_piece[0]: return True
    else:
        game_log = text_st.render('There is a piece of yours in here', True, 'Black')
        return False
    
def walls_crossing(new_pos_i, new_pos_j, old_pos_i, old_pos_j):
    global game_log
    if new_pos_i == old_pos_i:
        l = abs(new_pos_j - old_pos_j) - 1
        m = min(new_pos_j, old_pos_j)
        for i in range(l):
            for j in figures:
                if figures[j] != '-':
                    coord_j = int((ord(figures[j][0]) - 65))
                    coord_i = 8 - int(figures[j][1])
                    if new_pos_i == coord_i and m + i + 1 == coord_j:
                        game_log = text_st.render('Your way is blocked by another piece', True, 'Black')
                        return False
        return True
    if new_pos_j == old_pos_j:
        l = abs(new_pos_i - old_pos_i) - 1
        m = min(new_pos_i, old_pos_i)
        for i in range(l):
            for j in figures:
                if figures[j] != '-':
                    coord_j = int((ord(figures[j][0]) - 65))
                    coord_i = 8 - int(figures[j][1])
                    if m + i + 1 == coord_i and new_pos_j == coord_j:
                        game_log = text_st.render('Your way is blocked by another piece', True, 'Black')
                        return False
        return True
    else:
        l = abs(new_pos_i - old_pos_i) - 1
        if new_pos_i > old_pos_i and new_pos_j > old_pos_j:
            for i in range(l):
                for j in figures:
                    if figures[j] != '-':
                        coord_j = int((ord(figures[j][0]) - 65))
                        coord_i = 8 - int(figures[j][1])
                        if coord_i == old_pos_i + i + 1 and coord_j == old_pos_j + i + 1:
                            game_log = text_st.render('Your way is blocked by another piece', True, 'Black')
                            return False
        if old_pos_i > new_pos_i and old_pos_j > new_pos_j:
            for i in range(l):
                for j in figures:
                    if figures[j] != '-':
                        coord_j = int((ord(figures[j][0]) - 65))
                        coord_i = 8 - int(figures[j][1])
                        if coord_i == new_pos_i + i + 1 and coord_j == new_pos_j + i + 1:
                            game_log = text_st.render('Your way is blocked by another piece', True, 'Black')
                            return False
        if new_pos_i > old_pos_i and old_pos_j > new_pos_j:
            for i in range(l):
                for j in figures:
                    if figures[j] != '-':
                        coord_j = int((ord(figures[j][0]) - 65))
                        coord_i = 8 - int(figures[j][1])
                        if coord_i == old_pos_i + i + 1 and coord_j == old_pos_j - i - 1:
                            game_log = text_st.render('Your way is blocked by another piece', True, 'Black')
                            return False
        if old_pos_i > new_pos_i and new_pos_j > old_pos_j:
            for i in range(l):
                for j in figures:
                    if figures[j] != '-':
                        coord_j = int((ord(figures[j][0]) - 65))
                        coord_i = 8 - int(figures[j][1])
                        if coord_i == new_pos_i + i + 1 and coord_j == new_pos_j - i - 1:
                            game_log = text_st.render('Your way is blocked by another piece', True, 'Black')
                            return False
        return True
'''
def pawn_transgress():
    if new_pos_i == 0: # black
        flt = False
        while flt != True:
            print('Input new piece code.')
            key_letter = input()
            if key_letter in 'brk' or key_letter == 'qn':
                figures[desk[old_pos_i][old_pos_j]] = '-'
                new_key = 'B' + key_letter[0] + str(in_num)
                figures[new_key] = str(position_input)
                flt = True
            else: print('You can only turn pawn into queen, rook, bishop, or knight.')
    if new_pos_i == 7: # white
        flt = False
        while flt != True:
            print('Input new piece code.')
            key_letter = input()
            if key_letter in 'brk' or key_letter == 'qn':
                figures[desk[old_pos_i][old_pos_j]] = '-'
                new_key = 'W' + key_letter[0] + str(in_num)
                figures[new_key] = str(position_input)
                flt = True
            else: print('You can only turn pawn into queen, rook, bishop, or knight.')
'''
    
def pawn_moves(new_pos_i, new_pos_j, old_pos_i, old_pos_j):
    global game_log

    sp = '--'
    for j in figures:
        if figures[j] != '-':
            coord_j = int((ord(figures[j][0]) - 65))
            coord_i = 8 - int(figures[j][1])
            if new_pos_i == coord_i and new_pos_j == coord_j: 
                sp = j
                
    if (new_pos_i - old_pos_i == 1 and new_pos_j == old_pos_j and selected_piece[0] == 'B') or (old_pos_i - new_pos_i == 1 and new_pos_j == old_pos_j and selected_piece[0] == 'W'):
        for j in figures:
            if figures[j] != '-':
                coord_j = int((ord(figures[j][0]) - 65))
                coord_i = 8 - int(figures[j][1])
                if coord_i == new_pos_i and coord_j == new_pos_j:
                    game_log = text_st.render('Pawn cannot move here or take a piece that is located here', True, 'Black')
                    return False
                else: 
                    #pawn_transgress()
                    return True
    elif (new_pos_i - old_pos_i == 2 and new_pos_j == old_pos_j and selected_piece[0] == 'B' and old_pos_i == 1) or (old_pos_i - new_pos_i == 2 and new_pos_j == old_pos_j and selected_piece[0] == 'W' and old_pos_i == 6):
        for j in figures:
            if figures[j] != '-':
                coord_j = int((ord(figures[j][0]) - 65))
                coord_i = 8 - int(figures[j][1])
                if (coord_i == new_pos_i and coord_j == new_pos_j) or ((coord_i == new_pos_i - 1) and coord_j == new_pos_j and selected_piece[0] == 'B') or ((coord_i == new_pos_i + 1) and coord_j == new_pos_j and selected_piece[0] == 'W'): 
                    game_log = text_st.render('Pawn cannot move here or take a piece that is located here', True, 'Black')
                    return False
                else: 
                    return True
    
    elif (new_pos_i - old_pos_i == 1 and abs(new_pos_j - old_pos_j) == 1 and selected_piece[0] == 'B' and sp[0] == 'W') or (old_pos_i - new_pos_i == 1 and abs(new_pos_j - old_pos_j) == 1 and selected_piece[0] == 'W' and sp[0] == 'B'):
        #pawn_transgress()
        return True
    #elif (new_pos_i - old_pos_i == 1 and abs(new_pos_j - old_pos_j) == 1 and figure_input[0] == 'W' and desk[new_pos_i - 1][new_pos_j][0:2] == 'Bp' and old_pos_i == 4 and special_pawn_marker > 0) or (old_pos_i - new_pos_i == 1 and abs(new_pos_j - old_pos_j) == 1 and figure_input[0] == 'B' and desk[new_pos_i + 1][new_pos_j][0:2] == 'Wp' and old_pos_i == 3 and special_pawn_marker > 0):
        #if figure_input[0] == 'W': figures[desk[new_pos_i - 1][new_pos_j]] = '-'
        #if figure_input[0] == 'B': figures[desk[new_pos_i + 1][new_pos_j]] = '-'
        #return True
    else:
        game_log = text_st.render('Pawn cannot move here.', True, 'Black')
        return False

def rook_moves(new_pos_i, new_pos_j, old_pos_i, old_pos_j):
    global game_log
    if new_pos_i == old_pos_i or new_pos_j == old_pos_j:
            return True
    else:
        game_log = text_st.render('Rook cannot move here', True, 'Black')
        return False

def knight_moves(new_pos_i, new_pos_j, old_pos_i, old_pos_j):
    global game_log
    if (abs(new_pos_i - old_pos_i) == 2 and abs(new_pos_j - old_pos_j) == 1) or (abs(new_pos_i - old_pos_i) == 1 and abs(new_pos_j - old_pos_j) == 2):
            return True
    else:
        game_log = text_st.render('Knight cannot move here.', True, 'Black')
        return False
    
def bishop_moves(new_pos_i, new_pos_j, old_pos_i, old_pos_j):
    global game_log
    if (old_pos_i + old_pos_j == new_pos_i + new_pos_j) or (old_pos_i - old_pos_j == new_pos_i - new_pos_j):
            return True
    else:
        game_log = text_st.render('Bishop cannot move here.', True, 'Black')
        return False
    
def queen_moves(new_pos_i, new_pos_j, old_pos_i, old_pos_j):
    global game_log
    if (new_pos_i == old_pos_i) or (new_pos_j == old_pos_j) or (old_pos_i + old_pos_j == new_pos_i + new_pos_j) or (old_pos_i - old_pos_j == new_pos_i - new_pos_j):
            return True
    else:
        game_log = text_st.render('Queen cannot move here.', True, 'Black')
        return False
    
def king_moves(new_pos_i, new_pos_j, old_pos_i, old_pos_j):
    global game_log
    if abs(new_pos_i - old_pos_i) == 1 or abs(new_pos_j - old_pos_j) == 1: #and check_search(move_name_pr, new_pos_i, new_pos_j) == 'neither':
            return True
    #elif castling() == True and king_distance() == True: return True
    else:
        game_log = text_st.render('King cannot move here.', True, 'Black')
        return False
    
def king_distance(new_pos_i, new_pos_j):
    global game_log
    if selected_piece[0] == 'W':
        an_king_i = int(figures['Bkg'][1]) - 1
        an_king_j = int(7 - (ord(str(figures['Bkg'])[0]) - 65))
        if abs(new_pos_i - an_king_i) <= 1 and abs(new_pos_j - an_king_j) <= 1:
            game_log = text_st.render('Kings cannot be that close to each other.', True, 'Black')
            return False
        else: return True
    if selected_piece[0] == 'B':
        an_king_i = int(figures['Wkg'][1]) - 1
        an_king_j = int(7 - (ord(str(figures['Wkg'])[0]) - 65))
        if abs(new_pos_i - an_king_i) <= 1 and abs(new_pos_j - an_king_j) <= 1:
            game_log = text_st.render('Kings cannot be that close to each other.', True, 'Black')
            return False
        else: return True

# display creation

width = 1920
height = 1080
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Chess')
clock = pg.time.Clock()

# game cycle

move = 1
run = True
game_controls_explanation = False
selected_piece = ''
while run:
    background()

    position_updates()

    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:

            if game_controls_explanation == False:
                game_log = text_st.render('To move a piece drag it. Press right mouse button to undo the selection', True, 'Black')
                game_controls_explanation = True
            
            if pg.mouse.get_pressed()[0] == True:
                selected_piece = mouse_click_event()
            if pg.mouse.get_pressed()[2] == True:
                selected_piece = ''
        if event.type == pg.MOUSEBUTTONUP:
            mouse_release_event()
        if event.type == pg.QUIT:
            run = False
    
    pg.display.update()
    clock.tick(120)  # FPS (frames per second)


pg.quit()
# pls don't quit!