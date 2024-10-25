import streamlit as st
import pandas as pd
import json

# Recursive function to extract bookmarks from nested structure
def extract_bookmarks(data, platform='Browser'):
    bookmarks = []
    # If data is a list, iterate over each item
    if isinstance(data, list):
        for item in data:
            bookmarks.extend(extract_bookmarks(item, platform))
    # If data is a dict, check for children and title/url fields
    elif isinstance(data, dict):
        # If there's a URL, add the bookmark
        if 'uri' in data:
            bookmarks.append({
                'title': data.get('title', 'Untitled'),
                'url': data['uri'],
                'platform': platform
            })
        # If there are children, process them recursively
        if 'children' in data:
            bookmarks.extend(extract_bookmarks(data['children'], platform))
    return bookmarks

# Function to load browser bookmarks from JSON file
def load_browser_bookmarks(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    bookmarks = extract_bookmarks(data)
    return pd.DataFrame(bookmarks)

# Function to load social media bookmarks (mock data for Twitter)
def load_twitter_bookmarks():
    twitter_data = [
        {'title': 'Twitter Post 1', 'url': 'https://twitter.com/example1', 'platform': 'Twitter'},
        {'title': 'Twitter Post 2', 'url': 'https://twitter.com/example2', 'platform': 'Twitter'}
    ]
    return pd.DataFrame(twitter_data)

# Load bookmarks
browser_bookmarks = load_browser_bookmarks('./bookmarks.json')  # Update path as needed
twitter_bookmarks = load_twitter_bookmarks()

# Combine bookmarks
all_bookmarks = pd.concat([browser_bookmarks, twitter_bookmarks])

# Streamlit App
st.title("Unified Bookmarks Viewer")
st.write("Search and explore all your bookmarks from multiple platforms.")

# Search Input
search_term = st.text_input("Search all bookmarks by keyword")

# Filter Data Based on Search Term
if search_term:
    filtered_data = all_bookmarks[
        all_bookmarks.apply(lambda row: search_term.lower() in row.to_string().lower(), axis=1)
    ]
else:
    filtered_data = all_bookmarks

# Display Results
if not filtered_data.empty:
    st.write(f"### Search Results ({len(filtered_data)} found):")
    for _, row in filtered_data.iterrows():
        st.markdown(f"- [{row['title']}]({row['url']}) - *Platform*: {row['platform']}")
else:
    st.write("No bookmarks found for the search term.")
