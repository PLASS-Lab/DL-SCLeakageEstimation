import numpy as np
import pandas as pd
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GRU, Dense, Input, Embedding, Flatten, Concatenate, Layer
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import tensorflow.keras.backend as K
from tensorflow import keras
import time

data = pd.read_csv('')  
data = data[['Instr', 'signedD']]

def create_context_embedding(data):
    # Shift the 'Instr' column to get the previous and next instructions
    for i in range(1, 6):
        data[f'Prev{i}_Instr'] = data['Instr'].shift(i)
        data[f'Next{i}_Instr'] = data['Instr'].shift(-i)

    # Create context
    context_cols = [f'Prev{i}_Instr' for i in range(5, 0, -1)] + ['Instr'] + [f'Next{i}_Instr' for i in range(1, 6)]
    data['Eleven_instr'] = data[context_cols].fillna('').agg(' '.join, axis=1)

    data = data.dropna(subset=[f'Prev{i}_Instr' for i in range(1, 6)] + [f'Next{i}_Instr' for i in range(1, 6)])
    return data

# Apply the modified context function
data_with_context = create_context_embedding(data).copy()

label_encoder_instr = LabelEncoder()
label_encoder_elevengram = LabelEncoder()

# Fit label encoder and transform columns
data_with_context['Instr_encoded'] = label_encoder_instr.fit_transform(data_with_context['Instr'])
data_with_context['Eleven_instr_encoded'] = label_encoder_elevengram.fit_transform(data_with_context['Eleven_instr'])

# Select features and target
X = data_with_context[['Instr_encoded', 'Eleven_instr_encoded']]
y = data_with_context['signedD']
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Reshape input to be [samples, time steps, features] which is required for GRU
X_train_scaled = X_train_scaled.reshape((X_train_scaled.shape[0], 1, X_train_scaled.shape[1]))
X_test_scaled = X_test_scaled.reshape((X_test_scaled.shape[0], 1, X_test_scaled.shape[1]))

# Attention Layer
@keras.utils.register_keras_serializable()
class AttentionLayer(Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name='attention_weight', shape=(input_shape[-1], 1),
                                 initializer='random_normal', trainable=True)
        self.b = self.add_weight(name='attention_bias', shape=(input_shape[1], 1),
                                 initializer='zeros', trainable=True)
        super(AttentionLayer, self).build(input_shape)

    def call(self, inputs):
        e = K.tanh(K.dot(inputs, self.W) + self.b)
        e = K.squeeze(e, axis=-1)
        alpha = K.softmax(e)
        alpha = K.expand_dims(alpha, axis=-1)
        output = inputs * alpha
        return K.sum(output, axis=1)

# Model with embedding for n-gram features and attention mechanism
input_layer = Input(shape=(1, X_train_scaled.shape[2]))

# Embedding layer for the eleven-gram
eleven_instr_input = Input(shape=(1,))
eleven_instr_embedding = Embedding(input_dim=len(data_with_context['Eleven_instr_encoded'].unique()), output_dim=50)(eleven_instr_input)
eleven_instr_embedding = Flatten()(eleven_instr_embedding)

# GRU layers
gru_out = GRU(256, return_sequences=True)(input_layer)
gru_out = GRU(128, return_sequences=True)(gru_out)
gru_out = GRU(64, return_sequences=True)(gru_out)
gru_out = GRU(32, return_sequences=True)(gru_out) 

# Attention layer
attention_out = AttentionLayer()(gru_out)

# Concatenate with embedding output
concat_out = Concatenate()([attention_out, eleven_instr_embedding])

# Output layer
output = Dense(1)(concat_out)

# Create the model
model = Model(inputs=[input_layer, eleven_instr_input], outputs=output)

learning_rate = 0.001  # Adjust learning rate as needed
adam_optimizer = Adam(learning_rate=learning_rate, clipvalue=1)

# Compile the model with the Adam optimizer
model.compile(optimizer=adam_optimizer, loss='mse')
model.summary()

# Early stopping to monitor the validation loss
early_stopping = EarlyStopping(monitor='val_loss', patience=50, restore_best_weights=True)

train_start_time = time.time()  # Start the timer
# Train the model
history = model.fit([X_train_scaled, X_train['Eleven_instr_encoded']], y_train, epochs=50, batch_size=512, validation_split=0.1, callbacks=[early_stopping], verbose=1)
train_end_time = time.time()  # End the timer
training_time = train_end_time - train_start_time  # Calculate training time
print(f"Training time: {training_time:.4f} seconds")
#model.save('model.keras')

test_start_time = time.time()  # Start the timer
# Predict on test data
y_pred = model.predict([X_test_scaled, X_test['Eleven_instr_encoded']]).flatten()
test_end_time = time.time()  # End the timer
testing_time = test_end_time - test_start_time  # Calculate testing time

print(f"Testing time: {testing_time:.4f} seconds")

y_pred1 = np.round(y_pred).astype(int)

# Evaluate the model with R-squared score
r2_rounded = r2_score(y_test, y_pred1)
print(f"R-squared score rounded: {r2_rounded}")

# Calculate Mean Squared Errors
mse_rounded = mean_squared_error(y_test, y_pred1)
print(f"Mean Squared Error rounded predictions: {mse_rounded}")


# Create a DataFrame with the original instructions, true values, predicted values
results_df = pd.DataFrame({
    'Instr': X_test.index.map(data_with_context['Instr']),
    'True_signedD': y_test,
    'Predicted_signedD_rounded': y_pred1
})

# Save training and validation loss history to a CSV file
loss_history_df = pd.DataFrame({
    'Epoch': range(1, len(history.history['loss']) + 1),
    'Train_Loss': history.history['loss'],
    'Validation_Loss': history.history['val_loss']
})

# Save the DataFrame to a CSV file
loss_history_df.to_csv('loss.csv', index=False)

# Optionally print the first few rows to confirm
print(loss_history_df.head())

# Save the DataFrame to a CSV file

results_df.to_csv('results.csv', index=False)

