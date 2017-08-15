from measurement import Measurement, ParseException
from helpers import generate_hash


class CSVDataParser:

    def parse(self, csv_data):
        if csv_data is None or csv_data == '':
            return []

        data = csv_data.split('\n')
        names = data[0].split(',')

        try:
            mcu_fetch_timestamp = float(data[-1])
        except ValueError:
            return []

        parsed_measurements = []
        for line in data[1:-1]:
            measurement_data = self._convert_to_data_dict(names, line)
            measurement_data['hash'] = generate_hash(line)
            try:
                parsed_measurements.append(
                    Measurement(measurement_data, mcu_fetch_timestamp)
                )
            except ParseException as exc:
                print(exc)
            
        return parsed_measurements

    @staticmethod
    def _convert_to_data_dict(names, line):
        values = tuple(map(float, line.split(',')))
        return dict(zip(names, values))


parser = CSVDataParser()
