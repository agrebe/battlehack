# Need to use something other than blocks to ensure we have control of the stack
# when we jump.
# def break_it():
#     a = 1
#     for r in [0]:
#         {}
#     for r in [0]:
#         {}
#         {}
#         {}
#         {}
#         {}
#         {}
#         {}
        
#     def dummy():
#         pass
#     def dummy2():
#         pass
#     def dummy3():
#         pass
#     def evil():
#         log("a")
#     evil()

# This almost works, but unclear how to construct C-backed code object in payload
def call_code(payload):
    a = True + (True if True or False else False)
    {}
    {}
    {}
    {}
    a = payload + (True if True or False else False)
    b = {}
    b = b = b = b = b = {}
    {}
    {}
    {}
    {}
    def evil():
        pass
    evil()

def turn():
    # break_it()
    call_code(b'')
