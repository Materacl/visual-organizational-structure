import pandas as pd

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


def generate_graph_data_from_csv(csv_content):
    # Read the CSV string into a DataFrame
    df = pd.read_csv(csv_content)

    # Initialize an empty dictionary to store the graph data
    graph_data = {
        'nodes': [],
        'edges': []
    }

    # Create nodes from unique positions and FIOs
    unique_positions = df['Номер позиции'].unique()
    unique_fios = df['ФИО'].unique()

    for position in unique_positions:
        graph_data['nodes'].append({'id': position, 'label': position, 'type': 'position'})

    for fio in unique_fios:
        graph_data['nodes'].append({'id': fio, 'label': fio, 'type': 'fio'})

    # Create edges based on relationships between positions and FIOs
    for _, row in df.iterrows():
        position = row['Номер позиции']
        fio = row['ФИО']

        # Add edge between position and FIO
        graph_data['edges'].append({'from': position, 'to': fio})

    return graph_data
