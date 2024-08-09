import pandas as pd
import streamlit as st

import plotly.express as px

class ArrestWarrantMapBuilder:
    """
    World map showing Arrest Warrants issued per Nationality
    """
    def __init__(self, df):
        self._df = df

    @classmethod
    def from_detailed_arrest_warrant_df(
        cls, detailed_arrest_warrant_df: pd.DataFrame
    ) -> "ArrestWarrantMapBuilder":
        df = detailed_arrest_warrant_df.drop_duplicates(subset=["id"])
        df = df[
            ["nationality_iso_a3", "nationality_name"]
        ]

        df = (
            df.groupby(["nationality_iso_a3", "nationality_name"])
            .size()
            .reset_index(name="arrest_warrants_issued_per_nationality")
        )
        return cls(df)

    def build(self):
        df = self._df
        df = df.rename(
            columns={
                "nationality_iso_a3": "Nationality Code",
                "arrest_warrants_issued_per_nationality": "Arrest Warrants",
                "nationality_name": "Nationality",
            }
        )
        fig = px.choropleth(
            df,
            locations="Nationality Code",
            color="Arrest Warrants",
            hover_name="Nationality",
            color_continuous_scale=px.colors.sequential.Rainbow,
            width=4000,
            height=400,
        )
        fig.update_layout(
            width=4000,
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.markdown("##### Arrest Warrants Issued per Nationality")
        st.plotly_chart(fig, theme=None)