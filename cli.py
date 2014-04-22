import cmd
import leveldb
import os
import readline
import rlcompleter
import signal
import sys


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

    def preloop(self):
        # self._original_sigint = signal.getsignal(signal.SIGINT)
        # signal.signal(signal.SIGINT, self._signal_handler)
        readline.parse_and_bind("tab: complete")
        if os.path.exists(self.HISTORY_PATH):
            readline.read_history_file(self.HISTORY_PATH)

    def do_history(self, line):
        for i in xrange(1, readline.get_current_history_length() + 1):
            print '%d\t%s' % (i, readline.get_history_item(i))

    def do_open(self, path):
        self.db = leveldb.LevelDB(path)

    @db_selected
    def do_put(self, line):
        key, value = line.strip().split()
        self.db.Put(key, value)

    @db_selected
    def do_get(self, line):
        key = line.strip()
        print self.db.Get(key)

    @db_selected
    def do_range_iter(self, line):
        keys = line.strip().split()
        if keys and len(keys) == 2:
            key_from, key_to = keys
            it = self.db.RangeIter(key_from, key_to)
        else:
            it = self.db.RangeIter()
        for el in it:
            print '%s\t->\t%s' % el

    @db_selected
    def do_delete(self, line):
        key = line.strip()
        self.db.Delete(key)

    @db_selected
    def do_get_stats(self, line):
        print self.db.GetStats()

    def do_EOF(self, line):
        print
        return self.exit()

    def do_exit(self, line):
        return self.exit()

    def do_quit(self, line):
        return self.exit()

    def exit(self):
        readline.write_history_file(self.HISTORY_PATH)
        return True

    def _signal_handler(self, signum, frame):
        signal.signal(signal.SIGINT, self._original_sigint)

        try:
            if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
                sys.exit(1)
        except KeyboardInterrupt:
            print("Ok ok, quitting")
            sys.exit(1)

        # restore the exit gracefully handler here
        signal.signal(signal.SIGINT, self._signal_handler)


if __name__ == '__main__':
    cli = LevelDBCLI()
    cli.cmdloop()
