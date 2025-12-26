# scripts/data_cleaning.py

import pandas as pd
import numpy as np
import re
import os

def clean_flipkart_data(input_csv="data/raw/flipkart_raw.csv", output_csv="data/clean/cleaned_flipkart.csv"):
    # Create clean folder if not exists
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Load raw data
    flip = pd.read_csv(input_csv)

    # Drop unnecessary column
    if "Unnamed: 0" in flip.columns:
        flip.drop("Unnamed: 0", axis=1, inplace=True)

    # Price cleanup
    for col in ["Original_Price", "Discounted_Price"]:
        flip[col] = flip[col].str.replace("₹", "").str.replace(",", "").astype(float)

    # Off_Upto cleanup
    if "Off_Upto" in flip.columns:
        flip["Off_Upto"] = flip["Off_Upto"].str.replace("%", "", regex=False)
        flip["Off_Upto"] = pd.to_numeric(flip["Off_Upto"], errors="coerce").fillna(0)

    # Clean product name
    flip["Name"] = flip["Name"].str.replace(r"\s*\(.*?\)", " ", regex=True).str.strip()

    # Extract company and generation
    flip["Company"] = flip["Name"].str.split().str[0]

    def generation(name):
        for g in ["6G", "5G", "4G", "3G", "2G", "1G"]:
            if g in name:
                return g
        return np.nan

    # Optional: keep generation
    # flip["Gen"] = flip["Name"].apply(generation)

    # Display cleaning
    def display_type(s):
        if pd.isna(s):
            return np.nan
        match = re.search(r'\)\s*(.*)$', s)
        return match.group(1) if match else np.nan

    def display_size(s):
        if pd.isna(s):
            return np.nan
        match = re.search(r'\(([\d.]+)', s)
        return float(match.group(1)) if match else np.nan

    flip["Display_Type"] = flip["Display"].apply(display_type)
    flip["Display_Size"] = flip["Display"].apply(display_size)
    if "Display" in flip.columns:
        flip.drop("Display", axis=1, inplace=True)

    # Memory cleanup
    flip["Ram"] = flip["Memory"].str.split("|").str[0]
    flip.loc[flip["Ram"].str.contains("ROM", na=False), "Ram"] = np.nan

    mask = flip["Ram"].str.contains("MB", na=False)
    flip.loc[mask, "Ram"] = (
        flip.loc[mask, "Ram"]
        .str.replace("MB RAM", "", regex=False)
        .str.strip()
        .astype(float)
        .div(1024)
    )

    flip["Ram"] = flip["Ram"].str.replace("GB RAM ", "", regex=False)
    flip["Ram"] = flip["Ram"].str.replace(r'Expandable\s+Upto\s+\d+\s*GB', '', regex=True, case=False)
    flip["Ram"] = flip["Ram"].replace(r'^\s*$', np.nan, regex=True).astype(float).fillna(0)

    flip["Rom"] = flip["Memory"].str.extract(r'\|\s*(.*)')
    flip["Rom"] = (
        flip["Rom"]
        .str.replace(r'\|\s*Expandable\s+Upto\s+\d+\s*(GB|TB)', '', regex=True, case=False)
        .str.replace(r'\|\s*$', '', regex=True)
        .str.strip()
        .replace('', np.nan)
        .str.replace("MB ROM", "", regex=False)
    ).fillna(0).astype(float)

    # Drop unnecessary columns
    flip.drop(columns=["Memory", "Camera", "Off_Upto"], errors="ignore", inplace=True)

    # Remove rows with 0 RAM or ROM
    flip = flip[(flip["Ram"] != 0) & (flip["Rom"] != 0)].reset_index(drop=True)

    # Save cleaned data
    flip.to_csv(output_csv, index=False)
    print(f"Cleaned data saved to {output_csv}")
    return flip


