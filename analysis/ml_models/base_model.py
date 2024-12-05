from abc import ABC, abstractmethod
import pandas as pd


class BaseModel(ABC):
    @abstractmethod
    def prepare_data(self, data: pd.DataFrame):
        pass

    @abstractmethod
    def predict(self, data: pd.DataFrame):
        pass

    @abstractmethod
    def train(self, data: pd.DataFrame):
        pass