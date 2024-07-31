FROM python:3.11.0-slim

# Working Directory in container
WORKDIR /productmatchguide_log_dashboard

RUN apt-get update && apt-get install -y apt-utils --no-install-recommends

# install libGL.so.1
RUN apt-get install libgl1-mesa-glx -y

# install libgthread-2.0.so.0
RUN apt-get install libglib2.0-0 -y

# install python requirements
COPY requirements.txt ./requirements.txt
RUN python -m pip install pip --upgrade
RUN pip install --use-deprecated=legacy-resolver -r requirements.txt

# port number to expose
EXPOSE 8501

# copy files in project folder to /productmatchguide_log_dashboard folder
COPY . /productmatchguide_log_dashboard

# codes that runs when container starts
ENTRYPOINT ["streamlit", "run"]
CMD ["dashboard/Log_Tracker.py","--server.headless=true", "--global.developmentMode=false"]
# CMD ["app/🏠_Home.py","--server.headless=true", "--global.developmentMode=false"]

# command for Azure build
# version tag MUST be updated for deployment purpose
# az acr build --registry productMatchGenie --resource-group rg-productmatchgenie-prod --image pmg-log-tracker:0.0.7 .