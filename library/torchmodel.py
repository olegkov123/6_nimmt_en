import torch
import torch.nn as nn
import torch.nn.functional as F

class CustomModel(nn.Module):
    def __init__(self):
        super(CustomModel, self).__init__()

        # Dense layers for 5 input slices
        self.dense_layers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(105, 64),
                nn.ReLU(),
                nn.LayerNorm(64),
                nn.Linear(64, 64),
                nn.ReLU(),
                nn.LayerNorm(64)
            ) for _ in range(5)
        ])

        # Dense layers after concatenation
        self.dense4_1 = nn.Sequential(nn.Linear(320, 64), nn.ReLU(), nn.LayerNorm(64))
        self.dense4_2 = nn.Sequential(nn.Linear(64, 64), nn.ReLU(), nn.LayerNorm(64))
        self.dense4_3 = nn.Sequential(nn.Linear(64, 64), nn.ReLU(), nn.LayerNorm(64))

        # Added two new hidden layers
        self.dense4_4 = nn.Sequential(nn.Linear(64, 64), nn.ReLU(), nn.LayerNorm(64))
        self.dense4_5 = nn.Sequential(nn.Linear(64, 64), nn.ReLU(), nn.LayerNorm(64))

        # Final output layer
        self.output = nn.Linear(64, 105)

    def forward(self, inputs, mask):
        # Processing input data through dense layers
        processed_inputs = [dense_layer(inputs[:, i]) for i, dense_layer in enumerate(self.dense_layers)]

        # Concatenation of processed inputs
        concat = torch.cat(processed_inputs, dim=1)

        # Passing through additional dense layers
        dense4 = self.dense4_5(self.dense4_4(self.dense4_3(self.dense4_2(self.dense4_1(concat)))))

        # Output layer and activation function
        out = self.output(dense4)
        out = F.softmax(out, dim=1)

        # Applying the mask to the output
        output_masked = out * mask
        return output_masked

    def predict(self, input_data, mask):
        # Prediction for input data
        input_tensor = torch.tensor(input_data).float()
        mask_tensor = torch.tensor(mask).float()
        self.eval()
        with torch.no_grad():
            predictions = self(input_tensor, mask_tensor)
        return predictions.cpu().numpy()

    def predict_prod(self, input_data, mask):
        # Predict class for input data
        input_tensor = torch.tensor(input_data).float()
        mask_tensor = torch.tensor(mask).float()
        self.eval()
        with torch.no_grad():
            predictions = self(input_tensor, mask_tensor)

        # Get class index for each sample in the batch
        predicted_class_indices = torch.argmax(predictions, dim=1).cpu().numpy()
        return predicted_class_indices

    def train_on_batch(self, input_data, mask, target_data):
        # Train on one batch of data
        input_tensor = torch.tensor(input_data).float()
        mask_tensor = torch.tensor(mask).float()

        # Convert target_data to class indices and ensure proper shape for CrossEntropyLoss
        target_indices = torch.argmax(torch.tensor(target_data), dim=1).long()

        self.train()
        self.optimizer.zero_grad()
        outputs = self(input_tensor, mask_tensor)

        loss = self.criterion(outputs, target_indices)
        loss.backward()
        self.optimizer.step()

        _, predicted = torch.max(outputs.data, 1)
        total = target_indices.size(0)
        correct = (predicted == target_indices).sum().item()

        # Calculate accuracy
        accuracy = 100 * correct / total

        return loss.item(), accuracy
