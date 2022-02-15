FROM python:3.7-stretch
WORKDIR /streamlit
COPY ./requirements.txt /streamlit
RUN pip install -r requirements.txt
COPY ./app.py /streamlit
COPY ./streamlit_custom_slider/__init__.py /streamlit/streamlit_custom_slider/__init__.py
COPY ./score_objects.pkl /streamlit
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
