import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_jobs(user_input, job_data_path='data/jobs.csv'):
    df = pd.read_csv(job_data_path)

    # Remove any null values in important columns
    df = df.dropna(subset=['Job Title', 'Required Skills'])

    # Convert to string just in case
    df['Job Title'] = df['Job Title'].astype(str)
    df['Required Skills'] = df['Required Skills'].astype(str)

    # Combine text for vectorization
    df['text'] = df['Job Title'] + " " + df['Required Skills']

    # Add user input as a new row
    input_df = pd.DataFrame({
        'Job Title': ['User Input'],
        'Required Skills': [user_input],
        'text': ['User Input ' + user_input]
    })

    # Combine with existing job dataset
    combined_df = pd.concat([df, input_df], ignore_index=True)

    # Make sure all text data is string
    combined_df['text'] = combined_df['text'].fillna('').astype(str)

    # TF-IDF vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(combined_df['text'])

    # Similarity calculation
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    # Get top 5 matches
    top_indices = cosine_sim.argsort()[-5:][::-1]
    recommendations = df.iloc[top_indices].copy()
    recommendations['Match %'] = (cosine_sim[top_indices] * 100).round(2)

    return recommendations[['Job Title', 'Required Skills', 'Match %']]


