import xcffib
import xcffib.xproto

def Connection():
    def ___init__(self):
        self.conn = xcffib.Connection()
        self.setup = self.conn.setup
        self.core = self.conn.core
        self.__atom_cache = {}
        self.code_to_syms = {}
        self.sym_to_codes = {}
    
    # Returns the atom for any atom name
    def get_atom(self, name):
        if name in __atom_cache: return __atom_cache[name]
        __atom_cache[name] = self.core.InternAtom(False, len(name), name).reply().atom

    # Refresh the keycode to keysym map and the keysym to keycode map
    def refresh_keymap(self):
        self.code_to_syms = {}
        self.sym_to_codes = {}
        first = self.setup.min_keycode
        count = self.setup.max_keycode - self.setup.min_keycode + 1
        mapping = self.core.GetKeyboardMapping(first, count).reply()
        for i in range(mapping.keysyms):
            code = i // mapping.keysyms_per_keycode
            sym = mapping.keysyms[i]
            if code not in self.code_to_syms: self.code_to_syms[code] = [sym]
            else: self.code_to_syms[code].append(sym)
            if sym not in self.sym_to_codes: self.sym_to_codes[sym] = [code]
            else: self.sym_to_codes[sym].append(code)
    
    # This function gets called only once and applys only to modkeys (shift ctrl etc)
    def refresh_modmap(self):
        pass
