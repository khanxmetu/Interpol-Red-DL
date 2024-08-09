import streamlit as st
import pandas as pd


class ArrestWarrantTimePlotBuilder:
    @classmethod
    def from_detailed_arrrest_warrant_dataframe(cls, df: pd.DataFrame) -> "ArrestWarrantTimePlotBuilder":
        df = df[["id", "notice_id"]].drop_duplicates()
        df["year"] = df["notice_id"].str[:4].astype(int)
        df["year"] = pd.to_datetime(df["year"], format="%Y")
        df = df[["year", "id"]]
        df_grouped = df.groupby("year").size()
        return cls(df_grouped)

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def build(self):
        st.markdown("##### Arrest Warrants Issued per Year")
        st.line_chart(self._df, x_label="Year", y_label="Arrest Warrants")
