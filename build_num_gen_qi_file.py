#! /usr/bin/env python3

import pickle, sys, csv
'''
Generates a .csv file using the quasi-identifier file replacing the actual value for the
numeric quasi-identifiers with the range determined in the tables created by the numeric
generalization mechanism used and stored in the various maps. 
'''
# todo When changing to a configuration file driven list of qis, will need to change this as well

def get_gen_map(fname):
    '''
    Read in a generalization map from a pickle in the file system
    :param fname: The name of the file containing the pickle
    :return: the map that is read in from the file
    '''
    fin = open(fname, 'rw')
    gen_map = pickle.load(fin)
    fin.close()
    return gen_map

def get_gen_val(f_map, in_val):
    '''
    Return the generalized value from the map. If the value read in is other than the empty
    string, the value is cast to an integer.
    :param f_map: The generalization map to be used
    :param in_val: The value to be generalized; this will always come in as a string but will be
        cast to an integer if it is non-empty
    :return: the generalized value
    '''
    if in_val == '':
        return f_map[''][0]
    else:
        ind = int(in_val)
        return f_map[ind][0]

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python build_num_gen_qi_file.py qi_csv_file_in qi_gen_file_out')
        sys.exit(1)

    fin_name = sys.argv[1]
    fin = open(fin_name, 'rU')
    qi_in_l = csv.reader(fin)

    fout_name = sys.argv[2]

    comments_map = get_gen_map('f_comments_map_qi_reg_with_tail.pkl')
    endorse_map = get_gen_map('f_endorsed_map_qi_reg_with_tail.pkl')
    post_map = get_gen_map('f_post_map_qi_reg_with_tail.pkl')
    thread_map = get_gen_map('f_threads_map_qi_reg_with_tail.pkl')
    votes_map = get_gen_map('f_votes_map_qi_reg_with_tail.pkl')
    yob_map = get_gen_map('yob_map_qi_reg_with_tail.pkl')

    fout = open(fout_name, 'w')
    qi_gen_out = csv.writer(fout)

    qi_gen_out.writerow(next(qi_in_l))

    for l in qi_in_l:
        l[8] = get_gen_val(yob_map, l[8])
        l[10] = get_gen_val(post_map, l[10])
        l[11] = get_gen_val(votes_map, l[11])
        l[12] = get_gen_val(endorse_map, l[12])
        l[13] = get_gen_val(thread_map, l[13])
        l[14] = get_gen_val(comments_map,l[14])
        qi_gen_out.writerow(l)

    fout.close()
    fin.close()









