import csv, sys
import graph_utils as gu
import display_distributions as dd

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python display_distributions.py distribution_file.csv'
        sys.exit()

    fname = sys.argv[1]
    fin = open(fname, 'r')
    cin = csv.reader(fin)

    title_lst = []
    values_lst = []
    labels_lst = []
    v_lst = []
    l_lst = []
    x_axis_lst = []
    y_axis_lst = []
    color_lst = []
    x_axis_label = 'Bin Range'
    y_axis_label = 'Bin Count'
    title_lst.append(cin.next())
    x_axis_lst.append(x_axis_label)
    y_axis_lst.append(y_axis_label)
    color_lst.append('r')
    c_count = 1

    for l in cin:
        if len(l) < 2:
            title_lst.append(l[0])
            c_count += 1
            dd.scale_first_entry(v_lst, l_lst)
            values_lst.append(v_lst)
            labels_lst.append(l_lst)
            x_axis_lst.append(x_axis_label)
            y_axis_lst.append(y_axis_label)
            color_lst.append('r')
            v_lst = []
            l_lst = []
        else:
            v_lst.append(l[1])
            l_lst.append(l[0])

    dd.scale_first_entry(v_lst, l_lst)
    values_lst.append(v_lst)
    labels_lst.append(l_lst)

    fin.close()
    gu.make_multi_bar_chart(c_count, labels_lst, values_lst, x_axis_lst, y_axis_lst, title_lst, color_lst)