------------------------------------------------------------

setup_docs_folder [Function] (lines: 10-11):

Sets up the documentation folder.

This function creates a directory named "docs" if it does not already exist.

Args:
    None

Returns:
    None

Raises:
    None

------------------------------------------------------------

write_to_doc [Function] (lines: 13-17):

Writes unit information to a documentation file.

Args:
    file_path (str): The path to the original file.
    unit_information (list): A list of tuples containing unit information.
        Each tuple should have the following format:
        (unit_name, unit_type, start_line, end_line, unit_description)

Returns:
    None

Raises:
    IOError: If there is an error writing to the file.

------------------------------------------------------------

