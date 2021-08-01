def save_to_file(filename, data):
    # assume that data is 2d
    f = open(filename, "w")

    for row in data:
        line = "\t".join(row)
        f.write(line)
        f.write("\n")

    f.close()


def save_cats_to_file(filename, data):
    f = open(filename, "w")

    for pair, cat in data:
        f.write(pair + " " + str(cat))
        f.write("\n")

    f.close()


def read_cats_from_file(filename):
    f = open(filename, "r", encoding="utf8")
    result_pairs = []
    result_cats = []
    for line in f:
        pair, cat = line.split(" ")
        result_pairs.append(pair)
        result_cats.append(int(cat))
    f.close()

    return result_pairs, result_cats


def read_pairs_file(filename):
    f = open(filename, "r", encoding="utf8")
    result = []
    for line in f:
        result.append(line.replace("\n", "").split("\t"))
    f.close()

    return result
