import os, cPickle, sys, csv

def print_bin_size(bin_map):
    bin_dict = {}
    bin_list = []
    for y in bin_map:
        span = bin_map[y][0]
        if span not in bin_dict:
            bin_dict[span] = bin_map[y][2]
    s_span = sorted(bin_dict.keys())
    for s in s_span:
        print s, bin_dict[s]
        bin_list.append([s, bin_dict[s]])

    return bin_list

def build_bin_size_list(bin_map):
    bin_list = []
    bin_set = set()
    bin_k = bin_map.keys()
    bin_k.sort()
    if bin_k[-1] == '':
        bin_k.insert(0, bin_k.pop())


    for k in bin_k:
        span = bin_map[k][0]
        if span not in bin_set:
            bin_set.add(span)
            bin_list.append([span, bin_map[k][2]])

    return bin_list

def shorten_name(fname):
    '''
    A particularly blecherous mechanism to strip most of the filename out of the name associated with the kind
    of quasi-identifier. This assumes that the name has a form that starts with f_, followed by the name we really
    want, followed by lots of stuff we don't. Unless it is the yob quasi-identifier, in which case there is no
    f_ preface. Sigh...
    :param fname: the file name from which to extract the quasi-identifier name
    :return: the name of the quasi-identifier
    '''
    if fname[:3] == 'yob':
        return 'yob'
    else:
        stop_i = fname[2:].find('_')
        stop_i += 2
        return fname[2:stop_i]

def store_bin_size(bin_name, store_file, bin_list):
    store_file.writerow([bin_name])
    for s in bin_list:
        store_file.writerow(s)
    return

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python getBinSizes.py outFile.csv {binfiles}'
        sys.exit(1)
    out_file_name = sys.argv[1]

    if len(sys.argv) < 3:
        f_list = os.listdir('.')
    else:
        f_list = []
        for n in range(2, len(sys.argv)):
            f_list.append(sys.argv[n])

    out_f = open(out_file_name, 'w')
    out_c = csv.writer(out_f)
    for f in f_list:
        if '.pkl' in f:
            f_in = open(f, 'r')
            bin_map = cPickle.load(f_in)
            s_list = build_bin_size_list(bin_map)
            #store_bin_size(shorten_name(f), out_c, s_list)
            store_bin_size(f,out_c, s_list)
            f_in.close()

    out_f.close()
