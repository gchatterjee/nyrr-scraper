from typing import Union
from race import Race


def getRaceUpdatedTitle(race: Race, template: str) -> str:
    title = "A race" if (race.title is None) else race.title
    return template.format(title)


def getRaceAddedTitle(race: Race) -> str:
    return getRaceUpdatedTitle(race, "<b>{}</b> was added to the race index.")


def getRaceRemovedTitle(race: Race) -> str:
    return getRaceUpdatedTitle(race, "<b>{}</b> was removed from the race index.")


def getRaceChangedTitle(race: Race) -> str:
    return getRaceUpdatedTitle(race, "<b>{}</b> was changed in the race index")


def getScheduleString(race: Race) -> Union[str, None]:
    date, time, location = race.date, race.time, race.location
    if date is None and time is None and location is None:
        return None
    phrases = ["It has been scheduled "]
    if date is not None:
        phrases.append("on {}".format(date))
    if date is not None and time is not None:
        phrases.append(" ")
    if time is not None:
        phrases.append("at {}".format(time))
    if (date is not None or time is not None) and location is not None:
        phrases.append(", ")
    if location is not None:
        phrases.append("at {}".format(location))
    phrases.append(".")
    return "".join(phrases)


def getDateChangeString(raceA: Race, raceB: Race) -> Union[str, None]:
    dateA, dateB, timeA, timeB = raceA.date, raceB.date, raceA.time, raceB.time

    if dateA == dateB and timeA == timeB:
        return None

    dateWasAdded = dateA is None and dateB is not None
    timeWasAdded = timeA is None and timeB is not None
    dateWasRemoved = dateA is not None and dateB is None
    timeWasRemoved = timeA is not None and timeB is None
    dateWasChanged = (not dateWasAdded) and (not dateWasRemoved) and dateA != dateB
    timeWasChanged = (not timeWasAdded) and (not timeWasRemoved) and timeA != timeB

    if dateWasAdded and timeWasAdded:
        result = "It has been scheduled for {dateB} at {timeB}."
    elif dateWasAdded and timeWasRemoved:
        result = "The date has been set for {dateB}, but the time is no longer {timeA}."
    elif dateWasAdded and timeWasChanged:
        result = "The date has been set for {dateB}, and the time has been changed from {timeA} to {timeB}."
    elif dateWasRemoved and timeWasAdded:
        result = "The time has been set to {timeB}, but the date is no longer {dateA}."
    elif dateWasRemoved and timeWasRemoved:
        result = "It is no longer scheduled for {dateA} at {timeA}."
    elif dateWasRemoved and timeWasChanged:
        result = "The time has been changed from {timeA} to {timeB}, but the date is no longer {dateA}."
    elif dateWasChanged and timeWasAdded:
        result = "The date has been changed from {dateA} to {dateB}, and the time has been set to {timeB}."
    elif dateWasChanged and timeWasRemoved:
        result = "The date was changed from {dateA} to {dateB}, but the time was no longer {timeA}."
    else:
        result = (
            "It has been rescheduled from {dateA} at {timeA} to {dateB} at {timeB}."
        )
    return result.format_map(
        {"dateA": dateA, "dateB": dateB, "timeA": timeA, "timeB": timeB}
    )


def getLocationChangeString(raceA: Race, raceB: Race) -> Union[str, None]:
    locationA, locationB = raceA.location, raceB.location
    if locationA == locationB:
        return None
    if locationA is None:
        result = "It will be held at {locationB}."
    elif locationB is None:
        result = "It will no longer be held at {locationA}."
    else:
        result = "It has been moved from {locationA} to {locationB}."
    return result.format_map({"locationA": locationA, "locationB": locationB})


def getStatusString(race: Race) -> Union[str, None]:
    return "It is {}.".format(race.status) if race.status is not None else None


def getStatusChangeString(raceA: Race, raceB: Race) -> Union[str, None]:
    statusA, statusB = raceA.status, raceB.status
    if statusA == statusB:
        return None
    if statusA is None:
        result = "It is now {statusB}."
    elif statusB is None:
        result = "It is no longer {statusA}."
    else:
        result = "It has changed from {statusA} to {statusB}."
    return result.format({"statusA": statusA, "statusB": statusB})


def getUrlString(race: Race) -> Union[str, None]:
    return (
        "For more information, visit https://www.nyrr.org{}".format(race.url)
        if race.url is not None
        else None
    )
