# Long/Short Trade Prediction 📈

This project demonstrates a simple Streamlit app that predicts long and short trades based on historical minute-level stock data. The app utilizes a slider to adjust thresholds and percentages to simulate trade decisions and visualize them on a plot.

## Requirements

- Python 3.x
- Streamlit
- Pandas
- Matplotlib

To install the required packages, use the following command:

```bash
pip install streamlit pandas matplotlib
```

## Usage

1. **Prepare Data**: Ensure you have a CSV file named `PAYTM_minute.csv` in a `data` directory. The file should have at least two columns: `date` and `close`. The `date` column should contain datetime values, and the `close` column should contain closing prices.

2. **Run the App**: Execute the Streamlit app with the following command:

   ```bash
   streamlit run app.py
   ```

3. **Adjust Parameters**: Use the sliders in the app to select the threshold and percentage values. The app will then compute potential long and short trades based on these parameters.

4. **View Results**: The app displays the predicted trades and visualizes them on a graph showing closing prices over time. The graph highlights the trade points and provides annotations with the trade prices.

## Code Explanation

1. **Import Libraries**: Import necessary libraries including Pandas for data manipulation, Streamlit for the web interface, and Matplotlib for plotting.

2. **Read Data**: Load the CSV data into a Pandas DataFrame and convert the `date` column to datetime format.

3. **Parameter Configuration**: Use Streamlit sliders to select threshold values and percentage changes for long and short trade decisions.

4. **Trade Calculation**: Compute potential long and short trades based on the selected parameters. The app determines trade times and displays relevant messages.

5. **Plot Visualization**: Create a plot of closing prices over time, highlighting trade points with annotations.

## Example

Here's an example of how the app will look and function:

- **Slider for Threshold**: Adjust this to set the initial threshold for long/short trade decisions.
- **Slider for Percentage**: Adjust this to set the percentage change for the second threshold.
- **Trade Results**: The app will display messages indicating trade points and visualize them on a graph.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


