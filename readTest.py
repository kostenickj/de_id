import sys, csv

if __name__ == '__main__':
    fname = sys.argv[1]
    mode = sys.argv[2]
    fin = open(fname, 'rU')

    if mode == 'd':
        cin = csv.DictReader(fin)
    else:
        cin = csv.reader(fin)

    for l in cin:
        pass

    fin.close()