from flask import Flask, jsonify, abort, request
from models import get_engine, create_tables, get_session, Item, Character
import logging

def create_app(db_url=None):
    """
    Create and configure the Flask app.
    
    Args:
        db_url (str): Database URL to use. If None, defaults to 'sqlite:///items.db'.
    
    Returns:
        Flask app instance.
    """
    app = Flask(__name__)
    
    # Use the provided db_url or default to file-based SQLite.
    if db_url is None:
        db_url = "sqlite:///items.db"
    
    # Set up the database.
    engine = get_engine(db_url)
    create_tables(engine)
    session = get_session(engine)
    
    # Save session and engine in the app's config for later access.
    app.config["DB_SESSION"] = session
    app.config["DB_ENGINE"] = engine

    @app.route("/items", methods=["GET"])
    def get_items():
        session = app.config["DB_SESSION"]
        items = session.query(Item).all()
        result = []
        for item in items:
            result.append({
                "id": item.id,
                "name": item.name,
                "ingredients": item.ingredients,
                "obtaining_method": item.obtaining_method
            })
        return jsonify(result)

    @app.route("/items/<int:item_id>", methods=["GET"])
    def get_item(item_id):
        session = app.config["DB_SESSION"]
        item = session.query(Item).filter(Item.id == item_id).first()
        if not item:
            abort(404)
        result = {
            "id": item.id,
            "name": item.name,
            "ingredients": item.ingredients,
            "obtaining_method": item.obtaining_method
        }
        return jsonify(result)

    @app.route("/characters", methods=["GET"])
    def get_characters():
        session = app.config["DB_SESSION"]
        characters = session.query(Character).all()
        result = []
        for character in characters:
            result.append({
                "id": character.id,
                "name": character.name,
                "perks": character.perks,
                "description": character.description
            })
        return jsonify(result)

    @app.route("/characters/<int:character_id>", methods=["GET"])
    def get_character(character_id):
        session = app.config["DB_SESSION"]
        character = session.query(Character).filter(Character.id == character_id).first()
        if not character:
            abort(404)
        result = {
            "id": character.id,
            "name": character.name,
            "perks": character.perks,
            "description": character.description
        }
        return jsonify(result)

    @app.route("/characters/compare", methods=["GET"])
    def compare_characters():
        """
        Compare multiple characters side-by-side.
        Use query parameter 'ids' with a comma-separated list of character IDs.
        Example: /characters/compare?ids=1,2,3
        """
        ids_param = request.args.get("ids")
        if not ids_param:
            return jsonify({"error": "Please provide character IDs to compare."}), 400
        try:
            character_ids = [int(i) for i in ids_param.split(",")]
        except ValueError:
            return jsonify({"error": "Invalid character IDs."}), 400
        
        session = app.config["DB_SESSION"]
        characters = session.query(Character).filter(Character.id.in_(character_ids)).all()
        if not characters:
            abort(404)
        
        # Build a side-by-side comparison.
        comparison = {}
        for character in characters:
            comparison[character.name] = {
                "perks": character.perks,
                "description": character.description
            }
        return jsonify(comparison)

    return app

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # Create the app with the default database URL.
    app = create_app()
    app.run(debug=True)
