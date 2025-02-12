#Python code for a Streamlit application that:


#1. Reads a configuration file
#2. Displays a list of sections
#3. Allows users to select a section
#4. Displays property values for the selected section
#5. Allows users to add, update, or delete properties
#6. Allows users to add new sections or delete existing sections
#7. Saves the updated configuration

import streamlit as st
import configparser
import os

# Configuration file path
CONFIG_FILE = 'config.ini'

# Read configuration file
def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

# Save configuration file
def save_config(config):
    with open(CONFIG_FILE, 'w') as config_file:
        config.write(config_file)

# Streamlit application
def main():
    st.title("Configuration File Editor")

    # Read configuration file
    config = read_config()

    # Display list of sections
    st.write("Select a section:")
    sections = config.sections()
    sections.insert(0, "Add New Section")
    selected_section = st.selectbox("Sections", sections)

    if selected_section == "Add New Section":
        # Add new section
        new_section_name = st.text_input("Enter new section name:")
        if st.button("Add Section"):
            config[new_section_name] = {}
            save_config(config)
            st.success("Section added successfully!")
    else:
        # Display property values for selected section
        st.write(f"Properties for {selected_section}:")
        properties = dict(config.items(selected_section))

        # Allow user to add, update, or delete properties
        property_keys = list(properties.keys())
        property_keys.insert(0, "Add New Property")
        selected_property = st.selectbox(f"Properties for {selected_section}", property_keys)

        if selected_property == "Add New Property":
            # Add new property
            new_property_key = st.text_input("Enter new property key:")
            new_property_value = st.text_input("Enter new property value:")
            if st.button("Add Property"):
                config.set(selected_section, new_property_key, new_property_value)
                save_config(config)
                st.success("Property added successfully!")
        else:
            # Update or delete property
            current_value = properties[selected_property]
            updated_value = st.text_input(f"Value for {selected_property}", current_value)

            if st.button("Update Property"):
                config.set(selected_section, selected_property, updated_value)
                save_config(config)
                st.success("Property updated successfully!")

            if st.button("Delete Property"):
                config.remove_option(selected_section, selected_property)
                save_config(config)
                st.success("Property deleted successfully!")

        # Delete section
        if st.button("Delete Section"):
            config.remove_section(selected_section)
            save_config(config)
            st.success("Section deleted successfully!")

if __name__ == "__main__":
    main()


#Make sure to install Streamlit and configparser libraries:

#bash
#pip install streamlit configparser

#Run the application:

#bash
#streamlit run app.py

#Replace app.py with your Python file name.
