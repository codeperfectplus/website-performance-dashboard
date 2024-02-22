# website-performance-dashboard
website performance dashboard on google search console data

# Features 

1. Rich Dashboard with multiple charts to visualize the website performance data, Google search console data is used to create the dashboard.
2. Upload the data directly to the app and see the dashboard.
3. The app is built using Plotly and Dash, which makes it interactive and responsive.
4. The app is built using Flask, which makes it easy to deploy and scale.

## How to Install/Run 

### For Anaconda Users

1. Create a new environment from the `environment.yml` file.

```bash
conda env create -f environment.yml
```

2. Activate the environment.

```bash
conda activate website-dashboard
```

3. Run the App.

```bash
python app.py
```

4. Open the browser and go to `http://localhost:8080/` to see the app.


### For Pip Users

1. Install the required packages.

```bash
pip install -r requirements.txt
```

2. Run the App.

```bash

python app.py
```

3. Open the browser and go to `http://localhost:8080/` to see the app.


### For Docker Users

---pending---

## How to Use

1. Download the data from Google Search Console in the `csv` or `zip` format.
2. Upload the data the data directly to the app.
3. The app will process the data and show the dashboard.
4. You can reupload the data to see the updated dashboard.

## How to Contribute

1. Fork the repository.
2. Clone the repository to your local machine.
3. Create a new meaningful branch.
4. Make your changes and commit them.
5. Push the changes to your fork.
6. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Deepak Raj

## Acknowledgements

- [Google Search Console](https://search.google.com/search-console/about)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/)
- [Dash](https://dash.plotly.com/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)


