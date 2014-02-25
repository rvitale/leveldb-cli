import cmd
import leveldb
import os


def db_selected(fn):
    def _decorator(self, *args, **kwargs):
        if self.db:
            fn(self, *args, **kwargs)
        else:
            print 'No database selected!'
    return _decorator


class LevelDBCLI(cmd.Cmd, object):
    """Simple command processor example."""
    
    prompt = 'leveldb> '
    db = None
    HISTORY_PATH = '/tmp/.leveldb.history' 
    ignored_commands = set(('EOF', 'history'))
    
    def preloop(self):
        if os.path.exists(self.HISTORY_PATH):
            with open(self.HISTORY_PATH) as f:
                self._hist = [c.strip() for c in f]
        else:
            self._hist = []

    def precmd(self, line):
        c = line.strip()
        if c not in self.ignored_commands:
            self._hist.append(c)
        return line

    def do_history(self, line):
        for i, c in enumerate(self._hist):
            print i, c

    def do_open(self, path):
        "Greet the person"
        self.db = leveldb.LevelDB(path)

    @db_selected
    def do_put(self, key, value):
        self.db.Put(key, value)
    
    @db_selected
    def do_get(self, key):
        print self.db.Get(key)

    def do_EOF(self, line):
        with open('/tmp/.leveldb.history', 'a') as f:
            for c in self._hist:
                f.write('%s\n' % c)
        print
        return True


if __name__ == '__main__':
    cli = LevelDBCLI()
    cli.cmdloop()
