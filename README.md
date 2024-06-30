# hackbcn

To run a fast demo setup Python do the following:

Setup the .env file at the root folder. For that, you need an api key from [hume.ai](https://beta.hume.ai/) and [openai](https://openai.com/).

```
#.env
HUMEAI_APIKEY = ""
HUMEAI_UPLOAD_ENDPOINT = "https://api.hume.ai/v0/assets"
HUMEAI_BATCH_JOB_ENDPOINT = "https://api.hume.ai/v0/batch/jobs"
OPENAI_API_KEY = ""
```

Run this code:

```python
pip install -r requirements.txt
streamlit run app.py
```