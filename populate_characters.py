import logging
from models import get_engine, create_tables, get_session, Character
from wiki_scraper import WikiScraper

def main():
    engine = get_engine()
    create_tables(engine)
    session = get_session(engine)
    
    scraper = WikiScraper()
    # Adjust the category if the wiki uses a different one.
    characters_list = scraper.fetch_character_list(category="Category:Characters")
    logging.info(f"Fetched {len(characters_list)} characters from the wiki.")
    
    for character_entry in characters_list:
        title = character_entry.get("title")
        # Skip if the character is already in the database.
        existing_character = session.query(Character).filter(Character.name == title).first()
        if existing_character:
            continue
        
        details = scraper.fetch_character_details(title)
        if details:
            new_character = Character(
                name=details["name"],
                perks=details.get("perks"),
                description=details.get("description")
            )
            session.add(new_character)
            session.commit()
            logging.info(f"Added character: {title}")
        else:
            logging.warning(f"Failed to fetch details for character: {title}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
