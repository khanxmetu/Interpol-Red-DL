from typing import Optional
import streamlit as st
import pandas as pd
from sqlalchemy.sql import select
from streamlit_autorefresh import st_autorefresh

from models import Notice
from db import get_db_session
from repositories import NoticeRepository


def get_notices_minimal_data_as_dataframe() -> pd.DataFrame:
    notice_repo = NoticeRepository(get_db_session())
    return notice_repo.get_notices_minimal_data_as_dataframe()

def get_notices_count() -> int:
    notice_repo = NoticeRepository(get_db_session())
    return notice_repo.get_count()


def get_notice_id_from_selected_row() -> Optional[str]:
    notice_table = st.session_state.get("notice_table")
    df = st.session_state.get("prev_notice_list_df")
    if not notice_table: return
    rows = notice_table["selection"]["rows"]
    if not rows: return
    row = rows[0]
    notice_id = df.iloc[row].name
    st.session_state.pop("prev_notice_list_df")
    return notice_id

notice_id = get_notice_id_from_selected_row()
if notice_id:
    st.session_state["notice_id"] = notice_id
    st.switch_page("pages/Notice_Detail.py")

st.title("Notice List")
st.info("Select a notice to view its details")
df = get_notices_minimal_data_as_dataframe()
st.dataframe(
    df,
    use_container_width=True,
    selection_mode="single-row",
    on_select="rerun",
    key="notice_table",
)
st.session_state["prev_notice_list_df"] = df

st.caption(f"{get_notices_count()} notices retrieved")
