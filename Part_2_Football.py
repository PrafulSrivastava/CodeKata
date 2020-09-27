import numpy as np
import pandas as pd


# make the whitespace seperated list to a comma seperated list
def parsefile(file_in, file_out):
    with open(file_out, "w") as file2:  # empty the file
        file2.write("")
    with open(file_in, "r") as file:
        line = file.readline()
        header_flag = False

        while line:
            line = line.replace("-", "")  # remove unrequired symbols
            i = 0
            sp = []
            str = ","
            sp = line.split()  # split into tokens
            str = str.join(sp)  # join with comma
            while line[i] == " ":  # move upto the first non space character
                i += 1
            if line[i].isdigit():  # write only if the line starts with a serial number
                with open(file_out, "a") as newfile:
                    newfile.write(str + "\n")
            elif not header_flag:
                header_flag = True  # set to true denoting first line has been parsed and the Headers have been extracted
                with open(file_out, "a") as newfile:
                    newfile.write(str + "\n")
            line = file.readline()


def main():
    file_out = "file_out.txt"
    file = "football.dat"
    df = pd.read_csv(file)
    parsefile(file, file_out)
    df = pd.read_csv(file_out)

    df_res = pd.DataFrame(df.iloc[:, 0])  # add first columnns to result dataframe
    # df_res.append({"MxT":mxt_lst,"MnT": min_lst})
    print("Enter column 1")
    col1 = input()
    print("Enter column 2 to find difference")
    col2 = input()
    df_res[col1] = df[col1]
    df_res[col2] = df[col2]
    df_res["Diff"] = abs(df_res[col1] - df_res[col2])  # absolute difference
    min = df_res["Diff"].min(axis=0, skipna=True)  # min value
    print("|********Minimum Difference row:")
    print(df_res[df_res["Diff"] == min].to_string(index=False))  # min row location


if __name__ == '__main__':
    main()
