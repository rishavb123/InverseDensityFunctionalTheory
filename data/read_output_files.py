from typing import Tuple

import os

import csv
import numpy as np

import tqdm


class ReadOutputFiles:
    def __init__(self, path, validate=True) -> None:
        """Initializes the ReadOutputFiles class

        Args:
            path (str): The folder path that includes all the sparc files
            validate (bool, optional): Whether or not to validate that all the files exist. Defaults to True.
        """
        self.path = path
        self.valid = True
        if validate:
            for fname in [
                "Converged_exc_density",
                "feature_0_spin_type_0",
                "feature_1_spin_type_0",
                "HSMP_iter_0_spin_0_SH_1_STEP_0.500000_RCUT_0.500000",
                "xc_potential",
            ]:
                if not os.path.exists(f"{path}/{fname}.csv"):
                    self.valid = False

    @staticmethod
    def __read_csv_file(f_path, flattened=False):
        """Reads a csv file into rows

        Args:
            f_path (str): The csv file path
            flattened (bool, optional): Whether or not the tensor in the csv file has been flattened or not. Defaults to False.

        Returns:
            list: The list of rows
        """
        rows = []
        with open(f_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            try:
                for row in csv_reader:
                    if flattened:
                        if len(row) > 1 and row[0].isdigit():
                            rows.append((int(row[0]), float(row[1])))
                    else:
                        if (
                            len(row) > 3
                            and row[0].isdigit()
                            and row[1].isdigit()
                            and row[2].isdigit()
                        ):
                            rows.append(
                                (int(row[0]), int(row[1]), int(row[2]), float(row[3]))
                            )
            except:
                pass

        if flattened:
            full_length = max(row[0] for row in rows)
            dim_length = int(np.round(full_length ** (1 / 3)))
            sq_dim_length = dim_length * dim_length
            rows = [
                (
                    row[0] % dim_length,
                    (row[0] % sq_dim_length) // dim_length,
                    row[0] // sq_dim_length,
                    row[1],
                )
                for row in rows
            ]

        return rows

    @staticmethod
    def __convert_rows_file_to_np(rows):
        """Converts the list of rows into a numpy array

        Args:
            rows (list): The list of rows

        Returns:
            np.array: The numpy array
        """
        lengths = [1 + max(row[i] for row in rows) for i in range(3)]
        arr = np.empty(lengths)
        for row in rows:
            arr[row[0], row[1], row[2]] = row[3]
        return arr

    def __read_csv_file_np(self, f_name, flattened=False):
        """Reads a csv file and returns it in an numpy array

        Args:
            f_name (str): The file name (relative to the instance variable self.path)
            flattened (bool, optional): Whether the csv tensor is flattened. Defaults to False.

        Returns:
            np.array: The numpy array
        """
        rows = ReadOutputFiles.__read_csv_file(
            f"{self.path}/{f_name}", flattened=flattened
        )
        arr = ReadOutputFiles.__convert_rows_file_to_np(rows)
        return arr

    def get_converged_exc_density(self):
        """Gets the converged exc density

        Returns:
            np.array: The converged exc density
        """
        return self.__read_csv_file_np("Converged_exc_density.csv")

    def get_feature_0(self):
        """Gets the feature 0 file

        Returns:
            np.array: The feature 0 file
        """
        return self.__read_csv_file_np("feature_0_spin_type_0.csv")

    def get_feature_1(self):
        """Gets the feature 1 file

        Returns:
            np.array: The feature 1 file
        """
        return self.__read_csv_file_np("feature_1_spin_type_0.csv")

    def get_hsmp_iter_0(self):
        """Gets the hsmp feature at iteration 0

        Returns:
            np.array: The hsmp feature at iteration 0
        """
        return self.__read_csv_file_np(
            "HSMP_iter_0_spin_0_SH_1_STEP_0.500000_RCUT_0.500000.csv"
        )

    def get_xc_potential(self):
        """Gets the converged xc potential

        Returns:
            np.array: The converged xc potential
        """
        return self.__read_csv_file_np("xc_potential.csv", flattened=True)


def read_all_data(
    path="/storage/home/hcoda1/6/rbhagat8/p-amedford6-0/sparc_runs",
    mol="H2O",
    ind_s=0,
    ind_e=-1,
) -> Tuple[np.array]:
    """Reads all the data of a specific molecule in a directory

    Args:
        path (str, optional): The path to look in. Defaults to "/storage/home/hcoda1/6/rbhagat8/data/sparc_runs/".
        mol (str, optional): The molecule name. Defaults to "H2O".
        ind_s (int, optional): The start index. Defaults to 0.
        ind_e (int, optional): The end index. Defaults to None.

    Returns:
        Tuple[np.array]: The converged_exc_densities, feature_0s, feature_1s, hsmp_iter_0s, and xc_potentials as numpy arrays
    """
    path = f"{path}/{mol}"
    dir_list = os.listdir(path)
    dir_list = list(dir_list)[ind_s:ind_e] if ind_e != None else list(dir_list)[ind_s:]

    converged_exc_density = []
    feature_0 = []
    feature_1 = []
    hsmp_iter_0 = []
    xc_potential = []

    print("Loading")

    for dir_name in tqdm.tqdm(dir_list):
        sparc_run_path = f"{path}/{dir_name}"
        reader = ReadOutputFiles(sparc_run_path)

        if not reader.valid:
            continue

        converged_exc_density.append(reader.get_converged_exc_density())
        feature_0.append(reader.get_feature_0())
        feature_1.append(reader.get_feature_1())
        hsmp_iter_0.append(reader.get_hsmp_iter_0())
        xc_potential.append(reader.get_xc_potential())

    print("Post processing")

    converged_exc_density = np.array(converged_exc_density)
    feature_0 = np.array(feature_0)
    feature_1 = np.array(feature_1)
    hsmp_iter_0 = np.array(hsmp_iter_0)
    xc_potential = np.array(xc_potential)

    return (
        converged_exc_density.flatten(),
        feature_0.flatten(),
        feature_1.flatten(),
        hsmp_iter_0.flatten(),
        xc_potential.flatten(),
    )


if __name__ == "__main__":
    # path = "/storage/home/hcoda1/6/rbhagat8/data/sparc_runs/H2O/72834_-1.0--1.0--1.0_1.0-1.0-0.0_-1.0-0.0-1.0"
    # # path = "C:/Users/risha/Downloads/sparc_data"
    # reader = ReadOutputFiles(path)
    # arr = reader.get_converged_exc_density()

    # print(arr[15, 30, 0])

    ind_s = 15000
    ind_e = 20000

    (
        converged_exc_density,
        feature_0,
        feature_1,
        hsmp_iter_0,
        xc_potential,
    ) = read_all_data(ind_s=ind_s, ind_e=ind_e)

    print("Saving")

    print(converged_exc_density.shape)
    print(feature_0.shape)
    print(feature_1.shape)
    print(hsmp_iter_0.shape)
    print(xc_potential.shape)

    np.save(f"dataset/converged_exc_density_{ind_s}_{ind_e}.npy", converged_exc_density)
    np.save(f"dataset/feature_0_{ind_s}_{ind_e}.npy", feature_0)
    np.save(f"dataset/feature_1_{ind_s}_{ind_e}.npy", feature_1)
    np.save(f"dataset/hsmp_iter_0_{ind_s}_{ind_e}.npy", hsmp_iter_0)
    np.save(f"dataset/xc_potential_{ind_s}_{ind_e}.npy", xc_potential)
