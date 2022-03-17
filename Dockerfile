FROM python
WORKDIR /usr/src/app
COPY ./ .
RUN pip install -r requirements.txt
CMD ls && python app.py
EXPOSE 5001
