# Copyright 2023 AI Singapore

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from src.report.llm import Chatbot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class GradioReport:
    """
    Helper class to generate the report in gradio
    """

    def __init__(self, csv_file: str):
        try:
            self.df = pd.read_csv(csv_file, encoding="utf-8")
        except FileNotFoundError as error:
            error.args = ("CSV file not found",)
            logger.error(error.args)
            raise
        self.temp_dir = Path("temp")
        # check if good and bad votes are present
        try:
            self.df[["good_votes", "bad_votes"]]
        except KeyError as error:
            error.args = ("good_votes and bad_votes columns not found in CSV",)
            logger.error(error.args)
            raise

        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.chatbot = Chatbot()
        self.correlations = None

    def plot_good_bad_votes(self):
        plt.figure(figsize=(8, 6))
        self.df[["prompt", "good_votes", "bad_votes"]].plot(
            x="prompt", kind="bar", stacked=False
        )
        plt.title("Bar Plot of Good Votes and Bad Votes")
        plt.ylabel("Counts")
        plt.tight_layout()
        plt.savefig(self.temp_dir / "bar_plot.png")
        return self.temp_dir / "bar_plot.png"

    def good_bad_votes_evaluation(self):
        data = (
            self.df[["prompt", "good_votes", "bad_votes"]]
            .sort_values(by="good_votes", ascending=False)
            .to_dict("records")
        )
        output = self.chatbot.review_data(data=f"plot of good and bad votes: {data}")
        return output

    def plot_correlation(self):
        # Correlation plot for float columns against 'goal_rating'
        float_cols = self.df.select_dtypes(include="float64").columns.tolist()
        float_cols.remove("goal_rating")  # Remove 'goal_rating' from list
        # TODO: This is just temporary, find a better way to manage the files
        self.correlations = self.df[float_cols].apply(
            lambda x: x.corr(self.df["goal_rating"])
        )
        correlations = self.correlations
        cmap = plt.get_cmap("RdBu")
        colors = [
            cmap(
                (value - correlations.min()) / (correlations.max() - correlations.min())
            )
            for value in correlations
        ]
        plt.figure(figsize=(8, 6))
        correlations.plot(kind="bar", color=colors)
        plt.title("Correlation with Goal Rating")
        plt.ylabel("Correlation Coefficient")
        plt.tight_layout()
        plt.savefig(self.temp_dir / "corr_plot.png")
        return self.temp_dir / "corr_plot.png"

    def correlation_evaluation(self):
        data = self.correlations.to_dict()
        output = self.chatbot.review_data(
            data=f"coorelation plot of good ratings against other values: {data}"
        )
        return output
