import time

detections = {}
detected_people = set()


def is_activated(timestamp, people):
    global detections

    # update detections with the detected people of the last frame
    detections[timestamp] = people
    detected_people.update(people)

    # remove detections that are older than fifteen seconds
    now = time.time()
    detections = {timestamp: people for timestamp, people in detections.items() if timestamp >= now - 15}

    # calculate the max hit fail ratio for every person for the frames of the last fifteen seconds
    max_hit_ratio = calculate_max_hit_ratio()

    # activated if the hit ratio is greater than 15%
    return max_hit_ratio > 15


def calculate_max_hit_ratio():
    if len(detected_people) == 0:
        return 0

    hit_ratios = {}

    # we will count the intervals between hits and fails for every person to calculate their overall ratio
    for person in detected_people:

        # initialize both hit and fail duration to 0
        hit_duration = 0
        fail_duration = 0

        # take the first timestamp of the detections as timestamp for comparison
        previous_timestamp = list(detections.keys())[0]

        # iterate over all detections
        for timestamp, people in detections.items():

            # if the person was detected in this detection or in the previous one, we add the duration to hit duration
            if person in detections[previous_timestamp] or person in people:
                hit_duration += timestamp - previous_timestamp

            # otherwise we add the duration to the fail duration
            else:
                fail_duration += timestamp - previous_timestamp

            # set this timestamp to be the next one we will compare with
            previous_timestamp = timestamp

        # add the hit ratio for this person to the list of hit_ratios (and avoid division by zero)
        hit_ratio = 100 * hit_duration / (hit_duration + fail_duration) if hit_duration + fail_duration != 0 else 0
        hit_ratios[person] = hit_ratio

    # remove people that have not been detected in the last fifteen seconds from the detected_people set
    # TODO: how can we remove items from a set while we iterate over it??
    for person, hit_ratio in hit_ratios.items():
        if hit_ratio == 0:
            detected_people.remove(person)

    return max(hit_ratios.values())
