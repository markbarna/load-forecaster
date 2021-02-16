from optuna.trial import Trial
from statsmodels.tsa.statespace.mlemodel import MLEModel
from typing import Iterable, ClassVar


class Objective:

    def __init__(self, model_class: ClassVar[MLEModel], x: Iterable, **kwargs):
        """

        :param model_class:
        :param x:
        :param kwargs:
        """
        self.model = model_class
        self.x = x
        self._kwargs = kwargs

    def minimize(self, trial: Trial):
        """

        :param trial:
        :return:
        """
        # TODO: get model params

        # fit model with assigned params
        p_order = trial.suggest_int('p_order', 1, 5)
        d_order = trial.suggest_int('d_order', 1, 5)
        q_order = trial.suggest_int('q_order', 1, 5)
        fitted = self.model(self.x, order=(p_order, d_order, q_order)).fit()

        # return BIC
        return fitted.bic
