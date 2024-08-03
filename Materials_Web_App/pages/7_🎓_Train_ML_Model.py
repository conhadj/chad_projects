import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.tree import export_graphviz
from io import StringIO
import pydotplus
from PIL import Image
import tempfile
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from utils.streamlit_style import hide_streamlit_style

st.set_page_config(
    page_title="Train ML Models",
    page_icon="pictures/favicon.ico",
)

def plot_metrics(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot loss
    ax1.plot(history.history['loss'], label='Train Loss')
    ax1.plot(history.history['val_loss'], label='Validation Loss')
    ax1.set_title('Loss over Epochs')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.legend()
    
    # Plot accuracy
    ax2.plot(history.history['accuracy'], label='Train Accuracy')
    ax2.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax2.set_title('Accuracy over Epochs')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    
    st.pyplot(fig)

def plot_confusion_matrix(cm):
    fig_cm, ax_cm = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=[0, 1], yticklabels=[0, 1])
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    st.pyplot(fig_cm)

def display_nn_info(model):
    st.write("### Neural Network Model Information")
    for layer in model.layers:
        st.write(f"Layer: {layer.name}, Type: {layer.__class__.__name__}, Activation: {layer.activation.__name__}")
    st.write(f"Total Parameters: {model.count_params()}")

def create_model(input_dim):
    model = Sequential([
        Dense(64, input_dim=input_dim, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model

def plot_decision_tree(model, feature_names):
    # Select the first tree
    tree = model.estimators_[0]
    dot_data = StringIO()
    export_graphviz(tree, out_file=dot_data, feature_names=feature_names, filled=True, rounded=True, special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_file_path = f"{tmpdirname}/temp_tree.png"
        graph.write_png(temp_file_path)
        image = Image.open(temp_file_path)
        st.image(image, caption='Decision Tree from Random Forest')

def plot_svm_support_vectors(model, X_train, y_train):
    fig, ax = plt.subplots()
    X0, X1 = X_train[:, 0], X_train[:, 1]
    xx, yy = np.meshgrid(np.linspace(X0.min(), X0.max(), 500), np.linspace(X1.min(), X1.max(), 500))
    Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    ax.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.PuBu)
    ax.contour(xx, yy, Z, levels=[0], linewidths=2, colors='darkred')
    ax.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1], s=100, facecolors='none', edgecolors='k')
    ax.scatter(X0, X1, c=y_train, cmap=plt.cm.PuBu_r, edgecolors='k')

    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('SVM Support Vectors')
    st.pyplot(fig)

def train_model():
    # Hide Streamlit style components
    hide_streamlit_style()

    if 'df' not in st.session_state:
        st.warning("No data available. Please go to the 'Main Page' to load the data.")
        return

    df = st.session_state['df']

    st.write("## 🎓 Train Machine Learning Models")

    # Check if 'rating' and 'Su/Sy' columns exist
    feature_columns = ["Su", "Sy", "E", "G", "mu", "Ro"]
    if 'rating' in df.columns:
        feature_columns.append('rating')
    if 'Su/Sy' in df.columns:
        feature_columns.append('Su/Sy')

    # User inputs
    st.sidebar.header("Select Features and Parameters:")
    features = st.sidebar.multiselect(
        "Select Features:",
        options=feature_columns,
        default=feature_columns
    )
    
    model_choice = st.sidebar.selectbox(
        "Select Model:",
        options=["Random Forest", "Logistic Regression", "Support Vector Machine", "Neural Network"]
    )
    
    train_size = st.sidebar.slider(
        "Train-Test Split Ratio (Train %):",
        min_value=60,
        max_value=100,
        value=80,
        step=1
    )
    test_size = 100 - train_size
    
    k_fold = st.sidebar.slider(
        "Select K for K-fold Cross Validation:",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )

    epochs = 10
    if model_choice == "Neural Network":
        epochs = st.sidebar.slider(
            "Select Number of Epochs:",
            min_value=10,
            max_value=100,
            value=20,
            step=10
        )

    if st.button('Train Model'):
        X = df[features]
        y = df['Use']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size/100, random_state=42)

        # Initialize the model
        if model_choice == "Random Forest":
            model = RandomForestClassifier()
        elif model_choice == "Logistic Regression":
            model = LogisticRegression()
        elif model_choice == "Support Vector Machine":
            model = SVC(kernel='linear')
        elif model_choice == "Neural Network":
            model = create_model(input_dim=len(features))
            history = model.fit(X_train, y_train, epochs=epochs, validation_split=0.2, verbose=0)

        # Train the model (for non-neural network models)
        if model_choice != "Neural Network":
            model.fit(X_train, y_train)
        
        # Predict and evaluate
        y_pred = model.predict(X_test)
        if model_choice == "Neural Network":
            y_pred = (y_pred > 0.5).astype("int32")
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        st.write(f"### Model: {model_choice}")
        st.write(f"#### Train-Test Split: {train_size}% - {test_size}%")
        st.write(f"#### K-fold Cross Validation: {k_fold}")

        st.write("### Performance Metrics:")
        st.write(f"**Accuracy:** {accuracy:.2f}")
        st.write(f"**Precision:** {precision:.2f}")
        st.write(f"**Recall:** {recall:.2f}")
        st.write(f"**F1 Score:** {f1:.2f}")

        # K-fold cross-validation for all models
        if k_fold > 1:
            kf = KFold(n_splits=k_fold)
            fold_accuracies = []
            for train_index, val_index in kf.split(X):
                X_train_fold, X_val_fold = X.iloc[train_index], X.iloc[val_index]
                y_train_fold, y_val_fold = y.iloc[train_index], y.iloc[val_index]
                if model_choice == "Neural Network":
                    model = create_model(input_dim=len(features))
                    history = model.fit(X_train_fold, y_train_fold, epochs=epochs, validation_split=0.2, verbose=0)
                    val_accuracy = model.evaluate(X_val_fold, y_val_fold, verbose=0)[1]
                else:
                    model.fit(X_train_fold, y_train_fold)
                    y_val_pred = model.predict(X_val_fold)
                    val_accuracy = accuracy_score(y_val_fold, y_val_pred)
                fold_accuracies.append(val_accuracy)
            st.write(f"### K-fold Cross-Validation Scores (K={k_fold}):")
            st.write(fold_accuracies)
            st.write(f"**Mean CV Accuracy:** {np.mean(fold_accuracies):.2f}")
            st.write(f"**Standard Deviation of CV Accuracy:** {np.std(fold_accuracies):.2f}")

        # Loss and Accuracy plots (for neural network)
        if model_choice == "Neural Network":
            plot_metrics(history)
            display_nn_info(model)

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        plot_confusion_matrix(cm)

        # Plot decision tree for Random Forest
        if model_choice == "Random Forest":
            plot_decision_tree(model, features)

        # Plot SVM support vectors
        if model_choice == "Support Vector Machine":
            if len(features) == 2:
                plot_svm_support_vectors(model, X_train.to_numpy(), y_train.to_numpy())
            else:
                st.warning("SVM support vector plot requires exactly 2 features.")

if __name__ == "__main__":
    train_model()
