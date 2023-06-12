import json
import re


def type_validation(check_file):
    check_file = json.loads(check_file)
    error_count = {'bus_id': 0, 'stop_id': 0, 'stop_name': 0, 'next_stop': 0, 'stop_type': 0, 'a_time': 0}
    for i in range(len(check_file)):
        for key in check_file[i]:
            value = check_file[i][key]
            if key == "bus_id" or key == "stop_id" or key == "next_stop":
                if not isinstance(value, int):
                    error_count[key] += 1
            elif key == "stop_type":
                if not isinstance(value, str) or len(value) > 1:
                    error_count[key] += 1
            else:
                if not isinstance(value, str) or value == "":
                    error_count[key] += 1
    errors = sum(error_count.values())
    print(f"Type and required field validation: {errors} errors")
    for key in error_count:
        print(f"{key}: {error_count[key]}")


def format_validation(check_file):
    check_file = json.loads(check_file)
    error_count = {'stop_name': 0, 'stop_type': 0, 'a_time': 0}
    for i in range(len(check_file)):
        for key in check_file[i]:
            value = check_file[i][key]
            if key == "stop_name":
                if not re.match(r"(([A-Z][a-z]+)\s)+(Street|Boulevard|Avenue|Road)$", value):
                    error_count[key] += 1
            elif key == "stop_type":
                if not re.match("[SOF]?$", value):
                    error_count[key] += 1
            elif key == "a_time":
                if not re.match("([01][0-9]|2[0-3]):([0-5][0-9])$", value):
                    error_count[key] += 1
    errors = sum(error_count.values())
    print(f"Format validation: {errors} errors")
    for key in error_count:
        print(f"{key}: {error_count[key]}")


def buslines(check_file):
    check_file = json.loads(check_file)
    lines = []
    for i in range(len(check_file)):
        lines.append(check_file[i]["bus_id"])
    print("Line names and number of stops:")
    for id in set(lines):
        print(f"bus_id: {id}, stops: {lines.count(id)}")


def check_lines(check_file):
    check_file = json.loads(check_file)
    start_stops, transfer_stops, finish_stops = [], [], []
    stop_names = []
    check_start, check_stop = {}, {}
    for i in range(len(check_file)):
        bus_id =  check_file[i]["bus_id"]
        if not bus_id in check_start:
            check_start[bus_id] = 0
            check_stop[bus_id] = 0
        last_bus_id = check_file[i-1]["bus_id"] if i > 0 else "0"
        next_bus_id = check_file[i+1]["bus_id"] if i < (len(check_file) - 1) else "0"
        stop_name = check_file[i]["stop_name"]
        stop_type = check_file[i]["stop_type"]
        if stop_name in stop_names:
            if stop_name not in transfer_stops:
                transfer_stops.append(stop_name)
        else:
            stop_names.append((stop_name))
        if stop_type == "S":
            check_start[bus_id] += 1
            if stop_name not in start_stops:
                start_stops.append(stop_name)
        elif stop_type == "F":
            check_stop[bus_id] += 1
            if stop_name not in finish_stops:
                finish_stops.append(stop_name)
    for key in check_start:
        if check_start[key] != 1 or check_stop[key] != 1:
            print(f"There is no start or end stop for the line: {key}")
            return None
    print(f"Start stops: {len(start_stops)} {sorted(start_stops)}")
    print(f"Transfer stops: {len(transfer_stops)} {sorted(transfer_stops)}")
    print(f"Finish stops: {len(finish_stops)} {sorted(finish_stops)}")


def arrival_test(check_file):
    check_file = json.loads(check_file)
    arr_times = {}
    failed = []
    print("Arrival time test:")
    for i in range(len(check_file)):
        bus_id = check_file[i]["bus_id"]
        stop_name = check_file[i]["stop_name"]
        a_time = check_file[i]["a_time"]
        if bus_id not in arr_times or arr_times[bus_id] < a_time:
            arr_times[bus_id] = a_time
        elif bus_id not in failed:
            print(f"bus_id line {bus_id}: wrong time on station {stop_name}")
            failed.append(bus_id)
    if not failed:
        print("OK")


def stops_test(check_file):
    check_file = json.loads(check_file)
    start_stops, transfer_stops, finish_stops, ondemand_stops = [], [], [], []
    stop_names = []
    wrong_stops = []
    print("On demand stops test:")
    for i in range(len(check_file)):
        stop_name = check_file[i]["stop_name"]
        stop_type = check_file[i]["stop_type"]
        if stop_name in stop_names:
            if stop_name not in transfer_stops:
                transfer_stops.append(stop_name)
        else:
            stop_names.append((stop_name))
        if stop_type == "S":
            if stop_name not in start_stops:
                start_stops.append(stop_name)
        elif stop_type == "F":
            if stop_name not in finish_stops:
                finish_stops.append(stop_name)
    for i in range(len(check_file)):
        stop_name = check_file[i]["stop_name"]
        stop_type = check_file[i]["stop_type"]
        if stop_type == "O":
            if stop_name in start_stops or stop_name in finish_stops or stop_name in transfer_stops:
                wrong_stops.append(stop_name)
    if wrong_stops:
        print(f"wrong stop type: {sorted(wrong_stops)}")
    else:
        print("OK")


stops_test(input())
