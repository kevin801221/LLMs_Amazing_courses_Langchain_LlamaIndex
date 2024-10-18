# Wolfram Alpha API Explorer

This Streamlit application provides an interactive interface to explore various Wolfram Alpha APIs. It allows users to query Wolfram Alpha using different API endpoints and view the results in a user-friendly format.

## Features

- **Simple API**: Get simple images of complete Wolfram Alpha result pages.
- **Short Answers API**: Retrieve concise answers to queries.
- **Full Results API**: Access detailed results with multiple pods of information.
- **Conversational API**: Engage in a conversation-like interaction with Wolfram Alpha.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/wolfram-alpha-explorer.git
   cd wolfram-alpha-explorer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your Wolfram Alpha AppID:
   ```
   WOLFRAM_ALPHA_APPID=your-app-id-here
   ```

## Usage

To run the application, use the following command:

```
streamlit run app.py
```

This will start the Streamlit server and open the application in your default web browser.

## Project Structure

```
wolfram-alpha-explorer/
├── app.py
├── config.py
├── .env
├── requirements.txt
└── pages/
    ├── simple_api.py
    ├── short_answers_api.py
    ├── full_results_api.py
    └── conversational_api.py
```

- `app.py`: The main entry point of the application.
- `config.py`: Configuration file for loading environment variables.
- `.env`: Contains the Wolfram Alpha AppID (not tracked by git).
- `pages/`: Directory containing individual API implementation files.

## Contributing

Contributions to improve the application are welcome. Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Wolfram Alpha for providing the APIs
- Streamlit for the web application framework
