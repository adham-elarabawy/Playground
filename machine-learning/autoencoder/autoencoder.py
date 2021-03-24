import os
#Disable the warnings for now cuz they are annoying
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from torchvision.datasets import MNIST
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from util import masking_noise
import click

# Parameters
learning_rate = 0.01
training_epochs = 10
batch_size = 64



class Model(nn.Module):
    # Network Parameters
    self.n_hidden_1 = 256 # 1st layer num features
    self.n_hidden_2 = 128 # 2nd layer num features
    self.n_input = 784 # MNIST data input (img shape: 28*28) NOTE: no 3rd dimension b/c B&W
    def __init__(self):
        super(Model, self).__init__()
        self.encoder = nn.Sequential(
                        nn.Linear(in_features=self.n_input, out_features=self.n_hidden_1),
                        nn.Sigmoid(),
                        nn.Linear(in_features=self.n_hidden_1, out_features=self.n_hidden_2),
                        nn.Sigmoid())



        self.decoder = nn.Sequential(
                        nn.Linear(in_features=self.n_hidden_2, out_features=self.n_hidden_1),
                        nn.Sigmoid(),
                        nn.Linear(in_features=self.n_hidden_1, out_features=self.n_input),
                        nn.Sigmoid())

    def forward(self, input):
        encoded_input = self.encoder(input)
        out = self.decoder(encoded_input)
        return out

@click.command()
# training parameters
@click.option('--epochs', default=10, help='Number of training epochs')
@click.option('--rate', default=10, help='Learning rate')
@click.option('--batch', default=64, help='Batch size')
# general usage parameters
@click.option('--train', default="", help='Path to where trained model should be saved. If this argument is left blank, this runs in inference mode (requires a pretrained model to be loaded).')
@click.option('--weights', type=click.File('rb'), help='Pre-trained model file')
@click.option('--img', type=click.File('rb'), help='Input to apply autoencoder on')



def main(epochs, rate, batch, train, weights, img):
    if train:
        try:
            open(train, 'w')
        except OSError:
            print('Unable to create weights file at the given train path.')
            exit()

        model = Model()
        print(model)
        criterion = nn.BCELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        MNIST_data = MNIST("../data/mnist", train=True, download=True, transform = transforms.ToTensor())
        train_dataloader = DataLoader(MNIST_data, batch_size=batch_size)
        for epoch in range(training_epochs):
            for data in train_dataloader:
                img, _ = data
                img_noise = masking_noise(img, 0.5)

                optimizer.zero_grad()
                outputs = model(img_noise)
                loss = criterion(outputs, img)
                loss.backward()
                optimizer.step()
            print('Epoch {} of {}, Train Loss: {:.3f}'.format(epoch+1, training_epochs, loss))
        torch.save(model.state_dict(), train)
    else:
        try:
            open(model, 'w')
        except OSError:
            print('Unable to create weights file at the given train path.')
            exit()

        model = Model()
        model.load_state_dict(torch.load(weights))

        pred_img = model(img)

        # TODO: Write output image post-autoencoder
        # TODO: Save latent space representation


if __name__ == '__main__':
    main()
