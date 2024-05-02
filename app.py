from flask import Flask, render_template, request, jsonify, send_file
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Load the dataset
dataset = pd.read_csv("penguins.csv")
columns = dataset.columns.tolist()

@app.route('/')
def index():
    return render_template('index.html', columns=columns)

@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    # Get form data
    data = request.get_json()
    x_column = data['xColumn']
    y_column = data['yColumn']
    graph_type = data['graphType']

    # Generate the graph
    plt.figure(figsize=(10, 6))  # Set figure size
    if graph_type == 'scatter':
        sns.scatterplot(data=dataset, x=x_column, y=y_column,palette='Set1')
    elif graph_type == 'bar':
        sns.barplot(data=dataset, x=x_column, y=y_column,palette="Set2")
    elif graph_type == 'line':
        sns.lineplot(data=dataset, x=x_column, y=y_column,palette="Set3")
    elif graph_type == 'countplot':
        sns.countplot(data=dataset, x=x_column, y=y_column,palette="Set1")
    elif graph_type == 'box':
        sns.boxplot(data=dataset, x=x_column, y=y_column,palette="Set2")
    elif graph_type == 'distplot':
        sns.distplot(dataset.x_column,bins=10,color='b')
        #sns.swarmplot(data=dataset, x=x_column, y=y_columnpalette="Set1")
    elif graph_type == 'pair':
        sns.pairplot(data=dataset,palette="Set2")
    elif graph_type == 'lmplot':
        sns.lmplot(data=dataset, x=x_column, y=y_column,palette="Set1")

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Clear the plot to avoid overlapping
    plt.clf()
    plt.close()

    # Return the image blob
    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
