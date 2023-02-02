from datetime import datetime


class NegativeTitlesError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidYearCupError(Exception):
    def __init__(self, message):
        self.message = message


class ImpossibleTitlesError(Exception):
    def __init__(self, message):
        self.message = message


def data_processing(dict: dict):
    if dict["titles"] < 0:
        raise NegativeTitlesError({"error": "titles cannot be negative"})

    year_cup = dict["first_cup"].split("-")[0]
    if (int(year_cup) - 1930) % 4 != 0 or int(year_cup) < 1930:
        raise InvalidYearCupError({"error": "there was no world cup this year"})

    current_year = datetime.now().year
    possible_title = (current_year - int(year_cup)) / 4
    if dict["titles"] > possible_title:
        raise ImpossibleTitlesError(
            {"error": "impossible to have more titles than disputed cups"}
        )
