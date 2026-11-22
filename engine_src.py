import json, os, time
from urllib import request as ureq

# ---------- Constants ----------
INF = 100000
MATE = 1000000
PIECE_VAL = [0, 100, 320, 330, 500, 900, 0]

# 0x88 board offsets
KNIGHT_OFF = (31, 33, 14, 18, -31, -33, -14, -18)
KING_OFF   = (15, 17, -15, -17, 1, -1, 16, -16)
BISHOP_DIR = (15, 17, -15, -17)
ROOK_DIR   = (1, -1, 16, -16)

# Castling: (king_dest, (path_squares), rook_from, rook_to, castling_right_bit)
CASTLE = {
    4:  ((6, (5, 6), 7, 5, 1), (2, (3, 2), 0, 3, 2)),
    116: ((118, (117, 118), 119, 117, 4), (114, (115, 114), 112, 115, 8)),
}

# Piece-square tables
PST_P = (
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
)

PST_K_MG = (
   -50,-40,-30,-30,-30,-30,-40,-50,
   -40,-20,  0,  0,  0,  0,-20,-40,
   -30,  0, 10, 15, 15, 10,  0,-30,
   -30,  5, 15, 20, 20, 15,  5,-30,
   -30,  0, 15, 20, 20, 15,  0,-30,
   -30,  5, 10, 15, 15, 10,  5,-30,
   -40,-20,  0,  5,  5,  0,-20,-40,
   -50,-40,-30,-30,-30,-30,-40,-50,
)

PST_K_EG = (
   -20,-10,-10,-10,-10,-10,-10,-20,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5, 10, 10,  5,  0,-10,
   -10,  5,  5, 10, 10,  5,  5,-10,
   -10,  0, 10, 10, 10, 10,  0,-10,
   -10, 10, 10, 10, 10, 10, 10,-10,
   -10,  5,  0,  0,  0,  0,  5,-10,
   -20,-10,-10,-10,-10,-10,-10,-20,
)

PST_Q = (
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0,
)

PST_N = (
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -20,-30,-30,-40,-40,-30,-30,-20,
   -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20,
)

PST = [None, PST_P, PST_K_MG, PST_N, PST_Q, PST_Q, PST_N]

FLIP = [(7 - (i >> 4)) * 8 + (i & 7) for i in range(128)]

# ---------- Zobrist ----------
SEED = 20261122
def nxt(s):
    return (s * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF

Z_PIECE = [[nxt(SEED := nxt(SEED)) for _ in range(128)] for _ in range(13)]
Z_SIDE  = nxt(SEED := nxt(SEED))
Z_CASTLE = [nxt(SEED := nxt(SEED)) for _ in range(16)]
Z_EP    = nxt(SEED := nxt(SEED))

# ---------- Board ----------
class Board:
    __slots__ = ('b', 'side', 'castle', 'ep', 'hm', 'hash', 'wk', 'bk', 'nodes')
    def __init__(self):
        self.b = [0]*128
        self.side = 1
        self.castle = 0
        self.ep = -1
        self.hm = 0
        self.hash = 0
        self.wk = 4
        self.bk = 116
        self.nodes = 0

    def parse_fen(self, fen):
        self.b = [0]*128
        self.side = 1
        self.castle = 0
        self.ep = -1
        self.hm = 0
        self.hash = 0
        parts = fen.split()
        board_part = parts[0]
        r = 7
        f = 0
        for ch in board_part:
            if ch == '/':
                r -= 1
                f = 0
            elif ch.isdigit():
                f += int(ch)
            else:
                sq = r*16 + f
                pc = 'PNBRQK'.index(ch.upper()) + 1
                val = pc if ch.isupper() else -pc
                self.b[sq] = val
                if pc == 6:
                    if val > 0: self.wk = sq
                    else: self.bk = sq
                f += 1
        self.side = 1 if parts[1] == 'w' else -1
        for i, ch in enumerate('KQkq'):
            if ch in parts[2]:
                self.castle |= 1 << i
        if len(parts) > 3 and parts[3] != '-':
            self.ep = (int(parts[3][1]) - 1) * 16 + (ord(parts[3][0]) - 97)
        if len(parts) > 4:
            self.hm = int(parts[4])
        h = 0
        for sq in range(128):
            if not (sq & 8) and self.b[sq]:
                h ^= Z_PIECE[self.b[sq] + 6][sq]
        if self.side == -1:
            h ^= Z_SIDE
        h ^= Z_CASTLE[self.castle]
        if self.ep >= 0:
            h ^= Z_EP
        self.hash = h

# ---------- Attack detection ----------
def attacked(board, sq, by_side):
    b = board.b
    if by_side == 1:
        for d in (-15, -17):
            to = sq + d
            if not (to & 136) and b[to] == 1:
                return True
        for d in KNIGHT_OFF:
            to = sq + d
            if not (to & 136) and b[to] == 2:
                return True
        for d in KING_OFF:
            to = sq + d
            if not (to & 136) and b[to] == 6:
                return True
    else:
        for d in (15, 17):
            to = sq + d
            if not (to & 136) and b[to] == -1:
                return True
        for d in KNIGHT_OFF:
            to = sq + d
            if not (to & 136) and b[to] == -2:
                return True
        for d in KING_OFF:
            to = sq + d
            if not (to & 136) and b[to] == -6:
                return True
    for d in BISHOP_DIR:
        to = sq + d
        while not (to & 136):
            pc = b[to]
            if pc:
                if by_side == 1 and (pc == 3 or pc == 5):
                    return True
                if by_side == -1 and (pc == -3 or pc == -5):
                    return True
                break
            to += d
    for d in ROOK_DIR:
        to = sq + d
        while not (to & 136):
            pc = b[to]
            if pc:
                if by_side == 1 and (pc == 4 or pc == 5):
                    return True
                if by_side == -1 and (pc == -4 or pc == -5):
                    return True
                break
            to += d
    return False

# ---------- Move generation ----------
def gen_moves(board, captures_only=False):
    b = board.b
    side = board.side
    moves = []
    king_sq = board.wk if side == 1 else board.bk
    
    for sq in range(128):
        if sq & 8: continue
        pc = b[sq]
        if pc * side <= 0: continue
        pt = abs(pc)
        
        if pt == 1:
            forward = 16 * side
            start_rank = 1 if side == 1 else 6
            promo_rank = 7 if side == 1 else 0
            to = sq + forward
            if not (to & 136) and b[to] == 0:
                if (to >> 4) == promo_rank:
                    for prom in (2, 3, 4, 5):
                        moves.append((sq, to, prom, 0))
                else:
                    moves.append((sq, to, 0, 0))
                    if (sq >> 4) == start_rank:
                        to2 = to + forward
                        if not (to2 & 136) and b[to2] == 0:
                            moves.append((sq, to2, 0, 2))
            if not captures_only:
                for d in (forward - 1, forward + 1):
                    to = sq + d
                    if to & 136: continue
                    if b[to] * side < 0 or to == board.ep:
                        if (to >> 4) == promo_rank:
                            for prom in (2, 3, 4, 5):
                                moves.append((sq, to, prom, 0))
                        else:
                            flag = 0 if to != board.ep else 3
                            moves.append((sq, to, 0, flag))
        
        elif pt == 2:
            for d in KNIGHT_OFF:
                to = sq + d
                if to & 136: continue
                if captures_only and b[to] * side >= 0: continue
                if b[to] * side <= 0:
                    moves.append((sq, to, 0, 0))
        
        elif pt == 3:
            for d in BISHOP_DIR:
                to = sq + d
                while not (to & 136):
                    if b[to] * side > 0: break
                    if captures_only and b[to] == 0:
                        to += d
                        continue
                    moves.append((sq, to, 0, 0))
                    if b[to]: break
                    to += d
        
        elif pt == 4:
            for d in ROOK_DIR:
                to = sq + d
                while not (to & 136):
                    if b[to] * side > 0: break
                    if captures_only and b[to] == 0:
                        to += d
                        continue
                    moves.append((sq, to, 0, 0))
                    if b[to]: break
                    to += d
        
        elif pt == 5:
            for d in BISHOP_DIR + ROOK_DIR:
                to = sq + d
                while not (to & 136):
                    if b[to] * side > 0: break
                    if captures_only and b[to] == 0:
                        to += d
                        continue
                    moves.append((sq, to, 0, 0))
                    if b[to]: break
                    to += d
        
        elif pt == 6:
            for d in KING_OFF:
                to = sq + d
                if to & 136: continue
                if captures_only and b[to] * side >= 0: continue
                if b[to] * side <= 0:
                    moves.append((sq, to, 0, 0))
            if not captures_only and sq in CASTLE:
                for kdest, path, rfrom, rto, right in CASTLE[sq]:
                    if not (board.castle & right): continue
                    if any(b[s] for s in path): continue
                    if attacked(board, sq, -side): continue
                    if any(attacked(board, s, -side) for s in path): continue
                    if attacked(board, kdest, -side): continue
                    moves.append((sq, kdest, 0, 1))
    
    return moves

# ---------- Make/Unmake ----------
def make_move(board, move):
    fr, to, prom, flag = move
    b = board.b
    pc = b[fr]
    cap = b[to]
    old_castle = board.castle
    old_ep = board.ep
    old_hm = board.hm
    old_hash = board.hash
    old_wk = board.wk
    old_bk = board.bk
    
    board.hash ^= Z_PIECE[pc + 6][fr]
    if cap:
        board.hash ^= Z_PIECE[cap + 6][to]
    
    ep_cap_sq = -1
    if flag == 3:
        ep_cap_sq = to - 16 * board.side
        cap = b[ep_cap_sq]
        b[ep_cap_sq] = 0
        board.hash ^= Z_PIECE[cap + 6][ep_cap_sq]
    
    b[fr] = 0
    if prom:
        pc = prom * board.side
    b[to] = pc
    board.hash ^= Z_PIECE[pc + 6][to]
    
    if abs(pc) == 6:
        if board.side == 1:
            board.wk = to
        else:
            board.bk = to
    
    if flag == 1:
        if board.side == 1:
            if to == 6:
                b[7] = 0; b[5] = 4
                board.hash ^= Z_PIECE[4 + 6][7] ^ Z_PIECE[4 + 6][5]
            else:
                b[0] = 0; b[3] = 4
                board.hash ^= Z_PIECE[4 + 6][0] ^ Z_PIECE[4 + 6][3]
        else:
            if to == 118:
                b[119] = 0; b[117] = -4
                board.hash ^= Z_PIECE[-4 + 6][119] ^ Z_PIECE[-4 + 6][117]
            else:
                b[112] = 0; b[115] = -4
                board.hash ^= Z_PIECE[-4 + 6][112] ^ Z_PIECE[-4 + 6][115]
    
    new_castle = board.castle
    if abs(pc) == 6:
        if board.side == 1: new_castle &= ~3
        else: new_castle &= ~12
    if fr == 0 or to == 0: new_castle &= ~2
    if fr == 7 or to == 7: new_castle &= ~1
    if fr == 112 or to == 112: new_castle &= ~8
    if fr == 119 or to == 119: new_castle &= ~4
    if new_castle != board.castle:
        board.hash ^= Z_CASTLE[board.castle] ^ Z_CASTLE[new_castle]
    board.castle = new_castle
    
    new_ep = -1
    if flag == 2:
        new_ep = (fr + to) // 2
    if new_ep != board.ep:
        if board.ep >= 0: board.hash ^= Z_EP
        if new_ep >= 0: board.hash ^= Z_EP
    board.ep = new_ep
    
    board.hm = 0 if abs(pc) == 1 or cap else board.hm + 1
    
    board.side = -board.side
    board.hash ^= Z_SIDE
    
    return (fr, to, prom, flag, cap, ep_cap_sq, old_castle, old_ep, old_hm, old_hash, old_wk, old_bk)

def unmake_move(board, move, undo):
    fr, to, prom, flag, cap, ep_cap_sq, old_castle, old_ep, old_hm, old_hash, old_wk, old_bk = undo
    b = board.b
    pc = b[to]
    
    b[to] = 0
    b[fr] = pc if not prom else (abs(pc) // pc) * 1
    
    if cap:
        b[to] = cap
    if ep_cap_sq >= 0:
        b[ep_cap_sq] = -board.side
    
    if flag == 1:
        if board.side == 1:
            if to == 6:
                b[5] = 0; b[7] = 4
            else:
                b[3] = 0; b[0] = 4
        else:
            if to == 118:
                b[117] = 0; b[119] = -4
            else:
                b[115] = 0; b[112] = -4
    
    board.wk = old_wk
    board.bk = old_bk
    
    board.castle = old_castle
    board.ep = old_ep
    board.hm = old_hm
    board.hash = old_hash
    board.side = -board.side

# ---------- Evaluation ----------
def evaluate(board):
    b = board.b
    score = 0
    w_material = 0
    b_material = 0
    w_pawns = [0]*8
    b_pawns = [0]*8
    
    for sq in range(128):
        if sq & 8: continue
        pc = b[sq]
        if not pc: continue
        pt = abs(pc)
        val = PIECE_VAL[pt]
        fsq = FLIP[sq]
        pst = PST[pt][fsq] if pt != 6 else 0
        
        if pc > 0:
            score += val + pst
            w_material += val
            if pt == 1:
                w_pawns[sq & 7] += 1
        else:
            score -= val + pst
            b_material += val
            if pt == 1:
                b_pawns[sq & 7] += 1
    
    total_material = w_material + b_material
    eg_weight = max(0, min(1, (12000 - total_material) / 8000))
    wk_fsq = FLIP[board.wk]
    bk_fsq = FLIP[board.bk]
    wk_score = int(PST_K_MG[wk_fsq] * (1 - eg_weight) + PST_K_EG[wk_fsq] * eg_weight)
    bk_score = int(PST_K_MG[bk_fsq] * (1 - eg_weight) + PST_K_EG[bk_fsq] * eg_weight)
    score += wk_score - bk_score
    
    for f in range(8):
        for r in range(8):
            sq = r*16 + f
            if sq & 8: continue
            if b[sq] == 1:
                passed = True
                for rf in (f-1, f, f+1):
                    if 0 <= rf < 8:
                        for rr in range(r+1, 8):
                            if b[rr*16 + rf] == -1:
                                passed = False
                                break
                    if not passed: break
                if passed:
                    score += 20 * (r - 1)
            elif b[sq] == -1:
                passed = True
                for rf in (f-1, f, f+1):
                    if 0 <= rf < 8:
                        for rr in range(r-1, -1, -1):
                            if b[rr*16 + rf] == 1:
                                passed = False
                                break
                    if not passed: break
                if passed:
                    score -= 20 * (6 - r)
    
    for f in range(8):
        if w_pawns[f] > 1:
            score -= 15 * (w_pawns[f] - 1)
        if b_pawns[f] > 1:
            score += 15 * (b_pawns[f] - 1)
    
    score += 5 * board.side
    
    return score * board.side

# ---------- Search ----------
TT = {}
KILLERS = [[0, 0] for _ in range(1024)]
HISTORY = {}
GAME_HASHES = set()
PLY = 0

def qsearch(board, alpha, beta, depth=0):
    global PLY
    PLY += 1
    board.nodes += 1
    
    if board.nodes & 1023 == 0 and time.time() > DEADLINE:
        raise TimeoutError
    
    stand_pat = evaluate(board)
    if stand_pat >= beta:
        PLY -= 1
        return beta
    if stand_pat > alpha:
        alpha = stand_pat
    
    if depth >= 12:
        PLY -= 1
        return alpha
    
    moves = gen_moves(board, captures_only=True)
    moves.sort(key=lambda m: (1000000 + 100*abs(board.b[m[1]]) - abs(board.b[m[0]])) if board.b[m[1]] else 0, reverse=True)
    
    for m in moves:
        undo = make_move(board, m)
        king_sq = board.wk if board.side == -1 else board.bk
        if not attacked(board, king_sq, board.side):
            score = -qsearch(board, -beta, -alpha, depth + 1)
            if score >= beta:
                unmake_move(board, m, undo)
                PLY -= 1
                return beta
            if score > alpha:
                alpha = score
        unmake_move(board, m, undo)
    
    PLY -= 1
    return alpha

def search(board, depth, alpha, beta, ply, can_extend=True):
    global PLY
    PLY += 1
    board.nodes += 1
    
    if board.nodes & 1023 == 0 and time.time() > DEADLINE:
        raise TimeoutError
    
    if board.hash in GAME_HASHES:
        PLY -= 1
        return 0
    
    tt_entry = TT.get(board.hash)
    if tt_entry and tt_entry[0] >= depth:
        tt_depth, tt_flag, tt_score, tt_move = tt_entry
        if tt_flag == 0:
            PLY -= 1
            return tt_score
        elif tt_flag == 1 and tt_score >= beta:
            PLY -= 1
            return tt_score
        elif tt_flag == 2 and tt_score <= alpha:
            PLY -= 1
            return tt_score
    
    king_sq = board.wk if board.side == -1 else board.bk
    in_check = attacked(board, king_sq, -board.side)
    if in_check and can_extend:
        depth += 1
    
    if depth <= 0:
        score = qsearch(board, alpha, beta)
        PLY -= 1
        return score
    
    moves = gen_moves(board)
    if not moves:
        PLY -= 1
        return -MATE + ply if in_check else 0
    
    tt_move = tt_entry[3] if tt_entry else None
    scored = []
    for m in moves:
        s = 0
        if m == tt_move:
            s = 1 << 30
        elif board.b[m[1]]:
            s = 1000000 + 100 * abs(board.b[m[1]]) - abs(board.b[m[0]])
        elif m == KILLERS[ply][0]:
            s = 50000
        elif m == KILLERS[ply][1]:
            s = 40000
        else:
            s = HISTORY.get(m, 0)
        scored.append((s, m))
    scored.sort(key=lambda x: -x[0])
    
    best_move = None
    best_score = -MATE
    legal_count = 0
    
    for _, m in scored:
        undo = make_move(board, m)
        king_sq2 = board.wk if board.side == -1 else board.bk
        if not attacked(board, king_sq2, board.side):
            legal_count += 1
            new_depth = depth - 1
            if board.hash in GAME_HASHES and evaluate(board) * board.side > 300:
                score = -10000
            else:
                score = -search(board, new_depth, -beta, -alpha, ply + 1, False)
            if score >= beta:
                if not board.b[m[1]]:
                    if KILLERS[ply][0] != m:
                        KILLERS[ply][1] = KILLERS[ply][0]
                        KILLERS[ply][0] = m
                HISTORY[m] = HISTORY.get(m, 0) + depth * depth
                unmake_move(board, m, undo)
                TT[board.hash] = (depth, 1, score, m)
                PLY -= 1
                return score
            if score > best_score:
                best_score = score
                best_move = m
            if score > alpha:
                alpha = score
        unmake_move(board, m, undo)
    
    if legal_count == 0:
        PLY -= 1
        return -MATE + ply if in_check else 0
    
    flag = 0 if alpha < best_score < beta else (2 if best_score <= alpha else 1)
    TT[board.hash] = (depth, flag, best_score, best_move)
    PLY -= 1
    return best_score

DEADLINE = 0

def iterative_deepening(board, time_limit=3.5):
    global TT, KILLERS, HISTORY, DEADLINE, PLY
    TT.clear()
    KILLERS = [[0, 0] for _ in range(1024)]
    HISTORY.clear()
    PLY = 0
    DEADLINE = time.time() + time_limit
    board.nodes = 0
    
    best_move = None
    for depth in range(1, 64):
        try:
            alpha = -MATE
            beta = MATE
            moves = gen_moves(board)
            if not moves:
                return None
            scored = []
            for m in moves:
                s = 0
                if board.b[m[1]]:
                    s = 1000000 + 100 * abs(board.b[m[1]]) - abs(board.b[m[0]])
                scored.append((s, m))
            scored.sort(key=lambda x: -x[0])
            
            root_best = None
            root_score = -MATE
            
            for _, m in scored:
                undo = make_move(board, m)
                king_sq = board.wk if board.side == -1 else board.bk
                if not attacked(board, king_sq, board.side):
                    score = -search(board, depth - 1, -beta, -alpha, 1)
                    if score > root_score:
                        root_score = score
                        root_best = m
                    if score > alpha:
                        alpha = score
                    if board.hash in GAME_HASHES:
                        score = 0
                unmake_move(board, m, undo)
                if time.time() > DEADLINE:
                    raise TimeoutError
            
            if root_best:
                best_move = root_best
            if root_score > 99000:
                break
        except TimeoutError:
            break
    return best_move

# ---------- UCI helpers ----------
SQ_NAME = [chr(97 + (i & 7)) + str((i >> 4) + 1) for i in range(128)]

def move_to_uci(m):
    fr, to, prom, flag = m
    s = SQ_NAME[fr] + SQ_NAME[to]
    if prom:
        s += 'nbrq'[prom - 2]
    return s

def uci_to_move(board, uci):
    fr = (ord(uci[0]) - 97) + (int(uci[1]) - 1) * 16
    to = (ord(uci[2]) - 97) + (int(uci[3]) - 1) * 16
    prom = 0
    if len(uci) == 5:
        prom = 'nbrq'.index(uci[4]) + 2
    return (fr, to, prom, 0)

# ---------- HTTP ----------
def http_post(url, body):
    data = json.dumps(body).encode()
    req = ureq.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    return json.loads(ureq.urlopen(req, timeout=8).read().decode())

# ---------- Main loop ----------
def main():
    url = os.environ['MAKEFUN_ENV_URL']
    game_id = None
    while True:
        resp = http_post(url + '/game', {})
        status = resp.get('status')
        outcome = resp.get('outcome')
        
        if outcome:
            resp = http_post(url + '/game', {})
            status = resp.get('status')
            if status == 'done' or resp.get('outcome'):
                break
            continue
        
        if status != 'your_move':
            break
        
        game_id = resp.get('game', game_id)
        fen = resp['fen']
        legal = resp.get('legal_moves', [])
        
        board = Board()
        board.parse_fen(fen)
        GAME_HASHES.add(board.hash)
        
        try:
            move = iterative_deepening(board, 3.5)
            if move:
                uci = move_to_uci(move)
            else:
                raise RuntimeError('no move')
        except Exception:
            uci = legal[0] if legal else 'e2e4'
        
        try:
            test_board = Board()
            test_board.parse_fen(fen)
            test_move = uci_to_move(test_board, uci)
            undo = make_move(test_board, test_move)
            king_sq = test_board.wk if test_board.side == 1 else test_board.bk
            if attacked(test_board, king_sq, test_board.side):
                raise ValueError('illegal')
            unmake_move(test_board, test_move, undo)
        except Exception:
            uci = legal[0] if legal else 'e2e4'
        
        http_post(url + '/move', {'game': game_id, 'move': uci})

if __name__ == '__main__':
    main()
