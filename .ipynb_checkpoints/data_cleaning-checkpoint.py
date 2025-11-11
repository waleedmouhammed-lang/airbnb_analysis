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
    import pandas as pd

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
