import pandas as pd
import os
import requests
from urllib.parse import urlparse

def get_high_quality_amazon_image_url(url):
    """Converts an Amazon image link to its highest quality version."""
    base_url = url.split("V1")[0]
    return f"{base_url}V1.jpg"


def download_and_update_posters(csv_filepath, image_folder="movie_posters"):
    """Downloads posters, renames sequentially, uses high-quality URLs."""

    df = pd.read_csv(csv_filepath)

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    for index, row in df.iterrows():
        poster_url = row['Poster_Link']
        if poster_url != "" and poster_url != "Unknown" and not pd.isna(poster_url):
            try:

                high_quality_url = get_high_quality_amazon_image_url(poster_url) # Call function here



                response = requests.get(high_quality_url, stream=True) # Download high-quality
                response.raise_for_status()


                filename = f"{index}.jpg"
                local_filepath = os.path.join(image_folder, filename)

                with open(local_filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)


                df.loc[index, 'Poster_Link'] = local_filepath  # Update with the local path
                print(f"Downloaded poster {filename} for {row['Series_Title']}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading poster for {row['Series_Title']}: {e}")
                df.loc[index, 'Poster_Link'] = "Unknown"


            except Exception as e:  # General error handling
                print(f"Unexpected error for {row['Series_Title']}: {e}")
                df.loc[index, 'Poster_Link'] = "Unknown"

        elif pd.isna(poster_url) or poster_url == "":  # Handle missing URLs
            df.loc[index, 'Poster_Link'] = "Unknown"

    df.to_csv("final_movie_data_updated.csv", index=False)



# Example usage:
download_and_update_posters(r"C:\Users\harsh\OneDrive\Desktop\final_project\final_movie_data.csv")