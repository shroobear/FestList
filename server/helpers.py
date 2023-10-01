from config import db

from sqlalchemy.orm import joinedload
from flask import make_response, request
from flask_sqlalchemy import SQLAlchemy as sa


class Routing:
    def get_relationship(self, id, orm_class, backref_name, parent_id_name):
        backref = getattr(orm_class, backref_name)
        orm_collection = (
            db.session.query(orm_class)
            .options(joinedload(backref))
            .filter(getattr(orm_class, parent_id_name) == id)
            .all()
        )
        return orm_collection

    def get_all(self, table_class, schema):
        collection = table_class.query.all()

        response = make_response(
            schema.dump(collection),
            200
        )

        return response
    
    def delete_entry(self, id, table_class, deleted_item):
        entry = table_class.query.filter_by(id=id).first()

        if not entry:
            return make_response({'message': f'{deleted_item} not found'}, 404)

        db.session.delete(entry)
        db.session.commit()
        return make_response({'message': f"{deleted_item} successfully deleted."}, 200)
        
    
    def get_by_id(self, id, table_class, schema):
        entry = table_class.query.filter_by(id=id).first()

        if not entry:
            return make_response({'message': 'Entry not found'}, 404)
        
        response = make_response(
            schema.dump(entry),
            200
        )

        return response
    
    def patch(self, id, table_class, schema):
        entry = table_class.query.filter_by(id=id).first()

        if not entry:
            return make_response({'message': 'Entry not found'}, 404)
        
        for attr in request.form:
            setattr(entry, attr, request.form[attr])

            db.session.add(entry)
            db.session.commit()

            return make_response(schema.dump(entry), 200)

