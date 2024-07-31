import pandas as pd
import streamlit as st

def read_log_ver1(filepath):
    # Initialize a list to store the extracted data
    parsed_data = []

    # Open and read the log file
    with open(filepath, "r", encoding="utf-8", errors="replace") as file:
        try:
            for line in file:
                line = line.strip()
                timestamp, rest = line.split(" INFO: ", 1)

                parts = rest.split(" | ")
                # initialize with default values
                validity = cert = manufac = spg = item_desc = country = city = ip = "None"
                if len(parts) == 8:
                    validity, cert, manufac, spg, item_desc, country, city, ip = parts
                else:
                    pass

                line_dict = {
                    "timestamp": timestamp,
                    "validity": validity,
                    "cert": cert,
                    "manufac": manufac,
                    "spg": spg,
                    "item_desc": item_desc,
                    "country": country,
                    "city": city,
                    "ip": ip,
                }
                parsed_data.append(line_dict)
        except Exception as e:
            print(f"Error parsing line: {line} - {e}")
    # st.write(parsed_data)
    return parsed_data

def read_log_ver2(filepath):
    # Initialize a list to store the extracted data
    parsed_data = []

    # Open and read the log file
    with open(filepath, "r", encoding="utf-8", errors="replace") as file:
        try:
            for line in file:
                line = line.strip()
                timestamp, rest = line.split(" INFO: ", 1)

                parts = rest.split(" | ")
                # initialize with default values
                validity = cert = manufac = spg = item_desc = country = city = ip = "None"
                if len(parts) == 3:
                    item_desc, validity, country = parts
                else:
                    pass

                line_dict = {
                    "timestamp": timestamp,
                    "validity": validity,
                    "cert": cert,
                    "manufac": manufac,
                    "spg": spg,
                    "item_desc": item_desc,
                    "country": country,
                    "city": city,
                    "ip": ip,
                }
                parsed_data.append(line_dict)
        except Exception as e:
            print(f"Error parsing line: {line} - {e}")
    # st.write(parsed_data)
    return parsed_data

def read_log_ver3(filepath):
    # Initialize a list to store the extracted data
    parsed_data = []

    # Open and read the log file
    with open(filepath, "r", encoding="utf-8", errors="replace") as file:
        try:
            for line in file:
                line = line.strip()
                timestamp, rest = line.split(" INFO: ", 1)

                parts = rest.split(" | ")
                # initialize with default values
                validity = cert = manufac = spg = item_desc = country = city = ip = "None"
                if len(parts) == 8:
                    validity, cert, spg, manufac, item_desc, country, city, ip = parts
                else:
                    pass

                line_dict = {
                    "timestamp": timestamp,
                    "validity": validity,
                    "cert": cert,
                    "manufac": manufac,
                    "spg": spg,
                    "item_desc": item_desc,
                    "country": country,
                    "city": city,
                    "ip": ip,
                }
                parsed_data.append(line_dict)
        except Exception as e:
            print(f"Error parsing line: {line} - {e}")
    # st.write(parsed_data)
    return parsed_data


def reformat_to_df(log_data):
    # st.write("log_data")
    # st.write(log_data)
    # Convert the list of dictionaries to a DataFrame
    log_df = pd.DataFrame(log_data)
    # st.write("log_df")
    # st.write(log_df)
    if "timestamp" in log_df.columns:
        log_df["timestamp"] = pd.to_datetime(log_df["timestamp"])
        log_df["date"] = log_df["timestamp"].dt.date

    if "validity" in log_df.columns:
        log_df["validity"] = log_df["validity"].str.lower()
    if "item_desc" in log_df.columns:
        log_df["item_desc"] = log_df["item_desc"].str.upper()

    return log_df


def merge_and_reformat_logs():

    parsed_data = read_log_ver1("logs//single_search_ver1.log") + read_log_ver2("logs//single_search_ver2.log") + read_log_ver3("logs//single_search_ver3.log")
    # st.write(parsed_data)
    log_df = reformat_to_df(parsed_data)
    # st.write(log_df)
    return log_df