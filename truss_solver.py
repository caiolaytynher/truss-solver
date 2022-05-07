import numpy as np
from numpy.linalg import solve
import json
import sys


def load_data(filepath: str) -> dict:
    """
    Loads a json file as a python dictionary.
    """
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_data(filepath: str, data: dict) -> None:
    """
    Saves a python dictionary as a json file.
    """
    with open(filepath, "w") as file:
        json.dump(data, file)


def get_list_of_names(string_of_names: str, sep=",") -> list[str]:
    """
    Convert a string of names into a list of names based of a separator,
    comma (,) by default.

    This function is space insensitive.
    """
    list_of_names = string_of_names.split(sep)

    for i, name in enumerate(list_of_names):
        list_of_names[i] = name.strip()

    return list_of_names


def is_number(value: str) -> bool:
    """
    Checks if a string value is a valid number.
    """
    if str(value).replace(".", "0").isdigit():
        return True

    return False


def get_nodes_list(num_of_nodes: int) -> list[str]:
    """
    Creates a list of characters in alphabetical order in the
    specified size.
    """
    nodes = []
    for i in range(num_of_nodes):
        nodes.append(chr(ord("A") + i))

    return nodes


def handle_multiplier(multiplier: str, negative: bool) -> float:
    """
    Translates the string multiplier to an actual numeric value.
    """
    value = 0
    if "/" in multiplier:
        num, denom = multiplier.split("/")
        value = float(num) / float(denom)

    elif "sin" in multiplier:
        multiplier = multiplier.replace("sin", "")
        value = np.sin(float(multiplier) * np.pi / 180)

    elif "cos" in multiplier:
        multiplier = multiplier.replace("cos", "")
        value = np.cos(float(multiplier) * np.pi / 180)

    else:
        value = float(multiplier)

    return -value if negative else value


def generate_data(file_name) -> None:
    """
    Generates the data necessary to run the main function.
    """
    while True:
        num_of_nodes = input("number of nodes: ")
        if is_number(num_of_nodes):
            num_of_nodes = int(num_of_nodes)
            break

        print("This value is not a number. Please try again.")

    string_of_names = input("name the forces: ")
    nodes = get_nodes_list(num_of_nodes)

    expressions = []
    for node in nodes:
        for type_of_forces in ["horizontal", "vertical"]:
            expression = input(f"{type_of_forces} forces in node {node}: ")
            expressions.append(expression)

    data = {"stringOfNames": string_of_names, "expressions": expressions}

    save_data(file_name, data)


def main(arguments) -> None:
    if len(arguments) > 1:
        file_name = arguments[1]
        data = load_data(file_name)
    else:
        generate_data("./output.json")
        data = load_data("./output.json")

    string_of_names = data["stringOfNames"]
    force_names = get_list_of_names(string_of_names)
    expressions = data["expressions"]

    forces_template = {}
    for name in force_names:
        forces_template[name] = 0

    forces_matrix = []
    forces_vector = np.zeros(len(force_names))
    for i, expression in enumerate(expressions):
        forces_dict = forces_template.copy()
        node_forces = get_list_of_names(expression, sep="+")
        for force in node_forces:
            if is_number(force):
                forces_vector[i] += -float(force)
                continue

            negative = "-" in force
            force = force.replace("-", "")

            if "*" not in force:
                forces_dict[force] = -1 if negative else 1
                continue

            force_name, multiplier = force.split("*")

            value = handle_multiplier(multiplier, negative)
            forces_dict[force_name] = value

        forces_matrix.append(list(forces_dict.values()))

    for row in forces_matrix:
        print(row)

    print(forces_vector)

    solution = solve(forces_matrix, forces_vector)
    for name, value in zip(force_names, solution):
        print(f"{name} = {value:.2f}")


if __name__ == "__main__":
    main(sys.argv)
