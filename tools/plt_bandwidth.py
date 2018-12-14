#!/usr/bin/env python
# Helper to generate standardized bandwidth plots

import csv
import os
import sys

BW_PATH = "experiments/network/ref-bandwidth"

def process_files():

    raw_data = {}
    for root, dirs, files in os.walk(BW_PATH):
        for filename in files:
            if filename.endswith(".csv"):
                raw_data[filename] = csv_to_list(os.path.join(BW_PATH, filename))

    for filename, containers in raw_data.items():
        # print("\n\n==============\n\t", filename, ":\n\n")
        for ctn_name, ctn in containers.items():
            # print("\n\n\n\t", ctn_name, ":\n\n")
            for idx, data in enumerate(ctn):

                # print(idx, data)
                # break

                if idx == 0:
                    anchor = data["timestamp"]
                    data["timestamp"] = 0
                    data["bw_ing"] = 0
                    data["bw_egr"] = 0
                    data["ding"] = 0
                    data["degr"] = 0
                    data["dt"] = 0
                    continue

                # update timestamp related to anchor and calculate delta t
                data["timestamp"] -= anchor
                data["dt"] = data["timestamp"] - ctn[idx - 1]["timestamp"]

                # calculate ingress and egress deltas
                data["ding"] = data["ing"] - ctn[idx - 1]["ing"] if data["ing"] > 0 else 0
                data["degr"] = data["egr"] - ctn[idx - 1]["egr"] if data["egr"] > 0 else 0

                # calculate ingress and egress bandwidth
                data["bw_ing"] = data["ding"] / data["dt"] / 1000 * 8  # Kilobits / second
                data["bw_egr"] = data["degr"] / data["dt"] / 1000 * 8

                if data["bw_ing"] < 0 or data["bw_egr"] < 0:
                    prev = ctn[idx - 1]
                    print(
                        "{} \t dt {} \t ing {} \t egr {} \t ding {} \t degr {} \t br_ing {} \t bw_egr {}"
                        .format(prev["timestamp"], prev["dt"], prev["ing"],
                                prev["egr"], prev["ding"], prev["degr"],
                                prev["bw_ing"], prev["bw_egr"]))
                    print(
                        "{} \t dt {} \t ing {} \t egr {} \t ding {} \t degr {} \t br_ing {} \t bw_egr {}"
                        .format(data["timestamp"], data["dt"], data["ing"],
                                data["egr"], data["ding"], data["degr"],
                                data["bw_ing"], data["bw_egr"]))

    return raw_data


def csv_to_list(fpath):

    containers = {}
    with open(fpath, newline='') as fp:
        lines = csv.reader(fp, delimiter=',')

        for row in lines:
            if len(row) < 5:
                continue
            ctn = row[1]
            if ctn not in containers:
                containers[ctn] = []
            entry = {}
            entry["timestamp"] = float(row[0])
            entry["ing"] = float(row[3])
            entry["egr"] = float(row[4])
            containers[ctn].append(entry)

    # sort containers by timestamp (in case it is not sorted in file)
    for key, ctn in containers.items():
        containers[key] = sorted(ctn, key=lambda k: k['timestamp'])

    return containers
