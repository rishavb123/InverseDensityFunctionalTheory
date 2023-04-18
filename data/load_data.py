import numpy as np


def load_data(ind_s_arr, ind_e_arr):
    converged_exc_density_full = []
    feature_0_full = []
    feature_1_full = []
    hsmp_iter_0_full = []
    xc_potential_full = []

    shp = (-1, 31, 31, 31)

    for ind_s, ind_e in zip(ind_s_arr, ind_e_arr):
        converged_exc_density = np.load(f"../p-amedford6-0/dataset/converged_exc_density_{ind_s}_{ind_e}.npy")
        feature_0 = np.load(f"../p-amedford6-0/dataset/feature_0_{ind_s}_{ind_e}.npy")
        feature_1 = np.load(f"../p-amedford6-0/dataset/feature_1_{ind_s}_{ind_e}.npy")
        hsmp_iter_0 = np.load(f"../p-amedford6-0/dataset/hsmp_iter_0_{ind_s}_{ind_e}.npy")
        xc_potential = np.load(f"../p-amedford6-0/dataset/xc_potential_{ind_s}_{ind_e}.npy")

        converged_exc_density_full.append(converged_exc_density.reshape(shp))
        feature_0_full.append(feature_0.reshape(shp))
        feature_1_full.append(feature_1.reshape(shp))
        hsmp_iter_0_full.append(hsmp_iter_0.reshape(shp))
        xc_potential_full.append(xc_potential.reshape(shp))

    return tuple(
        np.vstack(f)
        for f in (
            converged_exc_density_full,
            feature_0_full,
            feature_1_full,
            hsmp_iter_0_full,
            xc_potential_full,
        )
    )


if __name__ == "__main__":
    import time

    start_time = time.time()

    (
        converged_exc_density,
        feature_0,
        feature_1,
        hsmp_iter_0,
        xc_potential,
    ) = load_data([0], [5000])

    print(converged_exc_density.shape)

    print(f"Took {time.time() - start_time:0.4f} seconds")
