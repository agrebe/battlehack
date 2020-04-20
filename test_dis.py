import dis

# b = dis.Bytecode("""
# def f():
#   a = 1
#   b = 2
#   def g():
#     print(a, b)
# """).codeobj
# print(b.co_consts[0])
# dis.disassemble(b.co_consts[0])
# print(b.co_consts[0].co_consts[3])
# dis.disassemble(b.co_consts[0].co_consts[3])

b = dis.Bytecode("""
x = lambda y: y
""").codeobj
print(b)
dis.disassemble(b)
