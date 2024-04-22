from pprint import pprint

import pandas as pd
import json
import io

test_graph_nodes = [
    # ЮЛ
    {
        'data': {'id': 'LE1', 'label': 'БСЗ'},
    },

    # Локация
    {
        'data': {'id': 'L1', 'label': 'Брусника.Проектирование'},
    },
    {
        'data': {'id': 'L2', 'label': 'Дирекция'},
    },
    {
        'data': {'id': 'L3', 'label': 'Брусника.Тюмень'},
    },

    # Подразделение
    {
        'data': {'id': 'SU1', 'label': 'Подразделение ""Арес""'},
    },
    {
        'data': {'id': 'SU2', 'label': 'Подразделение ""Артемида""'},
    },
    {
        'data': {'id': 'SU3', 'label': 'Подразделение ""Афина""'},
    },
    {
        'data': {'id': 'SU4', 'label': 'Подразделение ""Афина""'},
    },
    {
        'data': {'id': 'SU5', 'label': 'Подразделение ""Афина""'},
    },

    # Отдел
    {
        'data': {'id': 'D1', 'label': 'Отдел ""Бельгия""'},
    },
    {
        'data': {'id': 'D2', 'label': 'Отдел ""Великобритания""'},
    },

    # Группа
    {
        'data': {'id': 'G1', 'label': 'Группа ""Москва""'},
    },
    {
        'data': {'id': 'G2', 'label': 'Группа ""Стамбул""'},
    },
    {
        'data': {'id': 'G3', 'label': 'Группа ""Лондон""'},
    },
    {
        'data': {'id': 'G4', 'label': 'Группа ""Санкт-Петербург""'},
    },
    {
        'data': {'id': 'G5', 'label': 'Группа ""Санкт-Петербург""'},
    },

    # Человек
    {
        'data': {'id': 'БСЗ131', 'label': 'Вакансия',
                 'job_title': 'Главный специалист-архитектор', 'job_type': 'Бизнес'},
    },
    {
        'data': {'id': 'БСЗ132', 'label': 'Вакансия',
                 'job_title': 'Специалист', 'job_type': 'Сервис'},
    },
    {
        'data': {'id': 'БСЗ133', 'label': 'Сотрудник Брусники 1',
                 'job_title': 'Специалист', 'job_type': 'Бизнес'},
    },
    {
        'data': {'id': 'БСЗ134', 'label': 'Сотрудник Брусники 2',
                 'job_title': 'Главный специалист-инженер', 'job_type': 'Бизнес'},
    },
    {
        'data': {'id': 'БСЗ135', 'label': 'Вакансия',
                 'job_title': 'Ведущий инженер', 'job_type': 'Бизнес'},
    },
]

# Add edges
test_graph_edges = [
    {'data': {'source': 'LE1', 'target': 'L1'}},
    {'data': {'source': 'LE1', 'target': 'L2'}},
    {'data': {'source': 'LE1', 'target': 'L3'}},

    {'data': {'source': 'L1', 'target': 'SU1'}},
    {'data': {'source': 'L1', 'target': 'SU2'}},
    {'data': {'source': 'L1', 'target': 'SU3'}},

    {'data': {'source': 'L2', 'target': 'SU4'}},

    {'data': {'source': 'L3', 'target': 'SU5'}},

    {'data': {'source': 'SU1', 'target': 'D1'}},
    {'data': {'source': 'SU1', 'target': 'D2'}},

    {'data': {'source': 'D1', 'target': 'G1'}},

    {'data': {'source': 'D2', 'target': 'G2'}},

    {'data': {'source': 'SU2', 'target': 'G3'}},

    {'data': {'source': 'SU3', 'target': 'G4'}},
    {'data': {'source': 'SU4', 'target': 'G5'}},

    {'data': {'source': 'G1', 'target': 'БСЗ131'}},

    {'data': {'source': 'G2', 'target': 'БСЗ132'}},

    {'data': {'source': 'D2', 'target': 'БСЗ133'}},

    {'data': {'source': 'G3', 'target': 'БСЗ134'}},
    {'data': {'source': 'G3', 'target': 'БСЗ135'}},
]

test_graph_data = test_graph_nodes + test_graph_edges


def create_node(node_id, label):
    return {
        'data': {'id': node_id, 'label': label},
    }


def create_node_employee(employee_id, label, job_title, job_type):
    return {
        'data': {'id': employee_id, 'label': label,
                 'job_title': job_title, 'job_type': job_type},
    }


def create_edge(source, target):
    return {
        'data': {'source': source, 'target': target},
    }


def generate_graph_data_from_csv(csv_content: str) -> json:
    # Read the CSV string into a DataFrame
    csv_file = io.StringIO(csv_content)
    df = pd.read_csv(csv_file).fillna('')

    # Nodes
    le_nodes = []
    l_nodes = []
    su_nodes = []
    d_nodes = []
    g_nodes = []
    e_nodes = []

    # Edges
    l_edges = []
    su_edges = []
    d_edges = []
    g_edges = []
    e_edges = []

    les = df[df["ЮЛ"] != ""]["ЮЛ"].unique()
    i = 0
    j = 0
    k = 0
    l = 0
    m = 0
    for le in les:
        le_id = f"LE{i}"
        le_nodes.append(create_node(le_id, le))
        i += 1

        le_df = df[df["ЮЛ"] == le]
        locs = le_df["Локация"].unique().tolist()
        for loc in locs:
            l_id = f"L{j}"
            l_nodes.append(create_node(l_id, loc))
            l_edges.append(create_edge(le_id, l_id))
            j += 1

            loc_df = le_df[df["Локация"] == loc]
            subunits = loc_df["Подразделение"][df["Подразделение"] != ""].unique().tolist()
            for subunit in subunits:
                su_id = f"SU{k}"
                su_nodes.append(create_node(su_id, subunit))
                su_edges.append(create_edge(l_id, su_id))
                k += 1

                subunit_df = loc_df[df["Подразделение"] == subunit]
                departments = subunit_df["Отдел"][df["Отдел"] != ""].unique().tolist()
                for department in departments:
                    d_id = f"D{l}"
                    d_nodes.append(create_node(d_id, department))
                    d_edges.append(create_edge(su_id, d_id))
                    l += 1

                    department_df = subunit_df[df["Отдел"] == department]
                    groups = department_df["Группа"][df["Группа"] != ""].unique().tolist()
                    for group in groups:
                        g_id = f"G{m}"
                        g_nodes.append(create_node(g_id, group))
                        g_edges.append(create_edge(d_id, g_id))
                        m += 1

                        group_df = department_df[df["Группа"] == group]
                        employees = group_df[["Номер позиции", "Должность", "ФИО", "Тип работы"]]
                        print(employees)

                        for employee in employees.itertuples(index=False):
                            e_nodes.append(create_node_employee(
                                employee[0],  # Номер позиции
                                employee[2],  # ФИО
                                employee[1],  # Должность
                                employee[3]  # Тип работы
                            ))
                            e_edges.append(create_edge(g_id, employee[0]))



            # nan_subunit_df = loc_df[df["Подразделение"] == ""]
            # nan_subunits_departments = nan_subunit_df["Отдел"].unique().tolist()
            # for nan_subunit in nan_subunit_df:
            #     print(nan_subunit)

    return le_nodes + l_nodes + l_edges + su_nodes + su_edges + d_nodes + d_edges + g_nodes + g_edges + e_nodes + e_edges


if __name__ == "__main__":
    print(generate_graph_data_from_csv(data))
