# News Sentiment Analysis with TTS

## Overview
The **News Sentiment Analysis with TTS** project is a web-based application that extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi. The tool allows users to input a company name and receive a structured sentiment report along with an audio output.

---

## Project Structure
The project consists of three main components:
1. **Frontend (Streamlit App)** – A web interface where users input a company name and receive sentiment reports.
2. **Backend (AI Service - `service-2-ai`)** – Performs sentiment analysis and generates Hindi TTS output.
3. **Web Fetch Service** – Fetches relevant news articles for analysis.

---

## Model Details
**The project uses the following AI models:** 
- **Summarization Model:** Utilizes OpenAI/Gemini-based NLP models for extracting key information from articles.
- **Sentiment Analysis Model**

 ![project-architecture](https://github.com/user-attachments/assets/f1ed261e-7e5b-4dc7-b6da-dbb30f6ba933)


---

## Installation & Setup
note:- 
1.  **Feel free to test the API using the provided API keys**
2.  **You can also add and test it with other non-JavaScript websites.**

### 1. Setting Up the Frontend (Streamlit)
```sh
# Navigate to the frontend directory
cd front-end

# Install required dependencies
pip install streamlit 

# Start the Streamlit application
streamlit run app.py
```
**Access the frontend at:** [http://localhost:8501](http://localhost:8501)

---

### 2. Setting Up the AI Backend Service (`service-2-ai`)
```sh
# Navigate to the AI service directory
cd ai-feed-analyzer

# Install required dependencies
pip install fastapi uvicorn requests openai nltk torch torchaudio transformers gtts pydantic

# Start the FastAPI service
uvicorn main:app --reload
```
**Access the AI backend at:** [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 3. Setting Up the Web Fetch Service (News Scraper)
```sh
# Navigate to the web fetch service directory
cd web-fetch-service

# Install dependencies
npm install

# Start the server
node server.js
```
**This endpoint retrieves all scraped data from non-JavaScript websites using bs4:** [http://localhost:3000/fetch-articles](http://localhost:3000/fetch-articles)

---

## API Endpoints
### 1. AI Backend Service (`service-2-ai`)
| Method | Endpoint            | Description                                      |
|--------|--------------------|--------------------------------------------------|
| `POST` | `/analyze`         | Performs sentiment analysis on extracted news   |
| `POST` | `/tts`             | Converts text analysis into Hindi audio output  |

### 2. Web Fetch Service
| Method | Endpoint           | Description                              |
|--------|-------------------|------------------------------------------|
| `GET`  | `/fetch-news`     | Fetches news articles for the given query |

---

## How It Works
1. The user enters a company name in the **Streamlit frontend**.
2. The **Web Fetch Service** fetches news articles related to the company.
3. The **AI Backend Service** analyzes the sentiment of the articles.
4. The AI service generates a comparative sentiment report and converts the summary to **Hindi TTS**.
5. The user receives a structured sentiment report along with an **audio output**.

---

## Technologies Used
- **Frontend:** Streamlit (Python)
- **Backend:** FastAPI, OpenAI, Transformers, Torch, gTTS
- **Web Fetch Service:** Node.js, Express

---

## API Development
**The APIs are designed to facilitate the extraction, processing, and conversion of news articles into structured reports with sentiment analysis and TTS capabilities. The key functionalities include:** 
- **Fetching Articles:** The Web Fetch Service scrapes news articles based on a given query.
- **Processing Data:** The AI Backend Service performs sentiment analysis using NLP models.
- **Generating Speech Output:** The AI backend converts the summarized text into Hindi speech using a TTS model.
- APIs can be accessed via Postman or cURL requests.

---

## API Usage
**The project integrates the following third-party APIs:** 
- **NewsAPI:** Used to fetch news articles based on a given keyword. (Used to get some more data for report analysis apart from scrappinf data)
- **OpenRouter AI:** Utilized for sentiment analysis and NLP-based text summarization.
- **Google TTS (gTTS):** Converts the summarized text into Hindi speech output.

 ---

## Assumption and Limitations
- **For scrapping and getting data more Non-Js websites need to be find** 
- **Further tunnings needed for scrapping the data for more reliable output** 
- **Made Seperate section for news generation, article report generation and for hindi tts as if a GET request is send at a streach high load need to tolerate** 
---

## Contribution
Feel free to contribute by submitting a pull request or reporting an issue.

---

## Contact
For any queries, contact the project maintainer at [your-dilhaquecp@gmail.com](mailto:dilhaquecp@gmail.com).

---

## bs4 api output

![Screenshot 2025-03-21 221537](https://github.com/user-attachments/assets/abe78e34-eae5-427a-9e50-a6c379e69aa4)

![Screenshot 2025-03-21 221537](https://github.com/user-attachments/assets/abe78e34-eae5-427a-9e50-a6c379e69aa4)

---

## Demo

Here are the final generated output images..

---

![Screenshot 2025-03-18 221743](https://github.com/user-attachments/assets/ace44f9e-0e1c-4f9d-bdd0-e4948a7cedef)

![Screenshot 2025-03-18 221714](https://github.com/user-attachments/assets/3402c742-d848-458c-bca4-3a4915d06d1f)

Generated Report :-

![Screenshot 2025-03-19 232316](https://github.com/user-attachments/assets/81690bfd-0e45-42c4-927e-1a62229adcfe)

![Screenshot 2025-03-19 232304](https://github.com/user-attachments/assets/8228b0f9-b9d3-4a95-b9a1-b0cebaba93bf)

generated report :-

![Screenshot 2025-03-21 213752](https://github.com/user-attachments/assets/9288e815-af26-4a8e-94c1-d5db4abc2015)

generated overall report :-
![Screenshot 2025-03-21 220948](https://github.com/user-attachments/assets/71034074-c31b-429c-a1e4-3e7b0fd77e85)

![Screenshot 2025-03-21 213819](https://github.com/user-attachments/assets/aeb96297-00ab-42fc-9b3f-0056d5283bc5)

