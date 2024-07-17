import streamlit as st
import pandas as pd
from utils.streamlit_style import hide_streamlit_style

st.set_page_config(
    page_title="Materials And Mechanical Properties",
    page_icon="pictures/favicon.ico",
)

def get_rating(row):
    conditions = [
        (438.3 <= row['Su'] <= 535.7, 318.6 <= row['Sy'] <= 389.4, 204930 <= row['E'] <= 209070, 71100 <= row['G'] <= 86900, 0.285 <= row['mu'] <= 0.315, 7467 <= row['Ro'] <= 8253),
        (389.6 <= row['Su'] <= 584.4, 283.2 <= row['Sy'] <= 424.8, 202860 <= row['E'] <= 211140, 63200 <= row['G'] <= 94800, 0.27 <= row['mu'] <= 0.33, 7074 <= row['Ro'] <= 8646),
        (340.9 <= row['Su'] <= 633.1, 247.8 <= row['Sy'] <= 460.2, 200790 <= row['E'] <= 213210, 55300 <= row['G'] <= 102700, 0.255 <= row['mu'] <= 0.345, 6681 <= row['Ro'] <= 9039),
        (292.2 <= row['Su'] <= 681.8, 212.4 <= row['Sy'] <= 495.6, 198720 <= row['E'] <= 215280, 47400 <= row['G'] <= 110600, 0.24 <= row['mu'] <= 0.36, 6288 <= row['Ro'] <= 9432)
    ]
    ratings = [5, 4, 3, 2]

    for rating, condition in zip(ratings, conditions):
        if all(condition):
            return rating
    return 1

def feature_eng():
    
    # Hide Streamlit style components
    hide_streamlit_style()

    if 'df' not in st.session_state:
        st.warning("No data available. Please go to the 'Main Page' to load the data.")
        return

    df = st.session_state['df']

    st.write("## 🔧 Feature engineering on the dataframe.")
    st.dataframe(df.head())

    if st.button('Apply Rating'):
        df['rating'] = df.apply(get_rating, axis=1)
        st.session_state['df'] = df
        st.success('Ratings have been applied to the dataframe.')

        # Explanation of the rating
        st.write("""
            The rating feature is based on specific ranges for several properties:
            - **5 stars**: Highest quality based on all properties within specific ranges.
            - **4 stars**: Slightly broader ranges.
            - **3 stars**: Even broader ranges.
            - **2 stars**: The broadest acceptable ranges.
            - **1 star**: Does not meet any of the above criteria.
        """)

        # Display a table explaining the ratings
        rating_data = {
            "Rating": [5, 4, 3, 2, 1],
            "Su Range": ["438.3 - 535.7", "389.6 - 584.4", "340.9 - 633.1", "292.2 - 681.8", "Other"],
            "Sy Range": ["318.6 - 389.4", "283.2 - 424.8", "247.8 - 460.2", "212.4 - 495.6", "Other"],
            "E Range": ["204930 - 209070", "202860 - 211140", "200790 - 213210", "198720 - 215280", "Other"],
            "G Range": ["71100 - 86900", "63200 - 94800", "55300 - 102700", "47400 - 110600", "Other"],
            "mu Range": ["0.285 - 0.315", "0.27 - 0.33", "0.255 - 0.345", "0.24 - 0.36", "Other"],
            "Ro Range": ["7467 - 8253", "7074 - 8646", "6681 - 9039", "6288 - 9432", "Other"]
        }
        rating_df = pd.DataFrame(rating_data)
        st.table(rating_df)

    if st.button('Convert Use to Int'):
        df['Use'] = df['Use'].astype(int)
        st.session_state['df_fe'] = df
        st.success('The "Use" column has been converted to integers.')

    if st.button('Create Su/Sy Feature'):
        df['Su/Sy'] = df['Su'] / df['Sy']
        st.session_state['df_fe'] = df
        st.success('The "Su/Sy" feature has been created.')

    if st.button('Drop Material Column'):
        print(df.columns)
        df.drop(["Material"] , axis=1 , inplace=True)
        st.session_state['df_fe'] = df
        st.success('Material column dropped.')


if __name__ == "__main__":
    feature_eng()