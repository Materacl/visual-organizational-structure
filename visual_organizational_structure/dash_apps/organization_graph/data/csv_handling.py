import pandas as pd
import io

from collections import deque


class Tree(object):
    def __init__(
            self,
            node_id,
            children=None,
            data=None,
            props=None,
            edge_data=None,
            edge_props=None,
    ):
        """
        A class to facilitate tree manipulation in Cytoscape.
        :param node_id: The ID of this tree, passed to the node data dict
        :param children: The children of this tree, also Tree objects
        :param data: Dictionary passed to this tree's node data dict
        :param props: Dictionary passed to this tree's node dict, containing the node's props
        :param edge_data: Dictionary passed to the data dict of the edge connecting this tree to its
        parent
        :param edge_props: Dictionary passed to the dict of the edge connecting this tree to its
        parent
        """
        if children is None:
            children = []
        if data is None:
            data = {}
        if props is None:
            props = {}
        if edge_data is None:
            edge_data = {}
        if edge_props is None:
            edge_props = {}

        self.node_id = node_id
        self.children = children
        self.data = data
        self.props = props
        self.edge_data = edge_data
        self.edge_props = edge_props
        self.index = {}

    def _dfs(self, search_id):
        if self.node_id == search_id:
            return self
        elif self.is_leaf():
            return None
        else:
            for child in self.children:
                result = child.dfs()
                if result:
                    return result

            return None

    def _bfs(self, search_id):
        stack = deque([self])

        while stack:
            tree = stack.popleft()

            if tree.node_id == search_id:
                return tree

            if not tree.is_leaf():
                for child in tree.children:
                    stack.append(child)

        return None

    def is_leaf(self):
        """
        :return: If the Tree is a leaf or not
        """
        return not self.children

    def add_children(self, children):
        """
        Add one or more children to the current children of a Tree.
        :param children: List of Tree objects (one object or more)
        """
        self.children.extend(children)

    def get_edges(self, recursion=True):
        """
        Get all the edges of the tree in Cytoscape JSON format.
        :return: List of dictionaries, each specifying an edge
        """
        edges = []

        for child in self.children:
            di = {"data": {"source": self.node_id, "target": child.node_id}}
            di["data"].update(child.edge_data)
            di.update(child.edge_props)
            edges.append(di)

        if recursion:
            for child in self.children:
                edges.extend(child.get_edges())

        return edges

    def get_nodes(self, recursion=True):
        """
        Get all the nodes of the tree in Cytoscape JSON format.
        :return: List of dictionaries, each specifying a node
        """
        di = {"data": {"id": self.node_id}}

        di["data"].update(self.data)
        di.update(self.props)
        nodes = [di]

        if recursion:
            for child in self.children:
                nodes.extend(child.get_nodes())
        else:
            for child in self.children:
                child_di = {"data": {"id": child.node_id}}

                child_di["data"].update(child.data)
                child_di.update(child.props)
                child_nodes = [child_di]
                nodes.extend(child_nodes)

        return nodes

    def get_elements(self, recursion=True):
        """
        Get all the elements of the tree in Cytoscape JSON format.
        :return: List of dictionaries, each specifying an element
        """
        if recursion:
            return self.get_nodes() + self.get_edges()
        else:
            return self.get_nodes(recursion=False) + self.get_edges(recursion=False)

    def find_by_id(self, search_id, method="bfs"):
        """
        Find a Tree object by its ID.
        :param search_id: the queried ID
        :param method: Which traversal method to use. Either "bfs" or "dfs"
        :return: Tree object if found, None otherwise
        """
        method = method.lower()

        if method == "bfs":
            return self._bfs(search_id)
        elif method == "dfs":
            return self._dfs(search_id)
        else:
            raise ValueError("Unknown traversal method")

    def create_index(self):
        """
        Generate the index of a Tree, and set it in place. If there was a previous index, it is
        erased. This uses a BFS traversal. Please note that when a child is added to the tree,
        the index is not regenerated. Furthermore, an index assigned to a parent cannot be
        accessed by its children, and vice-versa.
        :return: Dictionary mapping node_id to Tree object
        """
        stack = deque([self])
        self.index = {}

        while stack:
            tree = stack.popleft()
            self.index[tree.node_id] = tree

            if not tree.is_leaf():
                for child in tree.children:
                    stack.append(child)

        return self.index


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
            element_path = tuple([path for path in full_path[0:element_num] if path])
            if element_path not in paths:
                element_id = f"{id_str.upper()}{ids[id_str]}"
                paths[element_path] = element_id
                ids[id_str] += 1

                parent_path = tuple(filter(lambda x: x != "", full_path[:element_num - 1]))
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
            parent_path = tuple(filter(lambda x: x != "", full_path))
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


def find_parent_path(element_path: list) -> tuple:
    """
    Find the parent path of an element path.

    Args:
        element_path (tuple): The path of the element.

    Returns:
        tuple: The parent path.
    """
    return tuple(filter(lambda x: x != "", element_path[:-1]))
