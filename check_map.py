import cPickle, sys

def print_map(fname):
    fin = open(fname, 'r')
    c_map = cPickle.load(fin)
    fin.close()

    for key in sorted(c_map.iterkeys()):
        print key, c_map[key]

if __name__ == '__main__':
    fname = sys.argv[1]
    print_map(fname)