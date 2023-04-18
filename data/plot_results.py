import numpy as np
import matplotlib.pyplot as plt


def main():
    results = np.load("results/losses.npy")
    N = len(results)

    results_means = []
    results_stds = []

    num_data = 4983
    batch_size = 256

    num_batches = num_data / batch_size
    if num_batches % 1 != 0:
        num_batches += 1
    num_batches = int(num_batches)

    for i in range(0, N, num_batches):
        results_means.append(np.mean(results[i : i + num_batches]))

    # results_means = results_means[4:]
    # results_stds = results_stds[4:]

    xs = range(len(results_means))
    ys = results_means

    plt.title("MSE Loss vs Epoch Learning Curve")

    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.yscale("log")
    plt.plot(xs, ys)

    plt.show()


if __name__ == "__main__":
    main()
