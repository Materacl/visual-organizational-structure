import pandas as pd
import io
from dash_cytoscape.utils import Tree


class CSVHandler(Tree):
    """
    A class to handle CSV data and generate a tree structure.

    Args:
        company_name (str): The name of the company.
        csv_string (str): The CSV data in string format.

    Attributes:
        data (dict): A dictionary containing metadata about the company.
        csv_string (str): The CSV data in string format.
        content_df (pd.DataFrame): The DataFrame generated from the CSV data.
    """

    def __init__(self, company_name: str, csv_string: str) -> None:
        """
        Initializes the CSVHandler with the company name and CSV data.

        Args:
            company_name (str): The name of the company.
            csv_string (str): The CSV data in string format.
        """
        super().__init__('MAIN')
        self.data = {'label': company_name}
        self.csv_string = csv_string
        self.content_df = self._create_df_from_csv()
        self._generate_tree_from_csv()

    def _create_df_from_csv(self) -> pd.DataFrame:
        """
        Creates a DataFrame from the CSV string.

        Returns:
            pd.DataFrame: The DataFrame generated from the CSV data.
        """
        content_df = pd.read_csv(io.StringIO(self.csv_string)).fillna('')
        content_df = content_df[content_df["Номер позиции"] != ""]
        return content_df

    def _generate_tree_from_csv(self) -> None:
        """
        Generates a tree structure from the CSV data.
        """
        df = self.content_df

        paths = {(): 'MAIN'}
        ids = {
            "le": 0,
            "l": 0,
            "su": 0,
            "d": 0,
            "g": 0,
        }

        def create_children(full_path: list, element_num: int, id_str: str) -> None:
            """
            Create child node for the tree.

            Args:
                full_path (list): The full path of the node.
                element_num (int): The index of the element to create the child for.
                id_str (str): The ID prefix for the element.

            Returns:
                None
            """
            element_path = tuple(full_path[0:element_num])
            if element_path not in paths:
                element_id = f"{id_str.upper()}{ids[id_str]}"
                paths[element_path] = element_id
                ids[id_str] += 1

                parent_path = find_parent_path(element_path)
                parent_id = paths[parent_path]
                parent_node = self.find_by_id(parent_id)
                parent_node.children.append(Tree(element_id, data={'label': element_path[-1]}))

        def create_children_employee(full_path: list, employee_data: list) -> None:
            """
            Create child node of employee for the tree.

            Args:
                full_path (list): The full path of the employee node.
                employee_data (list): The data of the employee.

            Returns:
                None
            """
            parent_path = find_parent_path(tuple(full_path))
            parent_id = paths[parent_path]
            parent_node = self.find_by_id(parent_id)
            parent_node.children.append(Tree(employee_data[0], data={
                'label': employee_data[2], 'job_title': employee_data[1], 'job_type': employee_data[3]}))

        for _, row in df.iterrows():
            path = row[["ЮЛ", "Локация", "Подразделение", "Отдел", "Группа"]].tolist()

            # Legal Entity
            create_children(path, 1, 'le')

            # Locations
            create_children(path, 2, 'l')

            # Subinits
            create_children(path, 3, 'su')

            # Departmets
            create_children(path, 4, 'd')

            # Groups
            create_children(path, 5, 'g')

            # Employees
            data = row[["Номер позиции", "Должность", "ФИО", "Тип работы"]].tolist()
            create_children_employee(path, data)


def find_parent_path(element_path: tuple) -> tuple:
    """
    Find the parent path of an element path.

    Args:
        element_path (tuple): The path of the element.

    Returns:
        tuple: The parent path.
    """
    return tuple(filter(lambda x: x != "", element_path[:-1]))
