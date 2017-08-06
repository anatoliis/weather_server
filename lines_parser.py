from measurement_line import MeasurementLine


class LinesParser:

    def parse(self, csv_data):
        if csv_data == None or csv_data == '':
            return []
        data = csv_data.split('\n')
        names = data[0].split(',')
        mc_timestamp = float(data.pop())
        data = data[1:]
        parsed_data = []
        for line in data:
            measurement = MeasurementLine(names, line, mc_timestamp)
            parsed_data.append(measurement)
        return parsed_data
