import streamlit as st
import requests
import json

BACKEND_URL = "http://127.0.0.1:8000"

st.title("Sentiment Analysis & TTS for News")

company_name = st.text_input("Enter Company Name", "Tesla")

if st.button("Analyze Sentiment"):
    response = requests.post(f"{BACKEND_URL}/analyze_sentiment/", params={"company": company_name})
    if response.status_code == 200:
        data = response.json()
        st.subheader(f"Sentiment Analysis for {data['Company']}")
        
        # Display the sentiment summary
        if "SentimentSummary" in data:
            st.info(data["SentimentSummary"])
            
        # Display the comparative sentiment score
        if "ComparativeSentiment" in data:
            st.subheader("Sentiment Distribution")
            sentiment_data = data["ComparativeSentiment"]["Comparative Sentiment Score"]["Sentiment Distribution"]
            
            # Create a horizontal bar chart for sentiment distribution
            st.bar_chart(sentiment_data)
            
            # Display sentiment counts
            col1, col2, col3 = st.columns(3)
            col1.metric("Positive", sentiment_data["Positive"])
            col2.metric("Negative", sentiment_data["Negative"])
            col3.metric("Neutral", sentiment_data["Neutral"])
            
            # Display raw JSON
            with st.expander("View Raw Sentiment Data"):
                st.json(data["ComparativeSentiment"])
        
        # Display articles
        st.subheader("News Articles")
        for article in data["Articles"]:
            st.write(f"**Title:** {article['Title']}")
            st.write(f"**Summary:** {article['Summary']}")
            st.write(f"**Sentiment:** {article['Sentiment']}")
            st.write("---")
    else:
        st.error("Error fetching sentiment analysis.")

if st.button("Generate Report & Hindi TTS Audio"):
    report_response = requests.post(f"{BACKEND_URL}/generate_report/", params={"company": company_name})

    if report_response.status_code == 200:
        report_data = report_response.json()
        st.subheader("Generated Report")
        st.write(report_data["report"])
        
        # Display sentiment summary
        if "sentiment_summary" in report_data:
            st.info(report_data["sentiment_summary"])
            
        # Display comparative sentiment
        if "comparative_sentiment" in report_data:
            st.subheader("Sentiment Distribution")
            sentiment_data = report_data["comparative_sentiment"]["Comparative Sentiment Score"]["Sentiment Distribution"]
            
            # Create a horizontal bar chart for sentiment distribution
            st.bar_chart(sentiment_data)
            
            # Display sentiment counts
            col1, col2, col3 = st.columns(3)
            col1.metric("Positive", sentiment_data["Positive"])
            col2.metric("Negative", sentiment_data["Negative"])
            col3.metric("Neutral", sentiment_data["Neutral"])
            
            # Display raw JSON
            with st.expander("View Raw Sentiment Data"):
                st.json(report_data["comparative_sentiment"])

        # Request Hindi TTS for the generated report
        tts_response = requests.post(f"{BACKEND_URL}/tts/", json={"text": report_data["report"]})

        if tts_response.status_code == 200:
            audio_file = "report_hindi.mp3"

            # Save the audio file from response
            with open(audio_file, "wb") as f:
                f.write(tts_response.content)

            # Play and offer download of the Hindi audio report
            st.audio(audio_file, format="audio/mp3")
            st.download_button("Download Hindi TTS Report", data=open(audio_file, "rb"), file_name="report_hindi.mp3", mime="audio/mpeg")
        else:
            st.error("Error generating Hindi TTS audio.")
    else:
        st.error("Error generating report.")