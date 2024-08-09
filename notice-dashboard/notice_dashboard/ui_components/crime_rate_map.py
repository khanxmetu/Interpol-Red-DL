import streamlit as st
import pandas as pd
import plotly.express as px


class CrimeRateMapBuilder:
    def __init__(self, df: pd.DataFrame):
        self._df = df

    @classmethod
    def from_detailed_arrest_warrant_df(
        cls, detailed_arrest_warrant_df: pd.DataFrame, population_df: pd.DataFrame
    ) -> "CrimeRateMapBuilder":
        df = detailed_arrest_warrant_df.drop_duplicates(subset=["id"])
        df = df[["issuing_country_iso_a3", "issuing_country_name"]]
        df = (
            df.groupby(["issuing_country_iso_a3", "issuing_country_name"])
            .size()
            .reset_index(name="arrest_warrants_issued_by_country")
        )
        merged = pd.merge(
            df, population_df, left_on="issuing_country_iso_a3", right_on="iso_a3"
        )
        merged["crime_rate"] = (
            merged["arrest_warrants_issued_by_country"] / merged["population"] * 100_000
        )
        return cls(merged)

    def build(self):
        df = self._df
        df = df.rename(
            columns={
                "issuing_country_iso_a3": "Country Code",
                "arrest_warrants_issued_by_country": "Arrest Warrants",
                "issuing_country_name": "Country",
                "crime_rate": "Crime Rate"
            }
        )
        fig = px.choropleth(
            df,
            locations="Country Code",
            color="Crime Rate",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Rainbow,
            width=4000,
            height=400,
        )
        fig.update_layout(
            width=4000,
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.markdown("##### Crime Rate (per 100K)", help="(Arrest Warrants issued by Country / Population) * 100K")
        st.plotly_chart(fig, theme=None)
