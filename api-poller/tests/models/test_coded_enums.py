from api_poller.models.coded_enum import CodedEnum
from api_poller.models.country import Country

def test_coded_enum_obj_returns_code_based_on_enum_constant():
    class CustomEnum(CodedEnum):
        RED = 1

    assert CustomEnum.RED.code == "RED"

def test_coded_enum_get_enum_obj_by_code():
    class CustomEnum(CodedEnum):
        RED = 1

        @property
        def code(self):
            return self.name.lower()
        
    assert CustomEnum.get_from_code("red") == CustomEnum.RED

def test_country_enum_special_codes():
    assert Country._914.code == "914"
    assert Country._916.code == "916"
    assert Country._922.code == "922"
    assert Country._EU.code == "AT,BE,BG,CY,DE,DK,EE,ES,FI,FR,GR,HR,HU,IE,IT,LT,LU,LV,MT,NL"

def test_country_enum_normal_code():
    assert Country.AD.code == "AD"

def test_country_enum_get_enum_obj_by_code():
    assert Country.get_from_code("AD") == Country.AD

def test_country_enum_get_enum_obj_by_special_code():
    assert Country.get_from_code("AT,BE,BG,CY,DE,DK,EE,ES,FI,FR,GR,HR,HU,IE,IT,LT,LU,LV,MT,NL") == Country._EU