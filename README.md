# GoPizza-Brand-Analysis-with-Topic-Modeling

Brand analysis of GoPizza was conducted by scraping the reviews of all its branches from Yogiyo, a popular delivery and review site in Korea (gopizza_crawling_yogiyo.py).

After preprocessing the scraped reviews, the important nouns for each branch were visualized using TF-IDF (gopizza_review_tfidf.py).

Then, the topic clusters within the reviews were investigated through topic modeling with Latent Dirichlet Allocation and visualizing it with pyLDAvis (gopizza_review_LDA_topic_modeling.py).

The same process was repeated for the reviews of GoPizza's five main competitors (otherfranchise_crawling_yogiyo.py) and the results were compared to scrutinize GoPizza's brand position amongst its competitors.
