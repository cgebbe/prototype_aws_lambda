FROM public.ecr.aws/lambda/python:3.9

RUN yum -y install make
RUN python -m pip install --upgrade pip setuptools wheel pip-tools

# setup dependencies
COPY ./requirements.in .
COPY ./requirements-test.in .
RUN pip-compile --output-file requirements.txt requirements.in requirements-test.in -v
RUN pip-sync requirements.txt

COPY . .
CMD [ "src.app.handler" ]
