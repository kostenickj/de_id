#! /usr/bin/env python

import cPickle, sys, csv

def get_gen_map(fname):
    fin = open(fname, 'rw')
    gen_map = cPickle.load(fin)
    fin.close()
    return gen_map

def get_gen_val(f_map, in_val):
    if in_val == '':
        return f_map[''][0]
    else:
        ind = int(in_val)
        return f_map[ind][0]

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: python build_num_gen_qi_file.py qi_csv_file_in qi_gen_file_out'
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

    qi_gen_out.writerow(qi_in_l.next())

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









