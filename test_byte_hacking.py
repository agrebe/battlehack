import dis
import types
import struct

# # Dummy
# payload = bytes([
#     dis.opmap['LOAD_CONST'], 0, # load None
#     dis.opmap['RETURN_VALUE'], 0 # return it
# ])
payload_consts = (None, 'hello world')
payload_names = ('print',)
payload = bytes([
    dis.opmap['LOAD_GLOBAL'], 0, # load print
    dis.opmap['LOAD_CONST'], 1, # load hello world
    dis.opmap['CALL_FUNCTION'], 1, # print(...)
    dis.opmap['LOAD_CONST'], 0, # load None
    dis.opmap['RETURN_VALUE'], 0 # return it
])
print('payload', payload)
evil_struct = {
    'code': payload,
    'consts': payload_consts,
    'names': payload_names,
    'varnames': (),
    'freevars': (),
    'cellvars': (),
    'filename': '<dummy>',
    'name': 'evil_code',
    'lnotab': str(len(payload)).encode('utf-8') + b'\x00',
    'weakreflist': []
}
evil_array = struct.pack(
    'iiPPPPPPPPPPPPP',
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
for i in range(256**2):
    test_evil_array = evil_array + chr(i%256).encode('utf-8') + chr(i//256).encode('utf-8')
    h = hash(test_evil_array) # cache the hash
    if h < 0:
        h += 2**64
    i1, i2 = h % 2**32, h >> 32
    if i1 < 2**28 and i2 < 2**28: break
evil_array = test_evil_array
argcount = len(evil_array)
    
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
# print('here!')
# import time
# time.sleep(3)
exec(load_bytes_as_fn_co)
print(evil_fn)
args = [0]*argcount
evil_fn(*args)
