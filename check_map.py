import pickle, sys

def print_map(fname):
    fin = open(fname, 'rb')
    c_map = pickle.load(fin)
    fin.close()

    for key in sorted(c_map.iterkeys()):
        print(key, c_map[key])

if __name__ == '__main__':
    fname = sys.argv[1]
    print_map(fname)