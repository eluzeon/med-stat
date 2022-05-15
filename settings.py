#########
# CSV PARSER
#########
import datetime
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = True

CSV_INPUT_FIELDS_MAPPING = {
    ('Iteration', "Measurement iteration"): 'iteration',
    'Measurement time': 'measurement_time',
    'Pattern': 'pattern',
    'Object': 'object',
    'Dominant side': 'dominant_side',
    'Position': 'position',
    'Side': 'side',
    'Location': 'location',
    'State': 'state',
    'Frequency': 'frequency',
    'Stiffness': 'stiffness',
    'Decrement': 'decrement',
    'Relaxation': 'relaxation',
    'Creep': 'creep',
}

CSV_DELIMITER = ";"

######

EXPORT_PATH = os.path.join(
    PROJECT_DIR,
    "output"
)

EXCEL_FILE_NAME = "data.xls"
# список из 5 строк-цветов
EXCEL_DATA_COLORS = [
    '#FFCC00',
    '#00ff00',
    '#C0C0C0',
    '#FFCB99',
    '#6486A8'
]

EXPORT_DPI_MIN = 150
EXPORT_DPI_MAX = 200

#######
# разница во времени, при которой исследования считаются одинаковыми
# например, если разница между m1 и m2 - 15 минут, значит что эти исследования оба "до" или оба "после"
# т.е. грубо говоря из одной группы, система будет выбирать последнее исследование для сравнения (т.е. m2)
#
# по умолчанию 20 минут
SAME_MEAS_MAX_TIME_INTERVAL = datetime.timedelta(minutes=20)


SCHEMA_DATETIME_FORMATS = [
    "%m/%d/%Y %H:%M:%S %p",
    "%d.%m.%Y %H:%M"
]

DOT_GRAPH_COLORS = 'rgbc'

LOGGING_FILE_PATH = os.path.join(PROJECT_DIR, "app.logs")
