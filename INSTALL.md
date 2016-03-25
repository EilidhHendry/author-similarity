sudo apt-get install git nginx postgresql postgresql-contrib python-psycopg2 libpq-dev rabbitmq-server python-pip python-dev cython python-numpy python-scipy libxml2-dev libxslt-dev

sudo pip install virtualenv

git clone git@github.com:EilidhHendry/author-similarity.git
cd author-similarity

virtualenv —system-site-packages venv
source venv/bin/activate
pip install -r requirements/server.txt
./scripts/nltk_prep.sh

npm install
sudo npm install -g gulp

gulp
