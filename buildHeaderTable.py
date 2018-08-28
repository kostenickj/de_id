import csv
import sys
import pickle

def build_header(from_line):
    ret_list = []
    ret_dict = {}

    for i in range(0, len(from_line)):
        ret_list.append([str(i), from_line[i]])
        ret_dict[from_line[i]] = i
    return ret_list, ret_dict

def write_csv_file(f_name, list):
    f_out = open(f_name + '.csv', 'w')
    csv_out = csv.writer(f_out)
    for l in list:
        csv_out.writerow(l)
    f_out.close()
    return None

def write_dict_file(f_name, w_dict):
    f_out = open(f_name + '.pkl', 'wb')
    pickle.dump(w_dict, f_out)
    f_out.close()
    return None


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python buildHeaderTable.py csv_in file_name_root')
        sys.exit(0)

    fin = open(sys.argv[1], 'r')
    cin = csv.reader(fin)
    head_l = next(cin)
    fin.close()

    h_list, h_dict = build_header(head_l)

    write_csv_file(sys.argv[2], h_list)
    write_dict_file(sys.argv[2], h_dict)