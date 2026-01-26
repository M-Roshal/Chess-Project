print()

#data input

desk = []

n = 8 # desk side length
k = 3 # number of spaces
move = 0 # current move
special_pawn_marker = 0 # pawn breakthrough flag

in_num = 3 # new piece index number

check_flag = 'neither'
checkmate_flag = False

c_tr_w = True # castling availibility tracker for white
c_tr_b = True # castling availibility tracker for black

#pieces input

figures = {
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

#commands

def upload_figures_positions():                   # puts the figures on the desk accordingly to the 'figures' dictionary
    for i in figures:
        coordinates = figures[i]
        if coordinates != '-':
            pos_j = int(7 - (ord(coordinates[0]) - 65))
            pos_i = int(coordinates[1]) - 1
            desk[pos_i][pos_j] = i

def show_desk():                        # shows the desk with current positions
    upload_figures_positions()
    print('Move N', move, end = '. ')
    if move % 2 != 0: print('White`s move')
    else: print('Black`s move')
    print()
    print(' ' * k, ' H    G    F    E    D    C    B    A')
    print(' ' * k, '——————————————————————————————————————')
    for i in range(n):
        print(i + 1, '| ', end = '')
        print(*desk[i], sep = '  ')
        if i != n - 1:
            print('  |')
        else: print()

def same_color_crossing():
    if desk[new_pos_i][new_pos_j][0] != figure_input[0]: return True
    else:
        print('There is a piece of yours in here.')
        return False

def walls_crossing():
    if new_pos_i == old_pos_i:
        l = abs(new_pos_j - old_pos_j) - 1
        m = min(new_pos_j, old_pos_j)
        for i in range(l):
            if desk[new_pos_i][m + i + 1] != ' 0 ':
                print('Your way is blocked by another piece.')
                return False
        return True
    if new_pos_j == old_pos_j:
        l = abs(new_pos_i - old_pos_i) - 1
        m = min(new_pos_i, old_pos_i)
        for i in range(l):
            if desk[m + i + 1][new_pos_j] != ' 0 ':
                print('Your way is blocked by another piece.')
                return False
        return True
    else:
        l = abs(new_pos_i - old_pos_i) - 1
        if new_pos_i > old_pos_i and new_pos_j > old_pos_j:
            for i in range(l):
                if desk[old_pos_i + i + 1][old_pos_j + i + 1] != ' 0 ':
                    print('Your way is blocked by another piece.')
                    return False
        if old_pos_i > new_pos_i and old_pos_j > new_pos_j:
            for i in range(l):
                if desk[new_pos_i + i + 1][new_pos_j + i + 1] != ' 0 ':
                    print('Your way is blocked by another piece.')
                    return False
        if new_pos_i > old_pos_i and old_pos_j > new_pos_j:
            for i in range(l):
                if desk[old_pos_i + i + 1][old_pos_j - i - 1] != ' 0 ':
                    print('Your way is blocked by another piece.')
                    return False
        if old_pos_i > new_pos_i and new_pos_j > old_pos_j:
            for i in range(l):
                if desk[new_pos_i + i + 1][new_pos_j - i - 1] != ' 0 ':
                    print('Your way is blocked by another piece.')
                    return False
        return True

def taking_pieces():
    if desk[new_pos_i][new_pos_j] != ' 0 ':
        figures[desk[new_pos_i][new_pos_j]] = '-'

def pawn_transgress():
    global in_num
    if new_pos_i == 0: # black
        flt = False
        while flt != True:
            print('Input new piece code.')
            key_letter = input()
            if key_letter in 'brk' or key_letter == 'qn':
                figures[desk[old_pos_i][old_pos_j]] = '-'
                new_key = 'B' + key_letter[0] + str(in_num)
                figures[new_key] = str(position_input)
                in_num += 1
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
                in_num += 1
                flt = True
            else: print('You can only turn pawn into queen, rook, bishop, or knight.')

def pawn_moves():
    if (new_pos_i - old_pos_i == 1 and new_pos_j == old_pos_j and figure_input[0] == 'W') or (old_pos_i - new_pos_i == 1 and new_pos_j == old_pos_j and figure_input[0] == 'B'):
        if same_color_crossing() == True:
            if desk[new_pos_i][new_pos_j] == ' 0 ':
                pawn_transgress()
                return True
            else: 
                print('Pawn cannot move here or take a piece that is located here')
                return False
        else: return False
    elif (new_pos_i - old_pos_i == 2 and new_pos_j == old_pos_j and figure_input[0] == 'W' and old_pos_i == 1) or (old_pos_i - new_pos_i == 2 and new_pos_j == old_pos_j and figure_input[0] == 'B' and old_pos_i == 6):
        if same_color_crossing() == True and ((desk[new_pos_i - 1][new_pos_j] == ' 0 ' and figure_input[0] == 'W') or (desk[new_pos_i + 1][new_pos_j] == ' 0 ' and figure_input[0] == 'B')):
            if desk[new_pos_i][new_pos_j] == ' 0 ': return True
            else: 
                print('Pawn cannot move here or take a piece that is located here')
                return False
        else: return False
    elif (new_pos_i - old_pos_i == 1 and abs(new_pos_j - old_pos_j) == 1 and figure_input[0] == 'W' and desk[new_pos_i][new_pos_j][0] == 'B') or (old_pos_i - new_pos_i == 1 and abs(new_pos_j - old_pos_j) == 1 and figure_input[0] == 'B' and desk[new_pos_i][new_pos_j][0] == 'W'):
        taking_pieces()
        pawn_transgress()
        return True
    elif (new_pos_i - old_pos_i == 1 and abs(new_pos_j - old_pos_j) == 1 and figure_input[0] == 'W' and desk[new_pos_i - 1][new_pos_j][0:2] == 'Bp' and old_pos_i == 4 and special_pawn_marker > 0) or (old_pos_i - new_pos_i == 1 and abs(new_pos_j - old_pos_j) == 1 and figure_input[0] == 'B' and desk[new_pos_i + 1][new_pos_j][0:2] == 'Wp' and old_pos_i == 3 and special_pawn_marker > 0):
        if figure_input[0] == 'W': figures[desk[new_pos_i - 1][new_pos_j]] = '-'
        if figure_input[0] == 'B': figures[desk[new_pos_i + 1][new_pos_j]] = '-'
        return True
    else:
        print('Pawn cannot move here.')
        return False
        

def rook_moves():
    if new_pos_i == old_pos_i or new_pos_j == old_pos_j:
        if same_color_crossing() == True and walls_crossing() == True:
            taking_pieces()
            return True
        else: return False
    else:
        print('Rook cannot move here.')
        return False

def knight_moves():
    if (abs(new_pos_i - old_pos_i) == 2 and abs(new_pos_j - old_pos_j) == 1) or (abs(new_pos_i - old_pos_i) == 1 and abs(new_pos_j - old_pos_j) == 2):
        if same_color_crossing() == True:
            taking_pieces()
            return True
        else: return False
    else:
        print('Knight cannot move here.')
        return False

def bishop_moves():
    if (old_pos_i + old_pos_j == new_pos_i + new_pos_j) or (old_pos_i - old_pos_j == new_pos_i - new_pos_j):
        if same_color_crossing() == True and walls_crossing() == True:
            taking_pieces()
            return True
        else: return False
    else:
        print('Bishop cannot move here.')
        return False

def queen_moves():
    if (new_pos_i == old_pos_i) or (new_pos_j == old_pos_j) or (old_pos_i + old_pos_j == new_pos_i + new_pos_j) or (old_pos_i - old_pos_j == new_pos_i - new_pos_j):
        if same_color_crossing() == True and walls_crossing() == True:
            taking_pieces()
            return True
        else: return False
    else:
        print('Queen cannot move here.')
        return False

def king_moves():
    if max(abs(new_pos_i - old_pos_i), abs(new_pos_j - old_pos_j)) == 1:
        if same_color_crossing() == True and king_distance() == True and check_search(move_name_pr, new_pos_i, new_pos_j) == 'neither':
            taking_pieces()
            return True
        else: return False
    elif castling() == True and king_distance() == True: return True
    else:
        print('King cannot move here.')
        return False

def king_distance():
    if figure_input[0] == 'W':
        an_king_i = int(figures['Bkg'][1]) - 1
        an_king_j = int(7 - (ord(str(figures['Bkg'])[0]) - 65))
        if abs(new_pos_i - an_king_i) <= 1 and abs(new_pos_j - an_king_j) <= 1:
            print('Kings cannot be that close to each other.')
            return False
        else: return True
    if figure_input[0] == 'B':
        an_king_i = int(figures['Wkg'][1]) - 1
        an_king_j = int(7 - (ord(str(figures['Wkg'])[0]) - 65))
        if abs(new_pos_i - an_king_i) <= 1 and abs(new_pos_j - an_king_j) <= 1:
            print('Kings cannot be that close to each other.')
            return False
        else: return True

def check_search(mn, king_pos_i, king_pos_j, ch_pos_i, ch_pos_j): 
    for attacker in figures:
        if mn == 'White' and attacker[0] == 'W':
            if ('p' in attacker) and (king_pos_i - ch_pos_i == 1 and abs(king_pos_j - ch_pos_j) == 1): return('Black')
            if (('r' in attacker) or ('q' in attacker)) and (ch_pos_i == king_pos_i or ch_pos_j == king_pos_j):
                if ch_pos_i == king_pos_i:
                    fl2 = False
                    l = abs(ch_pos_j - king_pos_j) - 1
                    m = min(ch_pos_j, king_pos_j)
                    for i in range(l):
                        if desk[ch_pos_i][m + i + 1] != ' 0 ': fl2 = True
                    if fl2 == False: return('Black')
                if ch_pos_j == king_pos_j:
                    fl2 = False
                    l = abs(ch_pos_i - king_pos_i) - 1
                    m = min(ch_pos_i, king_pos_i)
                    for i in range(l):
                        if desk[m + i + 1][ch_pos_j] != ' 0 ': fl2 = True
                    if fl2 == False: return('Black')
            if (('k' in attacker) and ('g' not in attacker)) and ((abs(king_pos_i - ch_pos_i) == 2 and abs(king_pos_j - ch_pos_j) == 1) or (abs(king_pos_i - ch_pos_i) == 1 and abs(king_pos_j - ch_pos_j) == 2)): return('Black')
            if ('b' in attacker) and ((king_pos_i + ch_pos_j == ch_pos_i + king_pos_j) or (ch_pos_i - ch_pos_j == king_pos_i - king_pos_j)):
                l = abs(ch_pos_i - king_pos_i) - 1
                fl2 = False
                if king_pos_i > ch_pos_i and king_pos_j > ch_pos_j:
                    for i in range(l):
                        if desk[ch_pos_i + i + 1][ch_pos_j + i + 1] != ' 0 ': fl2 = True
                if ch_pos_i > king_pos_i and ch_pos_j > king_pos_j:
                    for i in range(l):
                        if desk[king_pos_i + i + 1][king_pos_j + i + 1] != ' 0 ': fl2 = True
                if king_pos_i > ch_pos_i and ch_pos_j > king_pos_j:
                    for i in range(l):
                        if desk[ch_pos_i + i + 1][ch_pos_j - i - 1] != ' 0 ': fl2 = True
                if ch_pos_i > king_pos_i and king_pos_j > ch_pos_j:
                    for i in range(l):
                        if desk[king_pos_i + i + 1][king_pos_j - i - 1] != ' 0 ': fl2 = True
                if fl2 == False: return('Black')

    if mn == 'Black' and attacker[0] == 'B':
        if ('p' in attacker) and (ch_pos_i - king_pos_i == 1 and abs(king_pos_j - ch_pos_j) == 1): return('White')
        if (('r' in attacker) or ('q' in attacker)) and (ch_pos_i == king_pos_i or ch_pos_j == king_pos_j):
            if ch_pos_i == king_pos_i:
                fl2 = False
                l = abs(ch_pos_j - king_pos_j) - 1
                m = min(ch_pos_j, king_pos_j)
                for i in range(l):
                    if desk[ch_pos_i][m + i + 1] != ' 0 ': fl2 = True
                if fl2 == False: return('White')
            if ch_pos_j == king_pos_j:
                fl2 = False
                l = abs(ch_pos_i - king_pos_i) - 1
                m = min(ch_pos_i, king_pos_i)
                for i in range(l):
                    if desk[m + i + 1][ch_pos_j] != ' 0 ': fl2 = True
                if fl2 == False: return('White')
        if (('k' in attacker) and ('g' not in attacker)) and ((abs(king_pos_i - ch_pos_i) == 2 and abs(king_pos_j - ch_pos_j) == 1) or (abs(king_pos_i - ch_pos_i) == 1 and abs(king_pos_j - ch_pos_j) == 2)): return('White')
        if ('b' in attacker) and ((king_pos_i + ch_pos_j == ch_pos_i + king_pos_j) or (ch_pos_i - ch_pos_j == king_pos_i - king_pos_j)):
            l = abs(ch_pos_i - king_pos_i) - 1
            fl2 = False
            if king_pos_i > ch_pos_i and king_pos_j > ch_pos_j:
                for i in range(l):
                    if desk[ch_pos_i + i + 1][ch_pos_j + i + 1] != ' 0 ': fl2 = True
            if ch_pos_i > king_pos_i and ch_pos_j > king_pos_j:
                for i in range(l):
                    if desk[king_pos_i + i + 1][king_pos_j + i + 1] != ' 0 ': fl2 = True
            if king_pos_i > ch_pos_i and ch_pos_j > king_pos_j:
                for i in range(l):
                    if desk[ch_pos_i + i + 1][ch_pos_j - i - 1] != ' 0 ': fl2 = True
            if ch_pos_i > king_pos_i and king_pos_j > ch_pos_j:
                for i in range(l):
                    if desk[king_pos_i + i + 1][king_pos_j - i - 1] != ' 0 ': fl2 = True
            if fl2 == False: return('White')
    
    return('neither')

def castling():
    if figure_input[0] == 'W' and figures['Wkg'] == 'E1':
        if position_input == 'G1':
            if check_search(move_name_pr, kpi, kpj) == 'neither' and check_search(move_name_pr, kpi, kpj + 1) == 'neither' and check_search(move_name_pr, kpi, kpj + 2) == 'neither':
                if desk[0][5] == ' 0 ' and desk[0][6] == ' 0 ' and figures['Wkg'] == 'E1' and figures['Wr2'] == 'H1' and c_tr_w == True:
                    figures['Wkg'] = 'G1'
                    figures['Wr2'] = 'F1'
                    return True
        elif position_input == 'C1':
            if check_search(move_name_pr, kpi, kpj) == 'neither' and check_search(move_name_pr, kpi, kpj - 1) == 'neither' and check_search(move_name_pr, kpi, kpj - 2) == 'neither':
                if desk[0][3] == ' 0 ' and desk[0][2] == ' 0 ' and desk[0][1] == ' 0 ' and figures['Wkg'] == 'E1' and figures['Wr1'] == 'A1' and c_tr_w == True:
                    figures['Wkg'] = 'C1'
                    figures['Wr1'] = 'D1'
                    return True
    if figure_input[0] == 'B' and figures['Bkg'] == 'E8':
        if position_input == 'G8':
            if check_search(move_name_pr, kpi, kpj) == 'neither' and check_search(move_name_pr, kpi, kpj + 1) == 'neither' and check_search(move_name_pr, kpi, kpj + 2) == 'neither':
                if desk[7][5] == ' 0 ' and desk[7][6] == ' 0 ' and figures['Bkg'] == 'E8' and figures['Br2'] == 'H8' and c_tr_b == True:
                    figures['Bkg'] = 'G8'
                    figures['Br2'] = 'F8'
                    return True
        elif position_input == 'C8':
            if check_search(move_name_pr, kpi, kpj) == 'neither' and check_search(move_name_pr, kpi, kpj - 1) == 'neither' and check_search(move_name_pr, kpi, kpj - 2) == 'neither':
                if desk[7][3] == ' 0 ' and desk[7][2] == ' 0 ' and desk[7][1] == ' 0 ' and figures['Bkg'] == 'E8' and figures['Br1'] == 'A8' and c_tr_b == True:
                    figures['Bkg'] = 'C8'
                    figures['Br1'] = 'D8'
                    return True
    return False

# Helper: determine if side `color` (“White” or “Black”) is in check.
def is_in_check(color):
    """
    Returns True if the king of side `color` is under attack by any opponent piece,
    using the same move-validation functions (pawn_moves, rook_moves, etc.).
    """
    # Determine king key and its position
    king_key = 'Wkg' if color == 'White' else 'Bkg'
    king_pos = figures.get(king_key, None)
    # If king is not on board (e.g. already captured or not placed), th3n not-in-check here.
    if not king_pos or king_pos == '-':
        return False

    # Compute king indices
    king_row = int(king_pos[1]) - 1
    king_col = int(7 - (ord(king_pos[0]) - 65))

    # Opponent's color letter
    opponent_prefix = 'B' if color == 'White' else 'W'

    # Save any globals we will override
    saved_figure_input = globals().get('figure_input', None)
    saved_position_input = globals().get('position_input', None)
    saved_old_pos_i = globals().get('old_pos_i', None)
    saved_old_pos_j = globals().get('old_pos_j', None)
    saved_new_pos_i = globals().get('new_pos_i', None)
    saved_new_pos_j = globals().get('new_pos_j', None)

    # For each opponent piece that is still on board
    for p in list(figures.keys()):
        if not p.startswith(opponent_prefix):
            continue
        p_pos = figures[p]
        if p_pos == '-':
            continue
        # Set globals so that we “attempt” moving this piece to the king’s square
        globals()['figure_input'] = p
        globals()['position_input'] = king_pos

        # Compute old indices for p
        old_i = int(p_pos[1]) - 1
        old_j = int(7 - (ord(p_pos[0]) - 65))
        globals()['old_pos_i'] = old_i
        globals()['old_pos_j'] = old_j
        globals()['new_pos_i'] = king_row
        globals()['new_pos_j'] = king_col

        # Now call the appropriate move-validation function:
        valid_attack = False
        # Pawn:
        if 'p' in p and not ('kg' in p):  # pawn keys contain 'p'
            # pawn_moves() should allow diagonal capture into king square if legal
            try:
                valid_attack = pawn_moves()
            except Exception:
                valid_attack = False
        # Rook:
        elif 'r' in p and 'q' not in p:
            try:
                valid_attack = rook_moves()
            except Exception:
                valid_attack = False
        # Knight:
        elif 'k' in p and 'g' not in p:  # assuming knight keys contain 'k' but not 'kg'
            try:
                valid_attack = knight_moves()
            except Exception:
                valid_attack = False
        # Bishop:
        elif 'b' in p and not ('qn' in p):  # bishop keys contain 'b' but not queen
            try:
                valid_attack = bishop_moves()
            except Exception:
                valid_attack = False
        # Queen:
        elif 'q' in p and 'qn' in p:  # queen keys contain 'qn'
            try:
                valid_attack = queen_moves()
            except Exception:
                valid_attack = False
        # King (attacking adjacent square):
        elif 'kg' in p:
            try:
                valid_attack = king_moves()
            except Exception:
                valid_attack = False
        else:
            # Unknown piece key pattern; skip
            valid_attack = False

        # If move-validation says it can move to king square, it's an attack
        if valid_attack:
            # Restore globals before returning
            if saved_figure_input is not None:
                globals()['figure_input'] = saved_figure_input
            else:
                globals().pop('figure_input', None)
            if saved_position_input is not None:
                globals()['position_input'] = saved_position_input
            else:
                globals().pop('position_input', None)
            if saved_old_pos_i is not None:
                globals()['old_pos_i'] = saved_old_pos_i
            else:
                globals().pop('old_pos_i', None)
            if saved_old_pos_j is not None:
                globals()['old_pos_j'] = saved_old_pos_j
            else:
                globals().pop('old_pos_j', None)
            if saved_new_pos_i is not None:
                globals()['new_pos_i'] = saved_new_pos_i
            else:
                globals().pop('new_pos_i', None)
            if saved_new_pos_j is not None:
                globals()['new_pos_j'] = saved_new_pos_j
            else:
                globals().pop('new_pos_j', None)

            return True

    # Restore globals
    if saved_figure_input is not None:
        globals()['figure_input'] = saved_figure_input
    else:
        globals().pop('figure_input', None)
    if saved_position_input is not None:
        globals()['position_input'] = saved_position_input
    else:
        globals().pop('position_input', None)
    if saved_old_pos_i is not None:
        globals()['old_pos_i'] = saved_old_pos_i
    else:
        globals().pop('old_pos_i', None)
    if saved_old_pos_j is not None:
        globals()['old_pos_j'] = saved_old_pos_j
    else:
        globals().pop('old_pos_j', None)
    if saved_new_pos_i is not None:
        globals()['new_pos_i'] = saved_new_pos_i
    else:
        globals().pop('new_pos_i', None)
    if saved_new_pos_j is not None:
        globals()['new_pos_j'] = saved_new_pos_j
    else:
        globals().pop('new_pos_j', None)

    return False

# Check for checkmate: if side `color` is in check AND has no legal move to escape.
# global checkmate_flag = True if it is checkmate.
def checkmate():
    global checkmate_flag

    color_to_test = 'White' if (move % 2 == 1) else 'Black'

    # kind check
    if not is_in_check(color_to_test):
        return False  # not in check --> cannot be checkmate

    # all legal moves for color_to_test; if any move leads to a position where king not in check, it is not checkmate
    prefix = 'W' if color_to_test == 'White' else 'B'

    # Save globals that we will override
    saved_figure_input = globals().get('figure_input', None)
    saved_position_input = globals().get('position_input', None)
    saved_old_pos_i = globals().get('old_pos_i', None)
    saved_old_pos_j = globals().get('old_pos_j', None)
    saved_new_pos_i = globals().get('new_pos_i', None)
    saved_new_pos_j = globals().get('new_pos_j', None)

    # For each piece of this color
    for p in list(figures.keys()):
        if not p.startswith(prefix):
            continue
        p_pos = figures[p]
        if p_pos == '-':
            continue  # captured already

        orig_pos = p_pos  # e.g. 'E2'
        # Compute old indices once
        old_i = int(orig_pos[1]) - 1
        old_j = int(7 - (ord(orig_pos[0]) - 65))

        # Try every destination square
        for file in 'ABCDEFGH':
            for rank in '12345678':
                dest = file + rank
                if dest == orig_pos:
                    continue
                # If destination holds own piece, skip
                dest_piece_key = None
                for q in figures:
                    if figures[q] == dest:
                        dest_piece_key = q
                        break
                if dest_piece_key and dest_piece_key.startswith(prefix):
                    continue

                # Set globals to attempt this move
                globals()['figure_input'] = p
                globals()['position_input'] = dest
                globals()['old_pos_i'] = old_i
                globals()['old_pos_j'] = old_j
                new_i = int(rank) - 1
                new_j = int(7 - (ord(file) - 65))
                globals()['new_pos_i'] = new_i
                globals()['new_pos_j'] = new_j

                # Call the corresponding move-validation
                valid_move = False
                if 'p' in p and not ('kg' in p):
                    try:
                        valid_move = pawn_moves()
                    except Exception:
                        valid_move = False
                elif 'r' in p and 'q' not in p:
                    try:
                        valid_move = rook_moves()
                    except Exception:
                        valid_move = False
                elif 'k' in p and 'g' not in p:
                    try:
                        valid_move = knight_moves()
                    except Exception:
                        valid_move = False
                elif 'b' in p and not ('qn' in p):
                    try:
                        valid_move = bishop_moves()
                    except Exception:
                        valid_move = False
                elif 'q' in p and 'qn' in p:
                    try:
                        valid_move = queen_moves()
                    except Exception:
                        valid_move = False
                elif 'kg' in p:
                    try:
                        valid_move = king_moves()
                    except Exception:
                        valid_move = False
                else:
                    valid_move = False

                if not valid_move:
                    continue

                # Simulate the move on figures:
                # 1) remove captured piece if exists
                captured_key = None
                if dest_piece_key:
                    captured_key = dest_piece_key
                    figures[captured_key] = '-'  # remove it

                # 2) move p
                figures[p] = dest

                # Now check if king is still in check after this move
                still_in_check = is_in_check(color_to_test)

                # Revert simulation
                figures[p] = orig_pos
                if captured_key:
                    figures[captured_key] = dest

                if not still_in_check:
                    # Found at least one legal move that escapes check, then not checkmate
                    # Restore globals and return False
                    if saved_figure_input is not None:
                        globals()['figure_input'] = saved_figure_input
                    else:
                        globals().pop('figure_input', None)
                    if saved_position_input is not None:
                        globals()['position_input'] = saved_position_input
                    else:
                        globals().pop('position_input', None)
                    if saved_old_pos_i is not None:
                        globals()['old_pos_i'] = saved_old_pos_i
                    else:
                        globals().pop('old_pos_i', None)
                    if saved_old_pos_j is not None:
                        globals()['old_pos_j'] = saved_old_pos_j
                    else:
                        globals().pop('old_pos_j', None)
                    if saved_new_pos_i is not None:
                        globals()['new_pos_i'] = saved_new_pos_i
                    else:
                        globals().pop('new_pos_i', None)
                    if saved_new_pos_j is not None:
                        globals()['new_pos_j'] = saved_new_pos_j
                    else:
                        globals().pop('new_pos_j', None)

                    return False

    # If  here, side is in check and no legal escape, so checkmate
    # Announce and set flag
    loser = color_to_test
    winner = 'Black' if loser == 'White' else 'White'
    print(f'Checkmate. {winner} wins.')
    checkmate_flag = True

    # Restore globals
    if saved_figure_input is not None:
        globals()['figure_input'] = saved_figure_input
    else:
        globals().pop('figure_input', None)
    if saved_position_input is not None:
        globals()['position_input'] = saved_position_input
    else:
        globals().pop('position_input', None)
    if saved_old_pos_i is not None:
        globals()['old_pos_i'] = saved_old_pos_i
    else:
        globals().pop('old_pos_i', None)
    if saved_old_pos_j is not None:
        globals()['old_pos_j'] = saved_old_pos_j
    else:
        globals().pop('old_pos_j', None)
    if saved_new_pos_i is not None:
        globals()['new_pos_i'] = saved_new_pos_i
    else:
        globals().pop('new_pos_i', None)
    if saved_new_pos_j is not None:
        globals()['new_pos_j'] = saved_new_pos_j
    else:
        globals().pop('new_pos_j', None)

    return True


# Check for stalemate: side `color_to_test` not in check, but has no legal moves
def stalemate():
    global checkmate_flag
    # Determine side to test (the side to move). Use same logic as in checkmate():
    color_to_test = 'White' if (move % 2 == 1) else 'Black'
    # If in check, not stalemate
    if is_in_check(color_to_test):
        return False

    prefix = 'W' if color_to_test == 'White' else 'B'

    # Save globals
    saved_figure_input = globals().get('figure_input', None)
    saved_position_input = globals().get('position_input', None)
    saved_old_pos_i = globals().get('old_pos_i', None)
    saved_old_pos_j = globals().get('old_pos_j', None)
    saved_new_pos_i = globals().get('new_pos_i', None)
    saved_new_pos_j = globals().get('new_pos_j', None)

    # Try all possible moves
    for p in list(figures.keys()):
        if not p.startswith(prefix):
            continue
        p_pos = figures[p]
        if p_pos == '-':
            continue
        orig_pos = p_pos
        old_i = int(orig_pos[1]) - 1
        old_j = int(7 - (ord(orig_pos[0]) - 65))

        for file in 'ABCDEFGH':
            for rank in '12345678':
                dest = file + rank
                if dest == orig_pos:
                    continue
                # Skip if own piece at dest
                dest_piece_key = None
                for q in figures:
                    if figures[q] == dest:
                        dest_piece_key = q
                        break
                if dest_piece_key and dest_piece_key.startswith(prefix):
                    continue

                # Set globals to attempt move
                globals()['figure_input'] = p
                globals()['position_input'] = dest
                globals()['old_pos_i'] = old_i
                globals()['old_pos_j'] = old_j
                new_i = int(rank) - 1
                new_j = int(7 - (ord(file) - 65))
                globals()['new_pos_i'] = new_i
                globals()['new_pos_j'] = new_j

                # Validate move
                valid_move = False
                if 'p' in p and not ('kg' in p):
                    try:
                        valid_move = pawn_moves()
                    except Exception:
                        valid_move = False
                elif 'r' in p and 'q' not in p:
                    try:
                        valid_move = rook_moves()
                    except Exception:
                        valid_move = False
                elif 'k' in p and 'g' not in p:
                    try:
                        valid_move = knight_moves()
                    except Exception:
                        valid_move = False
                elif 'b' in p and not ('qn' in p):
                    try:
                        valid_move = bishop_moves()
                    except Exception:
                        valid_move = False
                elif 'q' in p and 'qn' in p:
                    try:
                        valid_move = queen_moves()
                    except Exception:
                        valid_move = False
                elif 'kg' in p:
                    try:
                        valid_move = king_moves()
                    except Exception:
                        valid_move = False
                else:
                    valid_move = False

                if not valid_move:
                    continue

                # Simulate move
                captured_key = None
                if dest_piece_key:
                    captured_key = dest_piece_key
                    figures[captured_key] = '-'
                figures[p] = dest

                # If after move king still not in check, then there is a legal move → not stalemate
                if not is_in_check(color_to_test):
                    # revert
                    figures[p] = orig_pos
                    if captured_key:
                        figures[captured_key] = dest
                    # restore globals
                    if saved_figure_input is not None:
                        globals()['figure_input'] = saved_figure_input
                    else:
                        globals().pop('figure_input', None)
                    if saved_position_input is not None:
                        globals()['position_input'] = saved_position_input
                    else:
                        globals().pop('position_input', None)
                    if saved_old_pos_i is not None:
                        globals()['old_pos_i'] = saved_old_pos_i
                    else:
                        globals().pop('old_pos_i', None)
                    if saved_old_pos_j is not None:
                        globals()['old_pos_j'] = saved_old_pos_j
                    else:
                        globals().pop('old_pos_j', None)
                    if saved_new_pos_i is not None:
                        globals()['new_pos_i'] = saved_new_pos_i
                    else:
                        globals().pop('new_pos_i', None)
                    if saved_new_pos_j is not None:
                        globals()['new_pos_j'] = saved_new_pos_j
                    else:
                        globals().pop('new_pos_j', None)
                    return False

                # revert simulation
                figures[p] = orig_pos
                if captured_key:
                    figures[captured_key] = dest
                # continue trying other moves

    # No legal moves found and not in check => stalemate
    print('Stalemate.')
    checkmate_flag = True  # to break main loop if you rely on checkmate_flag to exit
    # restore globals
    if saved_figure_input is not None:
        globals()['figure_input'] = saved_figure_input
    else:
        globals().pop('figure_input', None)
    if saved_position_input is not None:
        globals()['position_input'] = saved_position_input
    else:
        globals().pop('position_input', None)
    if saved_old_pos_i is not None:
        globals()['old_pos_i'] = saved_old_pos_i
    else:
        globals().pop('old_pos_i', None)
    if saved_old_pos_j is not None:
        globals()['old_pos_j'] = saved_old_pos_j
    else:
        globals().pop('old_pos_j', None)
    if saved_new_pos_i is not None:
        globals()['new_pos_i'] = saved_new_pos_i
    else:
        globals().pop('new_pos_i', None)
    if saved_new_pos_j is not None:
        globals()['new_pos_j'] = saved_new_pos_j
    else:
        globals().pop('new_pos_j', None)
    return True

#program

print('Pieces are put on starting positions. The game starts:')
print("hint: Enter like ‘Wp1 E4’, or 'surrender' to surrender.")
print()

while not checkmate_flag:
    # the game
    special_pawn_marker -= 1

    for i in range(n):  # desk recreation
        desk.append([])
        for j in range(n):
            desk[i].append(' 0 ')

    move += 1

    if move % 2 != 0: 
        move_name = 'White'
        move_name_pr = 'Black'
    if move % 2 == 0: 
        move_name = 'Black'
        move_name_pr = 'White'

    spr = False # correct input flag
    show_desk()

    while spr != True:
        command = input()       # commands input

        if command == 'surrender': # checking for surrendering
            if move % 2 != 0: print('White surrendered. Black won.'), print()
            else: print('Black surrendered. White won.'), print()
            exit()
        
        parts = command.strip().split()
        if len(parts) != 2:
            print('Invalid format. Try again.')
            continue
        figure_input, position_input = parts
        position_input = position_input.upper()

        if (figure_input in figures) and (position_input[0] in 'ABCDEFGH') and (position_input[1] in '12345678'): # checking for correct input
            if (figure_input[0] == 'W' and move % 2 != 0) or (figure_input[0] == 'B' and move % 2 == 0):

                new_pos_j = int(7 - (ord(position_input[0]) - 65))
                new_pos_i = int(position_input[1]) - 1
                old_pos_i = int(str(figures[figure_input])[1]) - 1
                old_pos_j = int(7 - (ord(str(figures[figure_input])[0]) - 65))

                if 'p' in figure_input: 
                    spr = pawn_moves()
                    if abs(new_pos_i - old_pos_i) == 2: 
                        special_pawn_marker = 2
                if 'r' in figure_input: spr = rook_moves()
                if ('k' in figure_input) and ('g' not in figure_input): spr = knight_moves()
                if 'b' in figure_input: spr = bishop_moves()
                if 'q' in figure_input: spr = queen_moves()
                if 'kg' in figure_input: 
                    spr = king_moves()
                    if spr == True:
                        if move % 2 != 0: c_tr_w = False
                        if move % 2 == 0: c_tr_b = False

                kpj = int(7 - (ord(figures[str(move_name_pr[0] +'kg')][0]) - 65))
                kpi = int(figures[str(move_name_pr[0] +'kg')][1]) - 1

            else:
                if move % 2 != 0: print('White should move now.')
                if move % 2 == 0: print('Black should move now.')
            
            if check_flag != 'neither':
                if check_search(move_name_pr, kpi, kpj) != 'neither':
                    spr = False
                    print('You are under check, so you should escape it now.')
                else: check_flag = 'neither'
        
        else: print('You are supposed to enter piece name and new position coordinates, or type "surrender".')
    
    for i in figures:
        ch_pos_i = int(figures[i][1]) - 1
        ch_pos_j = int(7 - (ord(figures[i][0]) - 65))
        if move_name[0] == i[0]:
            if 'kg' in i:
                for j in figures:
                    if  move_name[0] != i[0] and j != 'kg':
                        ch_pos_i = int(figures[j][1]) - 1
                        ch_pos_j = int(7 - (ord(figures[j][0]) - 65))
                        check_flag = check_search(move_name, ch_pos_i, ch_pos_j, kpi, kpj)
            else: check_flag = check_search(move_name, kpi, kpj, ch_pos_i, ch_pos_j)
    
    if check_flag == 'White': print('White are under check!')
    if check_flag == 'Black': print('Black are under check!')

    if figure_input[1] == 'p' and (position_input[1] == '8' or position_input[1] == '1'):
        in_num += 1
    else: figures[figure_input] = position_input


    if checkmate():
        break  # or rely on checkmate_flag to exit loop
    if stalemate():
        break


    desk = []
    kpi = 0
    kpj = 0

print('Version: alpha 1.0. Critical cases and bugs are not eliminated yet. Core chess gameplay exists.')