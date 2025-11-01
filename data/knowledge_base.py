import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from utils.logger import logger


class RealEstateKnowledgeBase:
    """Manages real estate data from CSV using vector embeddings for retrieval"""
    
    def __init__(self, csv_file, embedding_model="all-MiniLM-L6-v2"):
        """
        Initialize the knowledge base
        
        Args:
            csv_file: Path to CSV file with property data
            embedding_model: Model to use for embeddings
        """
        logger.info(f"Loading real estate knowledge base from {csv_file}...")
        self.csv_file = csv_file
        self.model = SentenceTransformer(embedding_model)
        self.client = self._init_chromadb()
        self.collection = self._init_collection()
        self._load_csv_data()
        logger.info("Knowledge base loaded successfully!")
    
    def _init_chromadb(self):
        """Initialize ChromaDB client"""
        return chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
    
    def _init_collection(self):
        """Initialize or get ChromaDB collection"""
        try:
            return self.client.create_collection("real_estate")
        except Exception as e:
            logger.warning(f"Collection exists, recreating: {e}")
            self.client.delete_collection("real_estate")
            return self.client.create_collection("real_estate")
    
    def _load_csv_data(self):
        """Load real estate data from CSV and create embeddings"""
        if not os.path.exists(self.csv_file):
            logger.error(f"CSV file '{self.csv_file}' not found!")
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
        
        try:
            df = pd.read_csv(self.csv_file)
            
            for idx, row in df.iterrows():
                prop_text = self._format_property(row)
                self.collection.add(
                    documents=[prop_text],
                    ids=[f"property_{idx}"],
                    metadatas={
                        "name": str(row.get('Name', '')),
                        "price": str(row.get('Price', '')),
                        "location": str(row.get('Location', ''))
                    }
                )
            
            logger.info(f"Loaded {len(df)} properties from CSV")
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise
    
    def _format_property(self, row):
        """Format a CSV row into a readable text description"""
        parts = []
        
        columns_map = {
            'Name': 'Property Name',
            'Property Title': 'Title',
            'Price': 'Price',
            'Location': 'Location',
            'Total_Area': 'Total Area',
            'Price_per_SQFT': 'Price per SQFT',
            'Baths': 'Bathrooms',
            'Balcony': 'Balconies',
            'Description': 'Description'
        }
        
        for csv_col, display_name in columns_map.items():
            if pd.notna(row.get(csv_col)):
                parts.append(f"{display_name}: {row[csv_col]}")
        
        return "\n".join(parts)
    
    def search(self, query, n_results=3):
        """
        Search for relevant properties based on query
        
        Args:
            query: Search query from user
            n_results: Number of results to return
            
        Returns:
            Formatted string with relevant properties
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if results['documents']:
                return "\n\n---\n\n".join(results['documents'][0])
            return "No relevant properties found."
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return "Error searching database"
