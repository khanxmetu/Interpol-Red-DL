import os
import streamlit as st

import db
from models import Notice
from ui_components.notice_detail_view import (
    AdditionalInformationBuilder,
    ArrestWarrantsBuilder,
    PersonalDetailsBuilder,
    PhotosBuilder,
)
from repositories import NoticeRepository


def get_notice_by_id(notice_id: str) -> Notice:
    return NoticeRepository(db.get_db_session()).get_by_id(notice_id)


notice_id = st.session_state.pop("notice_id", None)

if not notice_id:
    st.warning("Select a notice to view its details")
    st.markdown("<a href='Notice_List' target='_self'>Go to Notice List</a>", unsafe_allow_html=True)
    st.stop()

use_downloaded_images = bool(int(os.environ["SERVE_DOWNLOADED_IMAGES"]))

notice = get_notice_by_id(notice_id)
arrest_warrants = notice.arrest_warrants
image_urls = notice.image_urls
st.title("Notice Detail")
st.subheader(f"Notice ID: {notice_id}")
PhotosBuilder(image_urls).build(use_downloaded=use_downloaded_images)
PersonalDetailsBuilder(notice).build()
ArrestWarrantsBuilder(arrest_warrants).build()
AdditionalInformationBuilder(notice).build()
