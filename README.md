# YouTube Script Generator

An AI-powered application that generates engaging YouTube scripts based on inspirational video transcripts.

## Features

- Generate scripts with customizable word count
- Clean, professional formatting
- Download scripts in Markdown format
- User-friendly interface

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

5. Run the application:
```bash
streamlit run app.py
```

## Deployment

This application is deployed on Streamlit Cloud. To deploy your own version:

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your OpenAI API key in the Streamlit Cloud secrets
5. Deploy!

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key

## License

MIT License 