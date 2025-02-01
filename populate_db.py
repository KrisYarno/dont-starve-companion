import logging
from models import get_engine, create_tables, get_session, Item
from wiki_scraper import WikiScraper

def main():
    engine = get_engine()
    create_tables(engine)
    session = get_session(engine)
    
    scraper = WikiScraper()
    # Adjust the category name if necessary.
    items_list = scraper.fetch_item_list(category="Category:Items")
    logging.info(f"Fetched {len(items_list)} items from the wiki.")
    
    for item_entry in items_list:
        title = item_entry.get("title")
        # Skip if the item is already in the database.
        existing_item = session.query(Item).filter(Item.name == title).first()
        if existing_item:
            continue
        
        details = scraper.fetch_item_details(title)
        if details:
            new_item = Item(
                name=details["name"],
                ingredients=details.get("ingredients"),
                obtaining_method=details.get("obtaining_method")
            )
            session.add(new_item)
            session.commit()
            logging.info(f"Added item: {title}")
        else:
            logging.warning(f"Failed to fetch details for: {title}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
