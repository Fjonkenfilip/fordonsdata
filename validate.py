import csv

'''
with open("telemetry.csv", encoding="utf-8", newline="") as file:

    packets = csv.DictReader(file)
    previous_id = None

    for packet in packets:
        current_id = int(packet["sequence_id"])

        if previous_id is not None:
            for missing_id in range(previous_id + 1, current_id):
                print(f"Saknat paket: {missing_id}")

        previous_id = current_id

'''

def find_missing_packets(sequence_ids):
    missing_ids = []
    previous_id = None

    for current_id in sequence_ids:
        if previous_id is not None:
            missing_ids.extend(range(previous_id + 1, current_id))

        previous_id = current_id

    return missing_ids

def find_out_of_order_timestamps(timestamps):
    out_of_order = []

    for index in range(1, len(timestamps)):
        if timestamps[index] < timestamps[index - 1]:
            out_of_order.append(index)

    return out_of_order

def find_stuck_values(values):
    stuck_indices = []
    run_length = 1

    for index in range(1, len(values)):
        if values[index] == values[index - 1]:
            run_length += 1
        else:
            run_length = 1

        if run_length == 5:
            stuck_indices.append(index)

    return stuck_indices

def main():
    with open("telemetry.csv", encoding="utf-8", newline="") as file:
        packets = list(csv.DictReader(file))

    sequence_ids = [int(packet["sequence_id"]) for packet in packets]
    timestamps = [int(packet["timestamp_ms"]) for packet in packets]

    for missing_id in find_missing_packets(sequence_ids):
        print(f"Saknat paket: {missing_id}")

    for index in find_out_of_order_timestamps(timestamps):
        print(
            f"Paket {sequence_ids[index]}: tidsstämpeln gick bakåt "
            f"från {timestamps[index - 1]} till {timestamps[index]} ms"
        )
        speeds = [float(packet["speed_kmh"]) for packet in packets]

    for index in find_stuck_values(speeds):
        print(
            f"Paket {sequence_ids[index]}: misstänkt fastnad hastighet "
            f"({speeds[index]} km/h i fem paket i rad)"
        )


if __name__ == "__main__":
    main()