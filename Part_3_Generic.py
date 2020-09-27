import numpy as np
import pandas as pd
import traceback
dic = {}
FULL_SET = "  15  64    55    60       5  54.9   0   0.00 F       040  4.3 200   7  9.6  96 70 1006.1"
# Using an input with every column filled to make a generic assumption about the input

# Understand function uses the FULL_SET to populate the global dictionary with {index:whitespaceSize}
# For Ex: "  15" => {0,2} which means after 2 spaces we get the first or Zeroth token

# enter a full row with no missing values to let the code understand the positions
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

    dic = pd.Series(ls).to_dict()  # populating dictionary
    return dic


# this function is used to fill NaN values by using dic populated earlier to find position of tokens,
# then call parseNans function on every token of every line
def performParseNan(file_in, file_out):
    with open(file_out, "w") as file2:  # empty the file
        file2.write("")
    with open(file_in, "r") as file:  # open input file
        line = file.readline()  # got header line
        with open(file_out, "a") as newfile:  # insert header line
            newfile.write(line.strip() + "\n")
        header_flag = False
        line_count = 0
        blank_count = 0
        while True:
            line = file.readline()  # get next line
            if line.strip():  # remove spaces or only spaced line will not be considered NULL
                i = 1
                temp = 0
                if line_count < 10:  # 1 digit index adjustment
                    temp = line[dic[0] + 1]
                else:
                    temp = line[dic[0]]
                if temp.isdigit():
                    while i < len(dic) - 1:  # remove garbage
                        line = parsefilNaNs(line, i, dic[i], "nan")
                        i += 1
                    with open(file_out, "a") as newfile:  # insert result.
                        newfile.write(line.strip() + "\n")
            else:
                if header_flag: # logic to skip 3 blank lines after header file, else exit
                    break
                blank_count +=1
                if blank_count == 3:
                    header_flag = True

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
    print("Enter Filename (full path)") # get Filename
    file = input()
    global dic
    print("Is the file well formatted (say N if there are no empty spaces ( for football.dat))?? Y or N") # Do not set to Y for football.dat since its already formatted
    choice = input()
    format_flag = False
    inflg = True
    file_out = "file_out.txt"

    while inflg:
        if choice == "Y":
            format_flag = True
            print("Intensive formatting required")
            inflg = False
        elif choice == "N":
            inflg = False
            print("Nominal formatting  required")
        else:
            print("Re-enter Y or N")

    if format_flag: # This flag is set for weather.dat because it has empty spaces
        print("Enter Full set with boundry spaces") # this is required as input , currently Hardcoding to reduce effort
        # full_set = input()
        full_set = FULL_SET
        dic = understand(full_set) # populating dictionary
        performParseNan(file, file_out) # filling empty values
        file = file_out
        file_out = "file_out2.txt"

    parsefile(file, file_out)
    df = pd.read_csv(file_out)

    df_res = pd.DataFrame(df.iloc[:, 0]) # Adding days column to result dataframe
    input_flag = False
    while not input_flag:
        print("Enter column 1")
        col1 = input()
        print("Enter column 2 to find difference")
        col2 = input()
        mxt_lst = []
        min_lst = []
        try:
            if (df[col1].dtype == "int64" or df[col1].dtype == "float64") and (df[col2].dtype == "int64" or df[col2].dtype == "float64"): # if the columns are not string do not worry about special character
                df_res[col1] = df[col1]
                df_res[col2] = df[col2]
            else:
                for i in range(0, len(df[col1])):
                    mxt_lst.append(float(df[col1][i].replace("*", "")))
                    min_lst.append(float(df[col2][i].replace("*", "")))
                df_res[col1] = mxt_lst
                df_res[col2] = min_lst
            input_flag = True
        except Exception as e:
            print("Wrong Column names, please re enter Error: ")
            traceback.print_exc()

    df_res["Diff"] = abs(df_res[col1] - df_res[col2]) # calculating absolute difference
    min = df_res["Diff"].min(axis=0, skipna=True) # finding row with min difference
    print("|********Minimum Difference row:")
    print(df_res[df_res["Diff"] == min].to_string(index=False))  # min row location


if __name__ == '__main__':
    main()
