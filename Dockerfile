FROM python:3.11

RUN pip install streamlit scikit-learn requests

WORKDIR /app

COPY . .

CMD ["streamlit", "run", "--server.port", "8080", "app.py"]
