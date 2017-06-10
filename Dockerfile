FROM generalassembly/scipy-notebook:nlp

# install libraries via pip using bash and activating respective environment
RUN ["bash", "-c", "source activate root && pip install twitter tweepy nltk redis"]
RUN ["bash", "-c", "source activate python2 && pip install twitter tweepy nltk redis"]


