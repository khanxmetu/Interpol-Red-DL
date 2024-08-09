import streamlit as st
from utils import millify


class NoticeCountBuilder:
    def __init__(self, count: int, millified=True):
        self._count = count
        self._millified = millified

    def build(self):
        st.metric("Notices", millify(self._count, precision=2))


class ArrestWarrantCountBuilder:
    def __init__(self, count: int, millified=True):
        self._count = count
        self._millified = millified

    def build(self):
        st.metric("Arrest Warrants", millify(self._count, precision=2))


class ClassifiedArrestWarrantCountBuilder:
    def __init__(self, count: int, millified=True):
        self._count = count
        self._millified = millified

    def build(self):
        st.metric("Classified Arrest Warrants", millify(self._count, precision=2))
