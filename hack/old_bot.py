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
