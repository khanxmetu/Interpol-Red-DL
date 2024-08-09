from typing import Optional
import streamlit as st

from models import (
    _OffenseType,
    _Country,
    _EyeColor,
    _HairColor,
    _Language,
    _OffenseType,
    _Sex,
    ArrestWarrant,
    ImageURL,
    Notice,
)
from datetime import datetime
from utils import (
    to_local_datetime,
    get_human_readable_date_time,
    get_human_readable_date,
    calculate_age,
)


class PhotosBuilder:
    def __init__(self, image_url_objects: list[ImageURL]):
        self._image_url_objects = image_url_objects

    def _get_preferred_image_urls(self, use_downloaded):
        if use_downloaded:
            return [
                image_url_object.downloaded_url
                for image_url_object in self._image_url_objects
            ]
        else:
            return [
                image_url_object.original_url
                for image_url_object in self._image_url_objects
            ]

    def build(self, use_downloaded):
        with st.container(border=True):
            st.subheader("Photos", divider=True)
            if not self._image_url_objects:
                st.markdown("There are no photos available to display")
            image_urls = self._get_preferred_image_urls(use_downloaded)
            st.image(image_urls, width=200)


def add_label_value(label: str, value: str):
    st.markdown(f"**{label}:** {value}")


def add_label_list(label: str, lst: list[str]):
    if not lst:
        value_str = "None"
    elif len(lst) == 1:
        value_str = lst[0]
    else:
        value_str = ", ".join(lst)
    add_label_value(label, value_str)


class PersonalDetailsBuilder:
    def __init__(self, notice: Notice):
        self._notice = notice

    def _add_name(self, name: Optional[str], forename: Optional[str]):
        name = name or ""
        forename = forename or ""
        fullname = f"{name}, {forename}"
        add_label_value("Name", fullname)

    def _add_date_of_birth(self, date_of_birth: datetime.date):
        date_of_birth_str = get_human_readable_date(date_of_birth)
        age = calculate_age(date_of_birth)
        value = f"{date_of_birth_str} ({age} years)"
        add_label_value("Date of Birth", value)

    def _add_distinguishing_marks(self, distinguishing_marks: str):
        add_label_value("Distinguishing Marks", distinguishing_marks)

    def _add_country_of_birth(self, country_of_birth: _Country):
        add_label_value("Country of Birth", country_of_birth.value)

    def _add_nationalities(self, nationalities: list[_Country]):
        nationalities_names = [country.value for country in nationalities]
        add_label_list("Nationalities", nationalities_names)

    def _add_languages_spoken(self, languages: list[_Language]):
        languages_names = [language.value for language in languages]
        add_label_list("Languages", languages_names)

    def _add_eyes_colors(self, eye_colors: list[_EyeColor]):
        eye_colors_names = [eye_color.value for eye_color in eye_colors]
        add_label_list("Eyes Colors", eye_colors_names)

    def _add_hairs_colors(self, hair_colors: list[_HairColor]):
        hair_colors_names = [hair_color.value for hair_color in hair_colors]
        add_label_list("Hairs Colors", hair_colors_names)

    def _add_sex(self, sex: _Sex):
        add_label_value("Sex", sex.value)

    def _add_place_of_birth(self, place_of_birth: str):
        add_label_value("Place of Birth", place_of_birth)

    def _add_height(self, height: float):
        add_label_value("Height", f"{height} m")

    def _add_weight(self, weight: float):
        add_label_value("Weight", f"{weight} kg")

    def build(self):
        with st.container(border=True):
            st.subheader("Personal Details", divider=True)
            if self._notice.name or self._notice.forename:
                self._add_name(self._notice.name, self._notice.forename)
            if self._notice.date_of_birth:
                self._add_date_of_birth(self._notice.date_of_birth)
            if self._notice.distinguishing_marks:
                self._add_distinguishing_marks(self._notice.distinguishing_marks)
            if self._notice.country_of_birth:
                self._add_country_of_birth(self._notice.country_of_birth)
            if self._notice.nationalities:
                self._add_nationalities(self._notice.nationalities)
            if self._notice.languages_spoken:
                self._add_languages_spoken(self._notice.languages_spoken)
            if self._notice.eye_colors:
                self._add_eyes_colors(self._notice.eye_colors)
            if self._notice.hair_colors:
                self._add_hairs_colors(self._notice.hair_colors)
            if self._notice.sex:
                self._add_sex(self._notice.sex)
            if self._notice.place_of_birth:
                self._add_place_of_birth(self._notice.place_of_birth)
            if self._notice.height:
                self._add_height(self._notice.height)
            if self._notice.weight:
                self._add_weight(self._notice.weight)


class ArrestWarrantBuilder:
    def __init__(self, arrest_warrant: ArrestWarrant):
        self._arrest_warrant = arrest_warrant

    def _add_charge(self, charge: str):
        add_label_value("Charge", charge)

    def _add_charge_translation(self, charge_translation: str):
        add_label_value("Charge Translation", charge_translation)

    def _add_charge_issuing_country(self, charge_issuing_country: _Country):
        add_label_value("Charge Issuing Country", charge_issuing_country.value)

    def _add_offense_types(self, offense_types: Optional[_OffenseType]):
        if not offense_types:
            add_label_value("Offense Types", "Unclassified")
        else:
            offense_names = [offense_type.value for offense_type in offense_types]
            add_label_list("Offense Types", offense_names)

    def build(self):
        with st.container(border=True):
            if self._arrest_warrant.charge:
                self._add_charge(self._arrest_warrant.charge)
            if self._arrest_warrant.charge_translation:
                self._add_charge_translation(self._arrest_warrant.charge_translation)
            if self._arrest_warrant.issuing_country:
                self._add_charge_issuing_country(self._arrest_warrant.issuing_country)
            self._add_offense_types((self._arrest_warrant.offense_types))


class ArrestWarrantsBuilder:
    def __init__(self, arrest_warrants: list[ArrestWarrant]):
        self._arrest_warrants = arrest_warrants

    def _add_arrest_warrant(self, arrest_warrant: ArrestWarrant):
        aw_builder = ArrestWarrantBuilder(arrest_warrant)
        return aw_builder.build()

    def build(self):
        with st.container(border=True):
            st.subheader("Arrest Warrants", divider=True)
            for arrest_warrant in self._arrest_warrants:
                self._add_arrest_warrant(arrest_warrant)


class AdditionalInformationBuilder:
    def __init__(self, notice: Notice):
        self._notice = notice

    def _add_last_fetched_date(self, last_fetched_date: datetime.date):
        local_dt = to_local_datetime(last_fetched_date)
        human_readable = get_human_readable_date_time(local_dt)
        add_label_value("Last Fetched Date", human_readable)

    def _add_fetched_from_url(self, fetched_from_url: str):
        add_label_value("Fetched from", fetched_from_url)

    def build(self):
        with st.container(border=True):
            st.subheader("Additional Information", divider=True)
            self._add_last_fetched_date(self._notice.last_fetched_date)
            self._add_fetched_from_url(self._notice.url)




