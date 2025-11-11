# %% [markdown]
# # AirBnB Analysis - Data 2 Insights!

# %% [markdown]
# ## Package Imports

# %%
import numpy as np
import pandas as pd
import chardet
import psutil

# %% [markdown]
# ## User Defined Functions

# %%
def set_data_types(df):

    """
    Optimize the memory usage of a pandas DataFrame by adjusting column data types.

    This function:
      - Creates a copy of the input DataFrame to prevent modifying the original.
      - Identifies columns with object, integer, or float data types.
      - Converts object type columns to 'category' if the number of unique values is
          less than half the number of rows, reducing memory usage.
      - Downcasts integer columns to the smallest possible subtype ('int8', 'int16', 'int32', or 'int64')
          based on their min/max values.
      - Downcasts float columns to 'float16' or 'float32' based on their numeric range.
      - Returns a DataFrame with optimized data types for efficient memory consumption.

    Args:
        df (pandas.DataFrame): The input DataFrame to optimize.

    Returns:
        pandas.DataFrame: A copy of the DataFrame with optimized column data types.
    """
    import gc
    from pandas.api.types import is_integer_dtype, is_float_dtype

    # Creating copy of the original dataframe NOT to amend it
    df = df.copy()

    # Collecting similar data types columns in lists.
    object_columns = df.select_dtypes(include= ['object']).columns
    int_columns = df.select_dtypes(include= ['int']).columns
    float_columns = df.select_dtypes(include= ['float']).columns


    # Converting the object data type columns into category data type for memory reduction
    for col in object_columns:
        if (df[col].nunique(dropna= False)) < (df.shape[0] / 2):
            df[col] = df[col].astype('category')

    # Choosing the proper size for the integer datatypes
    for col in int_columns:
        temp = df[col]
        if is_integer_dtype(temp):
            df[col] = pd.to_numeric(temp, downcast= 'integer')
        elif is_float_dtype(temp):
            df[col] = pd.to_numeric(temp, downcast= 'float')

    gc.collect()

    # Returning the memory efficient copy of the original dataframe
    return df

# %%
def rename_columns(df):
    
    """
    Standardize DataFrame column names to camel case without spaces, underscores, or dots.

    This function:
      - Creates a copy of the input DataFrame to avoid modifying the original.
      - Renames each column by:
        - converting all characters to lowercase,
        - capitalizing the first letter of each word,
        - removing underscores, spaces, and periods.
      - Returns a DataFrame with cleaned column headers, ensuring consistency and
          readability for downstream processing.

    Args:
        df (pandas.DataFrame): The input DataFrame whose columns need renaming.

    Returns:
        pandas.DataFrame: A copy of the DataFrame with standardized camel case column names.
    """

    
    # Creating a copy of the original dataframe NOT to amend it
    df = df.copy()

    # Converting the columns' headers into camel case without spaces, underscores, or dots
    df.columns = [col.lower().title().replace("_", "").replace(" ", "").replace(".", "") for col in df.columns]

    #df.columns = (
    #    df.columns
    #    .astype(str)
    #    .str.strip()
    #    .str.replace('[_. ]+', '', regex=True)
    #    .str.title()
    #)
    
    return df

# %%
def print_memory():

    """
    Display the current memory usage of the running Python process in megabytes.

    The function:
      - Retrieves the memory usage (Resident Set Size) of the current process using the psutil library.
      - Prints the memory consumed by the process, formatted in MB to two decimal places.
      - Useful for tracking memory usage at various stages in a notebook, especially after data loading and processing steps.

    Returns:
        None
    """
    import os, psutil

    process = psutil.Process(os.getpid())
    
    mem_mb = process.memory_info().rss / (1024 ** 2)  # Memory in MB
    
    print(f"Current memory usage: {mem_mb:.2f} MB")

# %% [markdown]
# ## Loading & Preprocessing & Reducing Data
# *In this section of the notebook we load the data, parse the date columns and reduce the memory consumption to its lowest levels through converting object columns into Pandas.Category data type, downcasting the numeric data types into the proper size depending on its minimum and maximum range of numbers, and finally standardize the columns' header names for the further processing.*

# %%
# Data dictionary is good for getting a sneak peak about the data then delete it
#print_memory()

listings_data_dictionary = pd.read_csv('Airbnb Data/Listings_data_dictionary.csv')

#print_memory()

# listings_data_dictionary

# del listings_data_dictionary

# %%
# Detecting the dataset encoding!
# This criteria checks the first 10000 bytes which is very low to detect the proper
# encoding, so it's just a sanity check!
# with open('Airbnb Data/Listings.csv', 'rb') as f:
#    result = chardet.detect(f.read(10000)) # Reading the first 10000 bytes to detect
# print(result)

# %%
#print_memory()

listings = pd.read_csv('Airbnb Data/Listings.csv',
                      encoding= 'latin1', # We had a problem with utf-8 encoding.
                      parse_dates= ['host_since'],
                      low_memory= False) # First step to reduce memory.
#print_memory()

# listings

# %%
# The analysis will be conducted on the listings ONLY in Paris.
# Reducing the dataset before implementing any other operations will reduce memory usage.
#print_memory()

listings_paris = listings.loc[listings['city'] =='Paris']

#print_memory()

# %%
# Exploring the memory usage of the dataset before conducting any memory reductions
listings_paris.info(memory_usage= 'deep')

# %%
# Leveraging the user define function (set_data_types) to decrease the data set memory usage
#print_memory()

listings_sm = set_data_types(listings_paris)
listings_sm.info(memory_usage= 'deep')

#print_memory()

# %% [markdown]
# *Reduced more than 60% of the memory reserved for the dataset through setting the proper data type for each column*

# %%
listings_clean = rename_columns(listings_sm)

# listings_clean.columns

# %%
reviews_data_dictionary = pd.read_csv('Airbnb Data/Reviews_data_dictionary.csv',
                                     encoding= 'latin1')
# reviews_data_dictionary.head()

# del reviews_data_dictionary

# %%
reviews = pd.read_csv('Airbnb Data/Reviews.csv',
                     parse_dates= ['date'])

# reviews.head()

# %%
reviews.info(memory_usage= 'deep')

# %%
reviews_sm = set_data_types(reviews)
reviews_sm.info(memory_usage= 'deep')

# %%
reviews_clean = rename_columns(reviews_sm)

# reviews_clean.columns

# %%
print_memory()

del listings_data_dictionary
del reviews_data_dictionary
del listings
del listings_paris
del listings_sm
del reviews
del reviews_sm

print_memory()

# %% [markdown]
# ## Data Exploration
# *In this section we are going to explore the dataset and start building our analysis framework!*

# %%
listings_clean.head()

# %%



