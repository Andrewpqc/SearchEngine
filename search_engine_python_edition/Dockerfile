FROM coady/pylucene
MAINTAINER andrewpqc <JamieOgburn1988@gmail.com>
ENV DEPLOY_PATH /pyluceneapp
RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH
ADD requirements.txt requirements.txt
RUN pip install --index-url http://pypi.doubanio.com/simple/ -r requirements.txt --trusted-host=pypi.doubanio.com
ADD . .
CMD python3 manage.py runserver -h 0.0.0.0 -p 5000




