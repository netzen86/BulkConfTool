from csv import DictReader


def get_cred(dev_file_name):
    result = []
    with open(dev_file_name) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            result.append(dict(row))
    return result


if __name__ == "__main__":
    print(get_cred('device.csv'))
