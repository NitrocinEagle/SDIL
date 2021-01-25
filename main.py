import configparser
import csv
import os
from datetime import datetime

COLUMNS = {
    'date': 'date',
    'operation': 'type',
    'amount': 'amount',
    'from': 'from',
    'to': 'to'
}


class CSVDataSource:
    source_folder = None
    source_filename = None

    # Columns
    date = COLUMNS['date']
    operation = COLUMNS['operation']
    amount = COLUMNS['amount']
    _from = COLUMNS['from']
    to = COLUMNS['to']

    source_date_formats = ['%b %d %Y', '%d-%m-%Y', '%d %b %Y']
    unified_date_fmt = None

    def __init__(self, config: configparser.ConfigParser):
        self.source_folder = config['main']['source_folder']
        self.unified_date_fmt = config['formats']['date_fmt']

    def unify_data(self):
        unified = []
        with open(os.path.join(self.source_folder, self.source_filename), 'r', encoding='UTF-8') as csv_file:
            row_data = csv.DictReader(csv_file)
            for row in row_data:
                unified.append(self.process_row(row))
                unified.append('\n')
        return unified

    def process_amount(self, row):
        euro = row[self.amount].split('.')[0]
        cents = row[self.amount].split('.')[1]
        if len(cents) == 1:
            cents = f'{cents}0'

        return f'{euro}.{cents}'

    def process_date(self, row):
        for fmt in self.source_date_formats:
            try:
                old_date = datetime.strptime(row[self.date], fmt)
                new_date = old_date.strftime(self.unified_date_fmt)
            except ValueError:
                pass
            else:
                return new_date
        return 'NA'

    def process_row(self, row):
        date = self.process_date(row)
        operation_type = row[self.operation]
        amount = self.process_amount(row)
        _from = row[self._from]
        to = row[self.to]

        return ','.join([date, operation_type, amount, _from, to])


class Bank1Source(CSVDataSource):
    source_filename = 'bank1.csv'
    date = 'timestamp'


class Bank2Source(CSVDataSource):
    source_filename = 'bank2.csv'

    operation = 'transaction'
    amount = 'amounts'


class Bank3Source(CSVDataSource):
    source_filename = 'bank3.csv'

    date = 'date_readable'

    def process_amount(self, row):
        return f'{row["euro"]}.{int(row["cents"]):02d}'


def unify_data(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    unified_folder = config['main']['unified_folder']
    unified_filename = config['main']['unified_filename']

    bank_sources = [Bank1Source, Bank2Source, Bank3Source]

    with open(os.path.join(unified_folder, unified_filename), 'w', encoding='UTF-8') as f:
        f.write(f'{",".join(COLUMNS.keys())}\n')
        for source in bank_sources:
            f.writelines(source(config).unify_data())


if __name__ == '__main__':
    unify_data("config.ini")
