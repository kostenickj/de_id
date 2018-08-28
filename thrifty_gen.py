#####
# Thrifty Algorithm Version in python 2.7
# Usage: python2 greedy_gen.py data_in data_out k [cols]
#####
import sys
import pandas as pd
import numpy as np
import copy


# this will be the function that does all the lumping
#   df -> the data, in a pandas dataframe
#   columns -> a list of columns that will be generalized on
#     this is in order of which to generalize first
#     will first generalize on columns[0], then columns[1], etc.
#   k -> level of k-anonymity, default to 5
#   outfile -> the file to write the steps to
#   returns the generalized dataframe

# this will be the function that does all the lumping
#   df -> the data, in a pandas dataframe
#   columns -> a list of columns that will be generalized on
#     this is in order of which to generalize first
#     will first generalize on columns[0], then columns[1], etc.
#   k -> level of k-anonymity, default to 5
#   outfile -> the file to write the steps to
#   returns the generalized dataframe
def thrifty(df, columns, k=5, outfile='out.txt'):
    df = copy.deepcopy(df)
    current = 0
    current_col = columns[current]

    def new_lump_col(x):
        acc = ""
        final = columns[-1]
        for c in columns[:-1]:
            acc += str(x[c])
            acc += "*"
        acc += str(x[final])
        return acc

    def lump(s, t1, t2):
        if s == t1 or s == t2:
            if str(t2)[-1] == '+':
                return str(t2)
            return str(t2) + '+'
        return s

    # set up file
    out = open(outfile, 'w')
    out.write("GENERALIZING BASED (IN ORDER) ON:\n")
    for c in columns:
        out.write("  " + c + "\n")
    out.write("\n\nSTEPS TO GENERALIZE\n")
    while (True):
        # PRE-LUMPING
        # before starting, see if we need to go to the next column to generalize on
        if (len(df[current_col].value_counts()) < 2):
            current += 1
            current_col = columns[current]
        # create the new columns we need
        df['lump_col'] = df.apply(lambda row: new_lump_col(row), axis=1)
        df['freq'] = df.groupby('lump_col')['lump_col'].transform('count')
        # check if finished
        if df['freq'].min() >= k:
            break
        # check if we can't make it because there is nothing left to do
        elif len(df['freq'].unique()) <= 1:
            out.write("Could not finish generalizing to " + str(k) + " anonymity.\n")
            out.close()
            return False

        # GENERALIZING
        # find the lowest
        temp = copy.deepcopy(df)
        row1 = df.loc[df['freq'] == df['freq'].min()].iloc[0]
        lump1 = row1[current_col]
        # try to generalize things of size n with things of size k-n
        sz1 = row1['freq']
        target = k - sz1
        df2 = df.loc[(df['freq'] == target) & (df[current_col] != lump1)]
        if not df2.empty:
            row2 = df2.iloc[0]
            lump2 = row2[current_col]
        # if we cannot find size k-n, then just lump the two smallest together
        else:
            temp = temp[temp[current_col] != lump1]
            row2 = temp.nsmallest(1, 'freq').iloc[0]
            lump2 = row2[current_col]
        sz2 = row2['freq']
        out.write("Combine: " + lump1 + " with " + lump2 + ", sizes(" + str(sz1) + ", " + str(sz2) + ")\n")
        # lump them together
        df[current_col] = df.apply(lambda row: lump(row[current_col], lump1, lump2), axis=1)
    # finally, return
    out.close()
    return df


#### Script of code
if len(sys.argv) < 5:
    print("Usage: python2 greedy_gen.py data_in data_out k [cols]\n")
    exit(1)

df = pd.read_csv(sys.argv[1])
k = int(sys.argv[3])
if k < 1:
    print("Please enter a valid value of k\n")
    exit(2)
cols = sys.argv[4:]
df_cols = list(df)
if not set(cols).issubset(set(df_cols)):
    print("Please enter valid column values\n")
    exit(3)
df2 = thrifty(df, cols, k)
df2.to_csv(sys.argv[2])
print("Data generalized to " + str(k) + " in " + sys.argv[2] + "\nStep by step process in out.txt\n")
exit(0)
