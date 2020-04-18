import sys
import traceback
import pdb
from RestrictedPython import safe_builtins, limited_builtins, utility_builtins, Guards

class RobotRunner():
    def __init__(self, code, game_methods, log_method, error_method, *, debug):
        self.locals = {}
        self.globals = {
            '__builtins__': dict(i for dct in [safe_builtins, limited_builtins] for i in dct.items()),
            '__name__': '__main__'
        }
        self.globals['__builtins__']['__metaclass__'] = type
        self.globals['__builtins__']['__import__'] = self.import_call
        self.globals['__builtins__']['_getitem_'] = self.getitem_call
        self.globals['__builtins__']['_write_'] = self.write_call
        self.globals['__builtins__']['_getiter_'] = lambda i: i
        self.globals['__builtins__']['_inplacevar_'] = self.inplacevar_call
        self.globals['__builtins__']['_unpack_sequence_'] = Guards.guarded_unpack_sequence
        self.globals['__builtins__']['_iter_unpack_sequence_'] = Guards.guarded_iter_unpack_sequence
        
        self.globals['__builtins__']['log'] = log_method
        self.globals['__builtins__']['enumerate'] = enumerate
        self.globals['__builtins__']['set'] = set
        self.globals['__builtins__']['frozenset'] = frozenset
        self.globals['__builtins__']['sorted'] = sorted
        for key, value in game_methods.items():
            self.globals['__builtins__'][key] = value
        
        self.error_method = error_method
        self.game_methods = game_methods
        self.code = code
        self.imports = {}

        self.initialized = False
        self.debug = debug

        self.bytecode = 0 # TODO: set this to some estimate?


    @staticmethod
    def inplacevar_call(op, x, y):
        if not isinstance(op, str):
            raise SyntaxError('Unsupported in place op.')

        if op == '+=':
            return x + y

        elif op == '-=':
            return x - y

        elif op == '*=':
            return x * y

        elif op == '/=':
            return x / y

        else:
            raise SyntaxError('Unsupported in place op "' + op + '".')

    @staticmethod
    def write_call(obj):
        if isinstance(obj, type(sys)):
            raise RuntimeError('Can\'t write to modules.')

        elif isinstance(obj, type(lambda: 1)):
            raise RuntimeError('Can\'t write to functions.')

        return obj

    @staticmethod
    def getitem_call(accessed, attribute):
        if isinstance(attribute, str) and len(attribute) > 0:
            if attribute[0] == '_':
                raise RuntimeError('Cannot access attributes that begin with "_".')

        return accessed[attribute]

    def import_call(self, name, globals=None, locals=None, fromlist=(), level=0, caller='robot'):
        if not isinstance(name, str) or not (isinstance(fromlist, tuple) or fromlist is None):
            raise ImportError('Invalid import.')

        if name == '':
            # This should be easy to add, but it's work.
            raise ImportError('No relative imports (yet).')

        if not name in self.code:
            if self.debug and name == 'pdb':
                return pdb

            if name == 'random':
                import random
                return random
            
            if name == 'math':
                import math
                return math

            raise ImportError('Module "' + name + '" does not exist.')

        my_builtins = dict(self.globals['__builtins__'])
        my_builtins['__import__'] = lambda n, g, l, f, le: self.import_call(n, g, l, f, le, caller=name)
        run_globals = {'__builtins__': my_builtins, '__name__': name}

        # Loop check: keep dictionary of who imports who.  If loop, error.
        # First, we build a directed graph:
        if not caller in self.imports:
            self.imports[caller] = {name}
        else:
            self.imports[caller].add(name)

        # Next, we search for cycles.
        path = set()

        def visit(vertex):
            path.add(vertex)
            for neighbour in self.imports.get(vertex, ()):
                if neighbour in path or visit(neighbour):
                    return True
            path.remove(vertex)
            return False

        if any(visit(v) for v in self.imports):
            raise ImportError('Infinite loop in imports: ' + ", ".join(path))

        exec(self.code[name], run_globals)
        new_module = type(sys)(name)
        new_module.__dict__.update(run_globals)

        return new_module

    def init_robot(self):
        try:
            exec(self.code['bot'], self.globals, self.locals)
            self.globals.update(self.locals)
            self.initialized = True
        except Exception as e:
            self.error_method(traceback.format_exc(limit=5))
            if self.debug: raise

    def do_turn(self):
        if not self.initialized:
            self.init_robot()
        if 'turn' in self.locals and isinstance(self.locals['turn'], type(lambda: 1)):
            try:
                exec(self.locals['turn'].__code__, self.globals, self.locals)
            except:
                self.error_method(traceback.format_exc(limit=5))
                if self.debug: raise
        else:
            self.error_method('Couldn\'t find turn function.')

    def run(self):
        self.do_turn()
            
    def kill(self):
        pass
    def force_kill(self):
        pass
