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

import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.report.app import GradioReport


def plot_data(csv_file):
    # Load the CSV
    report = GradioReport(csv_file.name)

    # Generate the plots
    good_bad_loc = report.plot_good_bad_votes()
    bar_plot_description = report.good_bad_votes_evaluation()
    corr_plot_loc = report.plot_correlation()
    corr_plot_description = report.correlation_evaluation()

    return good_bad_loc, bar_plot_description, corr_plot_loc, corr_plot_description


def process_csv(csv_file):
    df = pd.read_csv(csv_file.name)
    df["Prompts"] = "This would be the prompt"
    return df[["prompt", "Prompts"]], *plot_data(csv_file)
