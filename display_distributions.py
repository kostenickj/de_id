import csv, sys
import graph_utils as gu

def scale_first_entry(b_values, b_labels):
    x = len(b_values[0])
    y = len(b_values[1])
    scale_diff = x-y
    if scale_diff > 0:
        b_values[0] = b_values[0][:-scale_diff]
        b_labels[0] = b_labels[0] + 'scaled by 1' + '0' * scale_diff


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python display_distributions.py distribution_file.csv')
        sys.exit()

    fname = sys.argv[1]
    fin = open(fname, 'r')
    cin = csv.reader(fin)

    g_values = []
    g_labels = []
    x_axis_label = 'Bin range'
    y_axis_label = 'Bin Count'
    chart_title = next(cin)[0]
    hold_title = ''
    draw_chart = False

    for l in cin:
        if draw_chart:
            scale_first_entry(g_values, g_labels)
            gu.make_bar_chart(g_labels, g_values, x_axis_label, y_axis_label, hold_title, 'r')
            g_values = [l[1]]
            g_labels = [l[0]]
            draw_chart = False
        elif len(l) < 2:
            hold_title = chart_title
            chart_title = l[0]
            draw_chart = True
        else:
            g_labels.append(l[0])
            g_values.append(l[1])

    fin.close()