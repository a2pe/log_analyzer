import os
import re
from datetime import datetime

import json

from collections import Counter

file_path = input("Enter the path to the log file (including the file name): ")
file_path_abs = os.path.abspath(file_path)
file_path_dir = os.path.dirname(file_path)

with open(file_path_abs, 'r') as f:
    data = f.readlines()

# Counting the number of lines in the output.
num_lines = len(data)

with open(file_path_abs, 'r') as f:
    text = f.read()


def get_nums_of_each_request(input_text):
    """Calculating the number of each request method in the log file with the regular expression."""
    pattern_1 = re.compile(r'(GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|TRACE)')
    request_data = pattern_1.findall(input_text)
    cnt = dict(Counter(request_data))
    return cnt


def get_ips_with_max_requests(input_text):
    """With the regular expression, finding the IP addresses in the log file.
    Calculating the maximum number of requests and the corresponding IP address(es) these requests were coming from."""
    reg_x = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    pattern_2 = re.compile(reg_x)
    request_data = pattern_2.findall(input_text)
    cnt = dict(Counter(request_data))
    nums = [u for u in cnt.values()]
    new_l = []
    for i in range(3):
        new_l.append(max(nums))
        nums.remove(max(nums))
    ips = []
    counter = 0
    for i in new_l:
        for k, j in cnt.items():
            if j == i:
                ips.append(k)
                counter += 1
                if counter == 3:
                    break
    # new = [i for i in cnt.keys() if cnt[i] in new_l]  # This option could provide more IPs than required.
    # return new
    return ips


def get_longest_requests(input_text):
    """Finding the longest requests from the log file."""
    # Adding the duration of each request to the list.
    requests = [input_text.split('\n')[i].split('"')[6] for i in range(num_lines)]
    # Converting string values into integers.
    requests_ints = [int(i) for i in requests]

    # Retrieving the maximum duration values from the list.
    top_3_durations = []
    for i in range(3):
        top_3_durations.append(max(requests_ints))
        requests_ints.remove(max(requests_ints))

    # Getting the indexes for the maximum values.
    indexes = []
    for i in range(len(top_3_durations)):
        requests_copy = [int(i) for i in requests]
        indexes.append(requests_copy.index(top_3_durations[i]))

    # Collecting the data on IP address, Data/Time, Method, URL for the longest requests.
    # Retrieving Request IPs for the longest requests.
    all_requests_ips = [input_text.split('\n')[i].split(' ')[0] for i in range(num_lines)]
    ips = [all_requests_ips[i] for i in indexes]

    # Retrieving Request Date/ Time for the longest requests.
    all_requests_times = [input_text.split('\n')[i].split(' ')[3] for i in range(num_lines)]
    request_times = [all_requests_times[i] for i in indexes]
    request_times_cleared = []
    for i in range(len(request_times)):
        request_times_cleared.append(''.join(j for j in request_times[i] if not j in ['[']))

    # Retrieving Request Methods for the longest requests.
    all_requests_methods = [input_text.split('\n')[i].split(' ')[5] for i in range(num_lines)]
    request_methods = [all_requests_methods[i] for i in indexes]
    request_methods_cleared = []
    for i in range(len(request_methods)):
        request_methods_cleared.append(''.join(j for j in request_methods[i] if not j in ['"']))

    # Retrieving Request URLs for the longest requests.
    all_requests_urls = [input_text.split('\n')[i].split(' ')[10] for i in range(num_lines)]
    request_urls = [all_requests_urls[i] for i in indexes]
    request_urls_cleared = []
    for i in range(len(request_urls)):
        request_urls_cleared.append(''.join(j for j in request_urls[i] if not j in ['"']))

    # Getting the outcome data with the required fields.
    names = ['Duration', 'IP address', 'Request Method', 'Request URL', 'Request Time']
    all_data = list(zip(top_3_durations, ips, request_methods_cleared, request_urls_cleared, request_times_cleared))
    upd_data = [dict(zip(names, all_data[i])) for i in range(len(all_data))]
    return upd_data


def getting_report(input_text):
    """Building the report with all the required data and saving it to .JSON file."""
    num_req = {'Number of Requests': num_lines}
    requests_with_details = get_nums_of_each_request(input_text)
    top_ips = {'Top 3 IP addresses': get_ips_with_max_requests(input_text)}
    longest_requests = {'3 Longest Requests:': get_longest_requests(input_text)}

    report = (f'Log Analyzing Report\nNumber of Requests: {num_lines}\n{requests_with_details}\n'
              f'Top 3 IP addresses, most requests were coming from:\n{get_ips_with_max_requests(input_text)}\n'
              f'3 Longest Requests: \n{get_longest_requests(input_text)}')

    final_dict = {}
    final_dict.update(num_req)
    final_dict.update(requests_with_details)
    final_dict.update(top_ips)
    final_dict.update(longest_requests)

    filename = datetime.now().strftime("%Y-%m-%dT%H%M") + "log.json"
    file_to_save = os.path.join(file_path_dir, filename)
    with open(file_to_save, 'w+') as f:
        json.dump(final_dict, f, indent=4)

    return report


print(getting_report(text))
