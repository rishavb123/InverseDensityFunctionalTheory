import csv
import numpy as np

class ReadOutputFiles():

    def __init__(self, path) -> None:
        self.path = path

    @staticmethod
    def __read_csv_file(f_path, flattened=False):
        rows = []
        with open(f_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if flattened:
                    if row[0].isdigit():
                        rows.append((
                            int(row[0]),
                            float(row[1])
                        ))
                else:
                    if row[0].isdigit() and row[1].isdigit() and row[2].isdigit():
                        rows.append((
                            int(row[0]),
                            int(row[1]),
                            int(row[2]),
                            float(row[3])
                        ))
        
        if flattened:
            full_length = max(row[0] for row in rows)
            dim_length = int(np.round(full_length ** (1/3)))
            sq_dim_length = dim_length * dim_length
            rows = [
                (row[0] % dim_length, (row[0] % sq_dim_length) // dim_length, row[0] // sq_dim_length, row[1])
                for row in rows
            ]

        return rows

    @staticmethod
    def __convert_rows_file_to_np(rows):
        lengths = [
            1 + max(row[i] for row in rows)
            for i in range(3)
        ]
        arr = np.empty(lengths)
        for row in rows:
            arr[row[0], row[1], row[2]] = row[3]
        return arr
    
    def __read_csv_file_np(self, f_name, flattened=False):
        rows = ReadOutputFiles.__read_csv_file(f"{path}/{f_name}", flattened=flattened)
        arr = ReadOutputFiles.__convert_rows_file_to_np(rows)
        return arr

    def get_converged_exc_density(self):
        return self.__read_csv_file_np("Converged_exc_density.csv")
    
    def get_feature_0(self):
        return self.__read_csv_file_np("feature_0_spin_type_0.csv")
    
    def get_feature_1(self):
        return self.__read_csv_file_np("feature_1_spin_type_0.csv")
    
    def get_hsmp_iter_0(self):
        return self.__read_csv_file_np("HSMP_iter_0_spin_0_SH_1_STEP_0.500000_RCUT_0.500000.csv")
    
    def get_xc_potential(self):
        return self.__read_csv_file_np("xc_potential.csv", flattened=True)

if __name__ == '__main__':
    path = '/storage/home/hcoda1/6/rbhagat8/data/sparc_runs/H2O/72834_-1.0--1.0--1.0_1.0-1.0-0.0_-1.0-0.0-1.0'
    # path = "C:/Users/risha/Downloads/sparc_data"
    reader = ReadOutputFiles(path)
    arr = reader.get_converged_exc_density()

    print(arr[15, 30, 0])