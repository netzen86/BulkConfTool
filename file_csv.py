from csv import DictReader


def get_cred(dev_file_name):
    dictionary = {}
    result = []
    with open(dev_file_name) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            dictionary.update(row)
            result.append(dictionary)
    return result


if __name__ == "__main__":
    print(get_cred('device.csv'))
