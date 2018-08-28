'''
A simple program to replace directory information in the log files for CS50X with randomly generated identifiers. The
identifiers that are generated need to be consistent both within a file and across files; that is, if a student is
mapped to a random identifier in one line of a file, that same random identifier should be used for that student in
other entries in that file, and in entries in other files.

Since this might be run again on additional log files, the mapping from current id -> random id should be saved so that
incremental runs can be done, rather than re-running all of the files.

The directory information that needs to be obfuscated is the username and the user_id (which is part of the context). We
will generate a random number between 0 and 10,000,000 that will be used to replace both. We will keep track of a mapping
from the user_id to the new random id to insure that we can re-use the same random id for a student, and also keep a set
of the random numbers that have been used to insure that the ids assigned to replace the name and user_id are unique.
'''

import os, cPickle, json, random, sys


def get_id_pickles(map_name, set_name):
    '''
    Get the dictionary mapping real ids to random numbers, and the set of random numbers already in use for ids

    The routine will open the files specified in the command line that contains the pickles for the dictionary and the
    set. If these files do not exist or cannot be read, and empty dictionary and set are created. If the files do exist,
    the files are opened for reading, the pickle used to reconstruct the dictionary and set, and the files are closed.
    The resulting dictionary and set are returned
    :param map_name: name of the file containing the pickle of the id->random_id dictionary
    :param set_name: name of the file containing the pickle of the set of random ids already in use
    :return: the dictionary from actual ids to random ids, and the set of random ids in use
    '''
    try:
        id_file = open(map_name, 'r')
        id_m = cPickle.load(id_file)
        id_file.close()
    except:
        id_m = {}

    try:
        id_set_file = open(set_name, 'r')
        id_s = cPickle.load(id_set_file)
        id_set_file.close()
    except:
        id_s = set()

    return id_m, id_s


def write_id_pickle(id_m, id_s, m_name, s_name):
    '''
    Write the real_id->random id table and the random_id set to disk

    Taking the names of the files for the pickles of the real_id to randomly generated id dictionary and the set that is
    the random ids, write a pickle to files named. This will overwrite the files that were used to read the dictionary
    and set at the beginning of the program run.
    :param id_m:  the real_id->random_id dictionary
    :param id_s:  the set of the random_ids
    :param m_name: name of the file to write the pickle of the dictionary
    :param s_name: name of the file to write the pickle of the set
    :return: None
    '''
    m_fout = open(m_name, 'w')
    cPickle.dump(id_m, m_fout)
    m_fout.close()

    s_fout = open(s_name, 'w')
    cPickle.dump(id_s, s_fout)
    s_fout.close()


def get_random_id(real_id, real_dict, random_set):
    '''
    Generate a random id to use to replace the actual user id and user name

    This routine will first check to see if the user_id has already been mapped to a random id. If it has, the previously
    generated id is returned. If not, a unique random number between 0 and 10,000,000 is generated, added to the mapping
    and set of random numbers used, and returned
    :param real_id:  real user_id to be replaced by a random number
    :param real_dict: dictionary mapping real_ids to random ids
    :param random_set: the set of random ids that are already in use
    :return: a random number to replace the actual id and user name
    '''
    if real_id in real_dict:
        return real_dict[real_id]

    new_id = random.randint(0, 10000000)
    while new_id in random_set:
        new_id = random.randint(0, 10000000)

    real_dict[real_id] = new_id
    random_set.add(real_id)
    return new_id


def make_did_file(fname_in, id_dict, idset):
    '''
    Reads through the log file, replacing the user_name and user_id fields with a random number

    The random number is remembered so that the same user id and user name will be replaced by the same number. The
    resulting line will be written to a file with the same file name with 'deId' appended to the root name
    :param fname_in: name of the file containing the log entries to be deidentified
    :param id_dict: dictionary mapping actual user_ids to random_ids
    :param idset: set of random_ids that are in use
    :return:
    '''
    print('Beginning deidentification of file', fname_in)
    outfilename = fname_in[:-5] + 'deId' + '.json'
    inf = open(fname_in, 'r')
    outf = open(outfilename, 'w')

    for l in inf:
        try:
            jl = json.loads(l)
            new_id = get_random_id(jl['context']['user_id'], id_dict, idset)
            jl['username'] = new_id
            jl['context']['user_id'] = new_id
            outf.write(json.dumps(jl))
        except:
            pass

    inf.close()
    outf.close()
    return


if __name__ == '__main__':

    num_files = len(sys.argv)
    if num_files < 4:
        print('Usage: python simpleCS50deId.py id_map_file.pkl id_set_file.pkl file_to_convert.json...')
        sys.exit(1)

    id_map_name = sys.argv[1]
    id_set_name = sys.argv[2]
    id_map, id_set = get_id_pickles(id_map_name, id_set_name)

    flist = []
    for i in range(1, num_files):
        if sys.argv[i][-4:] == 'json':
            flist.append(sys.argv[i])

    for fname in flist:
        make_did_file(fname, id_map, id_set)

    write_id_pickle(id_map, id_set, id_map_name, id_set_name)
