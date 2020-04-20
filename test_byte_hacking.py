import dis
import types
import struct

def g(a):
    print(a)
print(g.__code__.co_varnames)

def make_int(i):
    return struct.pack('I', i)
def make_pointer(p):
    return struct.pack('P', p)

evil_struct = {
    'code': bytes([
        dis.opmap['LOAD_CONST'], 0, # load None
        dis.opmap['RETURN_VALUE'], 0 # return it
    ]),
    'consts': (None,),
    'names': (),
    'varnames': (),
    'freevars': (),
    'cellvars': (),
    'filename': '<dummy>',
    'name': 'evil_code',
    'lnotab': b'\x02\x00',
    'weakreflist': []
}
evil_array = struct.pack(
    'iiiiiiPPPPPPPPPPPPP',
    0, # posonlyargcount
    0, # kwonlyargcount
    0, # nlocals
    1, # stack size
    0, # flags
    666, # first line no
    id(evil_struct['code']),
    id(evil_struct['consts']),
    id(evil_struct['names']),
    id(evil_struct['varnames']),
    id(evil_struct['freevars']),
    id(evil_struct['cellvars']),
    0, # cell2arg
    id(evil_struct['filename']),
    id(evil_struct['name']),
    id(evil_struct['lnotab']),
    0, # zombieframe
    0, # weakreflist
    0 # extra
)
    
# def f(): print('hello world')
# evil_array = f.__code__
fn_name = 'evil_fn'
evil_fn = None

load_bytes_as_fn_co_code = bytes([
    dis.opmap['LOAD_GLOBAL'], 0, # load evil_array
    dis.opmap['LOAD_GLOBAL'], 1, # load 'evil_fn'
    dis.opmap['MAKE_FUNCTION'], 0, # make evil bytes into function
    dis.opmap['STORE_GLOBAL'], 2, # store into evil_fn
    dis.opmap['LOAD_CONST'], 0, # load None
    dis.opmap['RETURN_VALUE'], 0 # return it
])
load_bytes_as_fn_co = types.CodeType(
    0, 0, 0, 2, 0,
    load_bytes_as_fn_co_code,
    (None,), # consts
    ('evil_array', 'fn_name', 'evil_fn'), # names
    (),
    '<inline>',
    '<lambda>',
    1,
    b'\x06\x00', # lnotab
    (), # freevars
    () # cellvars
)
dis.disassemble(load_bytes_as_fn_co)
print(evil_fn)
exec(load_bytes_as_fn_co)
print(evil_fn)
evil_fn()
