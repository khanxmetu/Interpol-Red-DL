import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from db import get_db_session
from ui_components.crime_rate_map import CrimeRateMapBuilder
from ui_components.offense_types_piechart import OffenseTypesPieChartBuilder
from ui_components.arrest_warrant_timeplot import ArrestWarrantTimePlotBuilder
from ui_components.metrics import (
    ArrestWarrantCountBuilder,
    ClassifiedArrestWarrantCountBuilder,
    NoticeCountBuilder,
)
from ui_components.arrest_warrant_map import ArrestWarrantMapBuilder
from repositories import ArrestWarrantRepository, NoticeRepository


def get_arrest_warrant_count() -> int:
    arrest_warrant_repo = ArrestWarrantRepository(get_db_session())
    return arrest_warrant_repo.get_count()


def get_notice_count() -> int:
    notice_repo = NoticeRepository(get_db_session())
    return notice_repo.get_count()


def get_offense_classified_count() -> int:
    arrest_warrant_repo = ArrestWarrantRepository(get_db_session())
    return arrest_warrant_repo.get_classified_count()


def get_detailed_arrest_warrant_df() -> pd.DataFrame:
    arrest_warrant_repo = ArrestWarrantRepository(get_db_session())
    return arrest_warrant_repo.get_detailed_arrest_warrants_as_dataframe()

def get_population_df() -> pd.DataFrame:
    df = pd.read_csv("external-data/2024_population.csv")
    df = df.rename(columns={
        "iso_code": "iso_a3",
    })
    # Using 2023's population since some values are missing in 2024's column
    df["population"] = df["2023_population"].str.replace(',', '').astype(int)
    return df[["iso_a3", "population"]]

detailed_arrest_warrants_df = get_detailed_arrest_warrant_df()

st.set_page_config(
    page_title="Notice Dashboard", layout="wide", initial_sidebar_state="expanded"
)
cols = st.columns(2)
with cols[0]:
    st.subheader("Interpol Red DL")
    st.title("Notice Dashboard")
with cols[1]:
    if st.toggle("Auto Refresh", value=True):
        st_autorefresh(interval=2000)

with st.container(border=True):
    cols = st.columns(3)
    with cols[0]:
        NoticeCountBuilder(get_notice_count()).build()
    with cols[1]:
        ArrestWarrantCountBuilder(get_arrest_warrant_count()).build()
    with cols[2]:
        ClassifiedArrestWarrantCountBuilder(get_offense_classified_count()).build()

ArrestWarrantMapBuilder.from_detailed_arrest_warrant_df(
    detailed_arrest_warrants_df
).build()

CrimeRateMapBuilder.from_detailed_arrest_warrant_df(
detailed_arrest_warrants_df, get_population_df()
).build()

cols = st.columns(2, vertical_alignment="bottom")
with cols[0]:
    ArrestWarrantTimePlotBuilder.from_detailed_arrrest_warrant_dataframe(
        detailed_arrest_warrants_df
    ).build()
with cols[1]:
    OffenseTypesPieChartBuilder.from__detailed_arrrest_warrant_dataframe(
        detailed_arrest_warrants_df,
    ).build()
