import numpy as np
import matplotlib.pyplot as plt


def make_bar_chart(x_labels, y_values, x_axis_label, y_axis_label, title, bar_color):
    if len(x_labels) != len(y_values):
        print('labels and values must match')
        return ()

    fig, ax = plt.subplots()
    index = np.arange(len(x_labels))
    bar_width = .4
    opacity = .4
    rects = ax.bar(index, y_values, bar_width, alpha=opacity, color=bar_color)
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(y_axis_label)
    ax.set_title(title)
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(x_labels)

    fig.tight_layout()
    plt.show()
    return


def build_bar_display(ax, x_labels, y_values, x_axis_label, y_axis_label, title, bar_color):
    index = np.arange(len(x_labels))
    bar_width = .4
    opacity = .4
    rects = ax.bar(index, y_values, bar_width, alpha=opacity, color=bar_color)
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(y_axis_label)
    ax.set_title(title)
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(x_labels)
    return


def make_multi_bar_chart(num_charts, x_label_arr, y_values_arr, x_axis_label_arr, y_axis_label_arr,
                         title_arr, bar_color_arr):
    '''
    Draw a canvas of multiple bar charts. This function will draw num_chart different charts on a single canvas,
    arranging them in two columns. The labels and values are passed in as lists of lists, the axis labels, titles, and
    bar colors as lists.
    :param num_charts: The number of charts to put on the canvas. Note that more than six will get messy
    :param x_label_arr: A list of lists of x axis tick labels
    :param y_values_arr: A list of lists of values determinig the height of the bar. Note that if the first bar is much larger than
    the second, it will be scaled by the difference in the orders of magnitude
    :param x_axis_label_arr:  a list of labels for the x axes
    :param y_axis_label_arr: a list of labels for the y axes
    :param title_arr:  a list of titles
    :param bar_color_arr: a list of colors for the bars
    :return:
    '''
    for i in range(0, num_charts):
        if len(x_label_arr[i]) != len(y_values_arr[i]):
            print('arrays must be of size number of charts')
            return

    num_rows = int(round(num_charts / 2.0))
    if num_charts > 1:
        num_cols = 2
    else:
        num_cols = 1

    fig, ax = plt.subplots(num_rows, num_cols, squeeze=False)
    for i in range(0, num_charts):
        a = ax[i / 2, i % 2]
        build_bar_display(a, x_label_arr[i], y_values_arr[i], x_axis_label_arr[i],
                          y_axis_label_arr[i], title_arr[i], bar_color_arr[i])

    fig.tight_layout()
    plt.show()
    return
