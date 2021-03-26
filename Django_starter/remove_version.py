import os


def remove_version_from_requirements(filename):
    # data_folder = os.path.join("Data")
    file_to_open = os.path.join(filename)

    requirement_file = open(file_to_open, 'r')
    # print(paintings_file.read())  # => Reading OK
    c = 0
    new_requirements = []

    for i in requirement_file.readlines():
        new_requirements.append(i.split('==')[0]+'\n')
    requirement_file.close()
    return new_requirements


def writing_requirements_to_file(new_requirements):
    # data_folder = os.path.join("Data", "Output")
    file_to_write = os.path.join('new_requirements.txt')

    writing_output = open(file_to_write, 'w')

    for i in new_requirements:
        writing_output.write(str(i))
    writing_output.close()

    return "new_requirements Ready"


writing_requirements_to_file(remove_version_from_requirements('requirements.txt'))
