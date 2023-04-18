import numpy as np
import time

import torch
import torch.nn.functional as F

from load_data import load_data


class CnnModel(torch.nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conv1 = torch.nn.Conv3d(1, 5, kernel_size=10)
        self.conv2 = torch.nn.Conv3d(5, 10, kernel_size=10)
        self.flatten = torch.nn.Flatten()
        self.fc1 = torch.nn.Linear(21970, 21970)
        self.relu1 = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(21970, 21970)
        self.relu2 = torch.nn.ReLU()
        self.unflatten = torch.nn.Unflatten(1, (10, 13, 13, 13))
        self.dconv1 = torch.nn.ConvTranspose3d(10, 5, kernel_size=10)
        self.dconv2 = torch.nn.ConvTranspose3d(5, 1, kernel_size=10)

    def forward(self, input):
        z = input
        for l in (
            self.conv1,
            self.conv2,
            self.flatten,
            self.fc1,
            self.relu1,
            self.fc2,
            self.relu2,
            self.unflatten,
            self.dconv1,
            self.dconv2,
        ):
            z = l(z)
        return z


if __name__ == "__main__":
    network = CnnModel().float()

    optimizer = torch.optim.Adam(network.parameters(), lr=1e-2)

    (
        converged_exc_density,
        feature_0,
        feature_1,
        hsmp_iter_0,
        xc_potential,
    ) = load_data([0], [5000])

    N = converged_exc_density.shape[0]

    converged_exc_density = converged_exc_density[:, np.newaxis, :, :, :]
    xc_potential = xc_potential[:, np.newaxis, :, :, :]

    converged_exc_density = torch.from_numpy(converged_exc_density).float()
    xc_potential = torch.from_numpy(xc_potential).float()

    network.train()

    batch_size = 256
    num_epochs = 10

    losses = []

    for epoch in range(num_epochs):
        print(f"Training epoch: {epoch + 1} / {num_epochs}")
        for batch_start in range(0, N, batch_size):
            start_time = time.time()

            optimizer.zero_grad()

            batch_end = batch_start + batch_size
            dens = converged_exc_density[batch_start:batch_end]
            pot = xc_potential[batch_start:batch_end]

            M = dens.shape[0]

            output = network(dens.float())

            loss = F.mse_loss(pot.float(), output)
            loss.backward()
            optimizer.step()

            losses.append(loss.item())
            print(
                f"\tbatch {batch_start}:{batch_end}/{N} with loss {losses[-1]} took {time.time() - start_time:0.4f} seconds"
            )

    np.save("../p-amedford6-0/results/losses.npy", np.array(losses))
