def generate_directory_name(name):
    directory_name = "".join([char.lower() for char in name if char.isalpha() or char.isdigit()]).rstrip()
    return directory_name
