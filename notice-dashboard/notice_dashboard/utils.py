import calendar
import datetime
from decimal import Decimal
import math


def to_local_datetime(utc_dt):
    """
    convert from utc datetime to a locally aware datetime according to the host timezone

    :param utc_dt: utc datetime
    :return: local timezone datetime
    """
    return datetime.datetime.fromtimestamp(calendar.timegm(utc_dt.timetuple()))


def get_human_readable_date_time(dt) -> str:
    s = dt.strftime("%I:%M %p %d/%m/%Y")
    return s


def get_human_readable_date(dt) -> str:
    s = dt.strftime("%d/%m/%Y")
    return s

def millify(n, precision=0, drop_nulls=True, prefixes=[]):
    """
    Humanize number.

    Orginal Source: https://github.com/azaitsev/millify/blob/master/millify/__init__.py
    """
    def remove_exponent(d):
        """Remove exponent."""
        return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()
    millnames = ['', 'k', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
    if prefixes:
        millnames = ['']
        millnames.extend(prefixes)
    n = float(n)
    millidx = max(0, min(len(millnames) - 1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
    result = '{:.{precision}f}'.format(n / 10**(3 * millidx), precision=precision)
    if drop_nulls:
        result = remove_exponent(Decimal(result))
    return '{0}{dx}'.format(result, dx=millnames[millidx])


def calculate_age(birth_date) -> int:
    today = datetime.date.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
