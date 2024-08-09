import pandas as pd
import plotly.express as px
import streamlit as st


class OffenseTypesPieChartBuilder:
    @classmethod
    def from__detailed_arrrest_warrant_dataframe(
        cls, detailed_df: pd.DataFrame
    ) -> "OffenseTypesPieChartBuilder":
        df = detailed_df.drop_duplicates(subset=["id"])
        df = (
            df[["offense_type"]]
            .groupby("offense_type", dropna=False)
            .size()
            .reset_index(name="frequency")
        )

        return cls(df)

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def build(self):
        df = self._df
        # df.loc[df["frequency"] < 5, "offense_type"] = (
        #     "Other offenses"
        # )
        df = df.fillna("Unclassified")

        df = df.rename(columns={
            "frequency": "Frequency",
            "offense_type": "Offense Type"
        })
        fig = px.pie(
            df, values="Frequency", names="Offense Type", title="Classification of Arrest Warrants by Offense Types"
        )
        st.plotly_chart(fig)
