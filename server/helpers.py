from config import db

from sqlalchemy.orm import joinedload
from flask import make_response, request


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

        db.session.delete(entry)
        db.session.commit()

        response_dict = {"message": f"{deleted_item} successfully deleted"}

        response = make_response(response_dict, 200)

        return response
    
    def get_by_id(self, id, table_class, schema):
        entry = table_class.query.filter_by(id=id).first()

        response = make_response(
            schema.dump(entry),
            200
        )

        return response
    
    def patch(self, id, table_class, schema):
        entry = table_class.query.filter_by(id=id).first()

        for attr in request.form:
            setattr(entry, attr, request.form[attr])

            db.session.add(entry)
            db.session.commit()

            response = make_response(schema.dump(entry), 200)

            return response