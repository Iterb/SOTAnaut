FROM python:3.9-slim

RUN apt-get update && apt-get install -y wait-for-it

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN pip install -U langchain-community
CMD ["wait-for-it", "elasticsearch:9200", "--", "python", "-m", "sotanaut.main"]
