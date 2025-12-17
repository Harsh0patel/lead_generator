import pandas as pd

class Stage1:
    def __init__(self, name=None, title=None, company=None):
        self.name = name
        self.title = title
        self.company = company

    def identification(self, csv_path):
        data = pd.read_csv(csv_path)
        result = data.copy()

        filters = {
            'name': self.name,
            'company': self.company,
            'title': self.title
        }

        for column, value in filters.items():
            if value:
                result = result[
                    result[column].str.contains(value, case=False, na=False)
                ]

        if result.empty:
            return None

        return result
