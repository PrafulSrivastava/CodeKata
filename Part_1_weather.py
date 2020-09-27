import numpy as np
import pandas as pd

DIC = {}  # Global dictionary to store token index and whitespace barrier
FULL_SET = "  15  64    55    60       5  54.9   0   0.00 F       040  4.3 200   7  9.6  96 70 1006.1"


# Using an input with every column filled to make a generic assumption about the input

# Understand function uses the FULL_SET to populate the global Dictionary with {index:whitespaceSize}
# For Ex: "  15" => {0,2} which means after 2 spaces we get the first or Zeroth token
def understand(str):
    ls = []  # list to store count of white spaces
    index = 0
    cnt = 0
    flag = False
    ws_cnt = 0  # white space count
    for x in str:
        if x != " ":  # if not whitespace
            if not flag:  # if first digit of number
                ls.append(ws_cnt)  # add ws_count to list
                index += 1  # increment index suggesting one token found
                flag = True  # set to True so that every digit is not considered a token
                ws_cnt = 0  # white space count reset
        else:
            ws_cnt += 1
            flag = False
        cnt += 1

    # print(ls)

    DIC = pd.Series(ls).to_dict()  # populating dictionary
    return DIC


# this function is used to fill NaN values by using DIC populated earlier to find position of tokens,
# then call parseNans function on every token of every line
def performParseNan(file_in, file_out):
    with open(file_out, "w") as file2:  # empty the file
        file2.write("")
    with open(file_in, "r") as file:  # open input file
        line = file.readline()  # got header line
        with open(file_out, "a") as newfile:  # insert header line
            newfile.write(line.strip() + "\n")
        header_flag = False
        line_count = 1
        while True:
            line = file.readline()  # get next line
            if line.strip():  # remove spaces or only spaced line will not be considered NULL
                i = 1
                temp = 0
                if line_count < 10:  # 1 digit index adjustment
                    temp = line[DIC[0] + 1]
                else:
                    temp = line[DIC[0]]
                if temp.isdigit():
                    while i < len(DIC) - 1:  # remove garbage
                        line = parsefilNaNs(line, i, DIC[i], "nan")
                        i += 1
                    with open(file_out, "a") as newfile:  # insert result.
                        newfile.write(line.strip() + "\n")
            else:
                break
            line_count += 1

# fill empty values with NaN
def parsefilNaNs(str, col, nxt_col, rep):
    index = 0
    cnt = 0
    flag = False
    for x in str:
        if x != " ":
            if not flag:
                index += 1
            flag = True
        else:
            flag = False
        if index == col:
            break
        cnt += 1
    while str[cnt] != " ":
        cnt += 1
    change_flag = False
    if str[cnt + nxt_col] == " ":
        change_flag = True
    if nxt_col > 1:
        if str[cnt + nxt_col - 1] != " ": # formatting restructure to prevent new NaN columns from getting created
            change_flag = False
    if change_flag:
        str = str[:cnt + nxt_col] + rep + str[cnt + nxt_col + 1:] # "7    78" becomes "7  NaN 78" , id a column with no value existed
    return str

# make the whitespace seperated list to a comma seperated list
def parsefile(file_in, file_out):
    with open(file_out, "w") as file2:
        file2.write("")
    with open(file_in, "r") as file:
        line = file.readline()
        header_flag = False

        while line:
            line = line.replace("-", "")
            i = 0
            sp = []
            str = ","
            sp = line.split()
            str = str.join(sp)
            while line[i] == " ":
                i += 1
            if line[i].isdigit():
                with open(file_out, "a") as newfile:
                    newfile.write(str + "\n")
            elif not header_flag:
                header_flag = True
                with open(file_out, "a") as newfile:
                    newfile.write(str + "\n")
            line = file.readline()


def main():
    global DIC, FULL_SET

    full_set = FULL_SET
    file_out = "file_out.txt"
    df = pd.read_csv("weather.dat")
    file = "wearher.txt"
    print("Enter column 1")
    col1 = input()
    print("Enter column 2 to find difference")
    col2 = input()
    DIC = understand(full_set) # populate DIC
    performParseNan(file, file_out) # Fill Empty values
    file = file_out
    file_out = "file_out2.txt"

    parsefile(file, file_out) # create new comma seperated output file
    df = pd.read_csv(file_out) # convert ouput to Dataframe
    mxt_lst = []
    min_lst = []
    diff = []
    for i in range(0, len(df[col1])):
        mxt_lst.append(float(df[col1][i].replace("*", ""))) # converting string to float for substraction
        min_lst.append(float(df[col2][i].replace("*", "")))

    df_res = pd.DataFrame(df['Dy'])# Adding days column to result dataframe
    # df_res.append({"MxT":mxt_lst,"MnT": min_lst})
    df_res[col1] = mxt_lst
    df_res[col2] = min_lst
    df_res["Diff"] = abs(df_res[col1] - df_res[col2]) # calculating absolute difference
    min = df_res["Diff"].min(axis=0, skipna=True) # finding row with min difference
    print("|********Minimum Difference row:")
    print(df_res[df_res["Diff"] == min].to_string(index=False))# result


if __name__ == '__main__':
    main()
