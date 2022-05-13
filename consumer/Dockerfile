FROM python:3

# create app directory
WORKDIR /usr/src/app

# copy the contents from requirements.txt
COPY requirements.txt  ./
RUN pip install --no-cache-dir -r requirements.txt

# current directory
COPY . .

CMD [ "python", "-u", "consume.py" ]