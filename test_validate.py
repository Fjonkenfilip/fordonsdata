from validate import find_missing_packets, find_out_of_order_timestamps, find_stuck_values

def test_flags_stuck_value_once():
    assert find_stuck_values([43.0] * 6) == [4]


def test_accepts_short_run():
    assert find_stuck_values([43.0] * 4) == []


def test_resets_when_value_changes():
    speeds = [43.0] * 4 + [44.0] * 5
    assert find_stuck_values(speeds) == [8]


def test_detects_one_missing_packet():
    assert find_missing_packets([100, 101, 102, 104]) == [103]


def test_detects_multiple_missing_packets():
    assert find_missing_packets([100, 101, 104]) == [102, 103]


def test_accepts_consecutive_packets():
    assert find_missing_packets([100, 101, 102]) == []


def test_detects_timestamp_that_goes_backwards():
    assert find_out_of_order_timestamps([0, 100, 80, 200]) == [2]


def test_accepts_timestamps_in_order():
    assert find_out_of_order_timestamps([0, 100, 200]) == []