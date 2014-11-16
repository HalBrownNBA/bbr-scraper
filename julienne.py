from BeautifulSoup import BeautifulSoup
from collections import OrderedDict

class Julienne:
    def __init__(self, table):
        self.soup = BeautifulSoup(table.strip())
        self.row_list = self.soup.first("tbody").findAll("tr")

    def validate(self):
        valid_toplevel = len(self.soup.contents) == 1 and self.soup.contents[0].name == "table"
        num_columns = len(self.soup.first("thead").contents)
        rows = self.row_list
        valid_body = all([len(row) == num_columns for row in rows])
        return valid_toplevel and valid_body

    def columns(self):
        return [tag.string.strip() for tag in self.soup.findAll("th")]

    def rows(self):
        rows_sans_whitespace = [[unicode(field.string).strip() for field in row if field != '\n'] for row in self.row_list]
        return [OrderedDict(zip(self.columns(), row)) for row in rows_sans_whitespace]

    def select(self, **kwargs):
        # TODO: Implement selecting rows, possibly by some index
        desired_cols = kwargs['columns']
        rows = self.rows()
        return map(lambda row: { key: row.get(key, None) for key in desired_cols }, rows)


    def to_csv(self):
        csv_str = ",".join(self.columns()) + "\n"
        csv_str += "\n".join([",".join(row.viewvalues()) for row in self.rows()])
        return csv_str
        
    def transpose():
        pass
