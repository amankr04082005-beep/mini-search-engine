"""Run once to populate the database with a handful of sample documents."""
from database import init_db
from index import add_document, get_all_documents

SAMPLE_DOCS = [
    (
        "Introduction to Python",
        "Python is a high-level, interpreted programming language known for "
        "its readability. It supports multiple paradigms including object "
        "oriented, functional, and procedural programming. Python is widely "
        "used in web development, data science, and automation.",
    ),
    (
        "What is a REST API",
        "A REST API is an architectural style for designing networked "
        "applications. It relies on stateless, client-server communication, "
        "typically using HTTP methods like GET, POST, PUT, and DELETE to "
        "operate on resources identified by URLs.",
    ),
    (
        "Understanding Databases",
        "A database is an organized collection of data stored and accessed "
        "electronically. Relational databases like MySQL and PostgreSQL use "
        "tables and SQL queries, while NoSQL databases like MongoDB store "
        "data as flexible documents.",
    ),
    (
        "Basics of Data Structures",
        "Data structures are ways of organizing data for efficient access "
        "and modification. Common data structures include arrays, linked "
        "lists, stacks, queues, trees, and hash maps. Choosing the right "
        "data structure improves algorithm performance.",
    ),
    (
        "How Search Engines Work",
        "A search engine indexes documents by building an inverted index, "
        "mapping words to the documents that contain them. When a user "
        "submits a query, the engine ranks matching documents using scoring "
        "methods like TF-IDF or more advanced ranking algorithms.",
    ),
    (
        "Introduction to Machine Learning",
        "Machine learning is a field of artificial intelligence where "
        "systems learn patterns from data rather than being explicitly "
        "programmed. Common techniques include supervised learning, "
        "unsupervised learning, and reinforcement learning.",
    ),
    (
        "Web Development with Flask",
        "Flask is a lightweight Python web framework used to build web "
        "applications and APIs. It is minimal by design, giving developers "
        "flexibility to choose their own tools for databases, "
        "authentication, and templating.",
    ),
    (
        "Version Control with Git",
        "Git is a distributed version control system that tracks changes "
        "in source code during software development. It allows multiple "
        "developers to collaborate, branch, and merge code changes "
        "efficiently using repositories hosted on platforms like GitHub.",
    ),
    (
        "Basics of Object Oriented Programming",
        "Object oriented programming organizes software design around "
        "objects rather than functions. Core concepts include "
        "encapsulation, inheritance, polymorphism, and abstraction, which "
        "help build modular and reusable code.",
    ),
    (
        "Introduction to Cloud Computing",
        "Cloud computing delivers computing services like servers, "
        "storage, and databases over the internet. Major providers include "
        "AWS, Azure, and Google Cloud, offering scalable infrastructure "
        "without the need to manage physical hardware.",
    ),
]


def main():
    init_db()
    if get_all_documents():
        print("Documents already exist, skipping seed.")
        return
    for title, content in SAMPLE_DOCS:
        add_document(title, content)
    print(f"Seeded {len(SAMPLE_DOCS)} documents.")


if __name__ == "__main__":
    main()
