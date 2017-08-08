from measurement import Measurement


class CSVDataParser:

    @staticmethod
    def parse(csv_data):
        if csv_data is None or csv_data == '':
            return []

        data = csv_data.split('\n')
        names = data[0].split(',')

        try:
            mc_timestamp = float(data[-1])
        except ValueError:
            return []

        parsed_data = []
        for line in data[1:-1]:
            measurement = Measurement(names, line, mc_timestamp)
            parsed_data.append(measurement)
        return parsed_data


parser = CSVDataParser()
