from flask import Flask, request, render_template, jsonify
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

from src.logger import logging


application = Flask(__name__)

app = application


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])  # form submit process...
def predict_datapoint():
    if request.method == 'GET':
        return render_template('form.html')

    else:
        data = CustomData(
            Delivery_person_Age=float(request.form.get('Delivery_person_Age')),
            Delivery_person_Ratings = float(request.form.get('Delivery_person_Ratings')),
            Vehicle_condition= float(request.form.get('Vehicle_condition')),
            multiple_deliveries = float(request.form.get('multiple_deliveries')),
            Restaurant_latitude = float(request.form.get('Restaurant_latitude')),
            Restaurant_longitude= float(request.form.get('Restaurant_longitude')),
            Delivery_location_latitude= float(request.form.get('Delivery_location_latitude')),
            Delivery_location_longitude= float(request.form.get('Delivery_location_longitude')),
            Weather_conditions = request.form.get('Weather_conditions'),
            Road_traffic_density= request.form.get('Road_traffic_density'),
            City = request.form.get('City'),
            Festival = request.form.get('Festival'),
            Type_of_vehicle = request.form.get('Type_of_vehicle'),
            Type_of_order = request.form.get('Type_of_order')
        )

        final_new_data = data.get_data_as_dataframe()

        logging.info(
            f"final new data - {type(final_new_data)} and value-{final_new_data}")

        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_new_data)

        results = round(pred[0], 2)

        return render_template('results.html', final_result=results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    # run at localhost... http://127.0.0.1:5000/
