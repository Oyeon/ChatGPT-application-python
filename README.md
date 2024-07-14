# GPTchat

GPTchat is a project that leverages OpenAI's GPT-3.5-turbo-0125 model to provide various services such as ad copy generation and document summarization. This project is built using Streamlit for the web interface.

## Project Structure

The project is organized into the following directories and files:
- `service/summarize_docs/summarize_docs.py`: This script provides a web interface for summarizing documents using the GPT-3.5-turbo-0125 model. It allows users to input text and select a language for the summary. The summarization is performed by sending a prompt to the OpenAI API and displaying the response.

- `service/ads_copywriter/ads_copywriter.py`: This script provides a web interface for generating ad copy using the GPT-3.5-turbo-0125 model. Users can input product details, brand information, and desired tone to generate ad copy. The ad copy is generated by sending a prompt to the OpenAI API and displaying the response.

- `service/summarize_docs/config.yaml`: This configuration file contains settings for the summarization service, including the OpenAI model to use and the supported languages.

- `service/ads_copywriter/config.yaml`: This configuration file contains settings for the ad copy generation service, including the OpenAI model to use.

- `service/summarize_docs/prompts.txt`: This file contains the prompt template used for summarizing documents. It defines the structure and instructions for generating summaries in different languages.

## Installation

To clone the repository and set up the project, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/GPTchat.git
    cd GPTchat/chatgpt_v01
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the `config` directory with the following content:
        ```
        OPENAI_API_KEY=your_openai_api_key
        ```

5. Run the Streamlit applications:
    - For the summarization service:
        ```bash
        streamlit run service/summarize_docs/summarize_docs.py
        ```
    - For the ad copy generation service:
        ```bash
        streamlit run service/ads_copywriter/ads_copywriter.py
        ```

## Usage

- Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).
- For the summarization service, input the text you want to summarize and select the desired language.
- For the ad copy generation service, input the product details, brand information, and desired tone to generate ad copy.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
