def save_to_file(filename, data):
    # assume that data is 2d
    f = open(filename, "a")

    for row in data:
        line = "\t".join(row)
        f.write(line)
        f.write("\n")

    f.close()


def read_pairs_file(filename):
    f = open(filename, "r", encoding="utf8")
    result = []
    for line in f:
        result.append(line.replace("\n" , "").split("\t"))

    return result
