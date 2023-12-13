import csv


def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            yield dict(zip(header, row))


def validate_data(model, data):
    for key in data:
        if "$" in key:
            key.replace("$", "")
    return model.model_validate(data)
