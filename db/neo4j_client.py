from neo4j import GraphDatabase, Driver
from dotenv import load_dotenv
import os

load_dotenv()  # Load credentials from .env

NEO4J_URI="neo4j+ssc://99ac5f56.databases.neo4j.io"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="2OOPeeZBMU_ZcaJSB7iyRSvcvuRo1rENZG1mZLtxgxY"
NEO4J_DATABASE="neo4j"

driver: Driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def save_product_to_neo4j(product: dict):
    """Insert or update a product node in the Neo4j graph."""
    query = """
    MERGE (p:Product {name: $name})
    SET p += {
        brand: $brand,
        price: $price,
        discount: $discount,
        availability: $availability,
        rating: $rating,
        review_count: $review_count,
        url: $url,
        category: $category
    }
    """
    params = {
        "name": product["Product Name"],
        "brand": product.get("Brand", ""),
        "price": product.get("Price", ""),
        "discount": product.get("Discount", ""),
        "availability": product.get("Availability", ""),
        "rating": product.get("Rating", ""),
        "review_count": product.get("Review Count", ""),
        "url": product.get("Product URL", ""),
        "category": product.get("Category", "")
    }

    with driver.session(database=NEO4J_DATABASE) as session:
        session.run(query, params)


def run_query(cypher_query: str, parameters: dict = None):
    """Run a Cypher query and return the results as a list of dictionaries."""
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run(cypher_query, parameters or {})
        return [record.data() for record in result]


# Optional: for testing
if __name__ == "__main__":
    product = {
        "Product Name": "Example Product",
        "Brand": "BrandX",
        "Price": "100",
        "Discount": "10%",
        "Availability": "In Stock",
        "Rating": "4.5",
        "Review Count": "100",
        "Product URL": "http://example.com",
        "Category": "CategoryX"
    }
    save_product_to_neo4j(product)
    print("✅ Product saved.")
