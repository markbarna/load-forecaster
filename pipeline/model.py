"""
Pipeline step to run the model training and generate diagnostic plots.
"""


from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.mlemodel import MLEModel
from typing import ClassVar
import pandas as pd
import os
import joblib
import logging
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

logger = logging.getLogger(__name__)


def plot_series(dataset: pd.DataFrame, model_save_path: str):
    """
    Plot diagnostic images of the stats model amd the time series data.
    :param dataset: expects a DataFrame with a DatetimeIndex, the first column numerical data,
        and the second column a category
    :param model_save_path: local of the model for saving the plots
    :return:
    """
    logger.info("====== Generating interesting plots of the time series =====")
    y_var = dataset.columns[0]
    hue_var = dataset.columns[-1]
    dataset['timestamp'] = dataset.index.to_timestamp()
    x_var = 'timestamp'

    # plot the time series
    sns.lineplot(
        data=dataset,
        x=x_var,
        y=y_var,
        hue=hue_var,
    )
    plt.xticks(rotation='45')
    plt.savefig(os.path.join(model_save_path, 'time_plot.png'), bbox_inches='tight')

    # plot auto-correlation and partial auto-correlation
    fig, axs = plt.subplots(dataset[hue_var].nunique(), sharex=True)
    for ax, (category, df) in zip(axs, dataset.groupby(hue_var)):
        plot_acf(df.iloc[:, 0], ax=ax, title=category)
    fig.suptitle('Auto-correlation')
    fig.savefig(os.path.join(model_save_path, 'auto_corr.png'))

    fig, axs = plt.subplots(dataset[hue_var].nunique(), sharex=True)
    for ax, (category, df) in zip(axs, dataset.groupby(hue_var)):
        plot_pacf(df.iloc[:, 0], ax=ax, title=category)
    fig.suptitle('Partial Auto-correlation')
    fig.savefig(os.path.join(model_save_path, 'part_auto_corr.png'))

    logger.info(f"====== plots saved to {model_save_path} ======")


class TimeSeriesModel:

    def __init__(self, model_class: ClassVar[MLEModel]):
        """
        Wrapper to hold a statsmodels (https://www.statsmodels.org/stable/index.html) time series model, where one model
        is fit for each level of a categorical variable.
        :param model_class: statsmodels MLEModel class object
        """
        self._m = model_class
        self.fitted_ = dict()
        self.results_ = dict()

    def fit_best_model(self, training_data: pd.DataFrame):
        """
        Find best model by fitting multiple models using search space of parameters.
        :param training_data: expects a DataFrame with a DatetimeIndex, the first column numerical data,
        and the second column a category
        :return:
        """
        # TODO: model training on parameter space
        logger.info(f"====== Fitting {self._m} model on training data ======")
        grouper = training_data.columns[1]
        for category, df in training_data.groupby(grouper):
            self.fitted_[category] = self._m(df.iloc[:, 0], order=(1,1,1))
            self.results_[category] = self.fitted_[category].fit()
            print(f'====== Results for variable {grouper}, level {category} ======')
            print(self.results_[category].summary())

    def predict(self, date: str, time: str, area: str) -> pd.Series:
        """
        Get the model's load forecast in megawatts
        :param date: date (must be later than training data), e.g. 2021-02-01
        :param time: time (HH:MM) 24-hr format
        :param area: PJM area zone
        :return: load forecast
        """
        timestamp = pd.Timestamp(f'{date} {time}:00')
        return self.results_[area].predict(timestamp)


def train_model(training_data_path: str, model_save_path: str, *args, **kwargs):
    """
    Run model training and plotting of trained models.
    :param training_data_path: path to input data. expects a parquet file with a DatetimeIndex,
        the first column numerical data,
        and the second column a category
    :param model_save_path: path to save the trained model binary
    :return:
    """
    model = TimeSeriesModel(ARIMA)
    dataset = pd.concat((pd.read_parquet(file.path)) for file in os.scandir(training_data_path)
                        if file.name.endswith('.parquet'))
    # convert index to a period index
    dataset = dataset.to_period(freq='600s')
    plot_series(dataset, model_save_path)
    model.fit_best_model(dataset)
    joblib.dump(model, os.path.join(model_save_path, 'model.gz'))

    # save diagnostic plots
    for category, results in model.results_.items():
        fig = plt.figure(figsize=(16, 9))
        fig = results.plot_diagnostics(fig=fig, lags=30)
        fig.savefig(os.path.join(model_save_path, f'{category}_diagnostic.png'))

    logger.info(f"====== Fitted model saved to {model_save_path} ======")
