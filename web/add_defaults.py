#!/usr/bin/env python3
# Add admin user and default collections
# First run the import script you like and save the output in the output dir as tsv file. Then run this script. You can run this script multiple times.
import flask_sqlalchemy
from app import Collection, Item, User, Role, app
from sqlalchemy import create_engine
from flask_security import SQLAlchemyUserDatastore
import csv
from glob import glob
from os.path import basename
from config import ADMIN_PASSWORD
engine = create_engine('sqlite:///app.sqlite', echo = True)
 
db = flask_sqlalchemy.SQLAlchemy(app)
db.create_all()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

#Create user
with app.app_context():
    admin = user_datastore.find_user(email='admin')
if not admin:
    admin = user_datastore.create_user(email='admin', password=ADMIN_PASSWORD)
    db.session.commit()
#Loop collections
for collection in glob('../scripts/output/*.tsv'):
    with open(f'../scripts/{collection}') as f:
        collection_name = basename(collection).split('.')[0].replace('_', ' ').title()
        if db.session.query(Collection).filter_by(user=admin, name=collection_name).first():
            print(f"{collection_name} exists")
            continue  # exists already
        print(collection_name)
        #If new collection, add it to the database
        c = Collection(name=collection_name, user_id=admin.id, public=True)
        db.session.add(c)
        reader = csv.reader(f, delimiter='\t')
        for i, r in enumerate(reader):
            if i == 0:
                continue  # Skip header
            print(r)
            sequence = r[0].strip()
            if not sequence.isnumeric():
                sequence = r[1].strip() if len(r) > 1 else ''
            if not sequence.isnumeric():
                sequence = 0
            name = ' '.join(v.strip() for v in r)
            db.session.add(
                Item(sequence=sequence, name=name, collection=c)
            )
db.session.commit()

