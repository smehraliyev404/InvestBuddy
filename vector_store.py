"""
Vector Store for ETF Knowledge Base
Simple semantic search using sentence-transformers (no ChromaDB needed)
"""

from sentence_transformers import SentenceTransformer, util
from etf_knowledge import ETF_KNOWLEDGE_BASE
import torch
import pickle
import os

class ETFVectorStore:
    """Simple vector store for ETF semantic search"""

    # Initialize the embedding model
    def __init__(self, cache_file="./etf_embeddings.pkl"):
        """Initialize vector store with embedding model"""
        print("🔄 Initializing ETF Vector Store...")

        # Initialize sentence transformer model (fast and efficient)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.cache_file = cache_file

        # Storage for embeddings and metadata
        self.documents = []
        self.embeddings = None
        self.metadata = []

        # Load or create embeddings
        if os.path.exists(cache_file):
            self._load_embeddings()
        else:
            self._create_embeddings()

    # Create embeddings for all ETFs
    def _create_embeddings(self):
        """Create embeddings for all ETF knowledge"""
        print("📚 Creating embeddings for ETF knowledge...")

        for symbol, info in ETF_KNOWLEDGE_BASE.items():
            # Create rich text for embedding - includes all searchable content
            doc_text = f"""
            Symbol: {symbol}
            Name: {info['name']}
            Simple Name: {info['simple_name']}
            Category: {info['category']}
            Risk Level: {info['risk_level']}
            Beginner Explanation: {info['beginner_explanation']}
            Good For: {info['good_for']}
            Why Beginners Love It: {info['why_beginners_love_it']}
            Real World Example: {info['real_world_example']}
            """

            self.documents.append(doc_text.strip())
            self.metadata.append({
                'symbol': symbol,
                'name': info['name'],
                'simple_name': info['simple_name'],
                'category': info['category'],
                'risk_level': info['risk_level'],
                'expense_ratio': info['expense_ratio']
            })

        # Generate embeddings
        self.embeddings = self.embedding_model.encode(
            self.documents,
            convert_to_tensor=True,
            show_progress_bar=True
        )

        # Save to cache
        self._save_embeddings()
        print(f"✅ Created embeddings for {len(self.documents)} ETFs")

    # Save embeddings to disk
    def _save_embeddings(self):
        """Save embeddings to cache file"""
        with open(self.cache_file, 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'embeddings': self.embeddings,
                'metadata': self.metadata
            }, f)
        print(f"💾 Saved embeddings to {self.cache_file}")

    # Load embeddings from disk
    def _load_embeddings(self):
        """Load embeddings from cache file"""
        with open(self.cache_file, 'rb') as f:
            data = pickle.load(f)
            self.documents = data['documents']
            self.embeddings = data['embeddings']
            self.metadata = data['metadata']
        print(f"✅ Loaded {len(self.documents)} ETF embeddings from cache")

    # Semantic search for ETFs
    def search(self, query, n_results=5):
        """
        Semantic search for ETFs based on natural language query

        Args:
            query: Natural language question or description
            n_results: Number of results to return

        Returns:
            List of relevant ETFs with metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query, convert_to_tensor=True)

        # Calculate cosine similarities
        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]

        # Get top results
        top_results = torch.topk(cos_scores, k=min(n_results, len(cos_scores)))

        # Format results
        formatted_results = []
        for score, idx in zip(top_results[0], top_results[1]):
            symbol = self.metadata[idx]['symbol']
            formatted_results.append({
                'symbol': symbol,
                'metadata': self.metadata[idx],
                'relevance_score': float(score),
                'full_info': ETF_KNOWLEDGE_BASE.get(symbol, {})
            })

        return formatted_results

    # Get context for AI chat
    def get_context_for_query(self, query, n_results=3, include_live_data=True):
        """
        Get relevant ETF context for AI to use in chat responses

        Args:
            query: User's question or message
            n_results: Number of ETFs to retrieve
            include_live_data: Whether to fetch and include live market data

        Returns:
            Formatted context string for AI
        """
        results = self.search(query, n_results=n_results)

        if not results:
            return ""

        context_parts = ["Here are some relevant ETFs that might help answer the user's question:\n"]

        for result in results:
            symbol = result['symbol']
            info = result['full_info']

            # Start with beginner-friendly info
            context_part = f"""
**{symbol} - {info['simple_name']}**
- Category: {info['category']}
- Risk: {info['risk_level']}
- Explanation: {info['beginner_explanation']}
- Good for: {info['good_for']}
- Why beginners love it: {info['why_beginners_love_it']}
- Example: {info['real_world_example']}
"""

            # Add live market data if requested
            if include_live_data:
                try:
                    from live_etf_data import get_live_etf_data, format_live_data_for_ai
                    live_data = get_live_etf_data(symbol)
                    live_info = format_live_data_for_ai(symbol, live_data)
                    context_part += f"\n{live_info}\n"
                except Exception as e:
                    print(f"Warning: Could not fetch live data for {symbol}: {e}")

            context_parts.append(context_part)

        return "\n".join(context_parts)


# Global vector store instance
_vector_store = None

# Get or create vector store instance
def get_vector_store():
    """Get or create global vector store instance"""
    global _vector_store
    if _vector_store is None:
        _vector_store = ETFVectorStore()
    return _vector_store

# Search ETFs by query
def search_etfs(query, n_results=5):
    """
    Search for ETFs using natural language

    Example queries:
        - "I want safe investments for retirement"
        - "Which ETFs focus on technology?"
        - "What's good for beginners with low risk?"
        - "I want to invest in sustainable companies"
    """
    store = get_vector_store()
    return store.search(query, n_results=n_results)

# Get AI context for user query
def get_ai_context(user_message, n_results=3, include_live_data=True):
    """
    Get relevant ETF knowledge to enhance AI responses
    Includes both beginner-friendly explanations AND live market data

    This is used behind the scenes to make the AI smarter

    Args:
        user_message: User's question or message
        n_results: Number of relevant ETFs to retrieve
        include_live_data: Whether to include current market data (default: True)

    Returns:
        Formatted context with educational info + live market data
    """
    store = get_vector_store()
    return store.get_context_for_query(user_message, n_results=n_results, include_live_data=include_live_data)


if __name__ == "__main__":
    # Test the vector store
    print("\n" + "="*60)
    print("Testing ETF Vector Store")
    print("="*60 + "\n")

    # Initialize
    store = get_vector_store()

    # Test queries
    test_queries = [
        "I want safe investments with low risk",
        "Which ETFs are good for technology companies?",
        "I'm a beginner and don't know where to start",
        "I want to invest in sustainable and responsible companies",
    ]

    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 60)
        results = search_etfs(query, n_results=3)

        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['symbol']} - {result['metadata']['simple_name']}")
            print(f"   Category: {result['metadata']['category']}")
            print(f"   Risk: {result['metadata']['risk_level']}")
            print(f"   Relevance: {result['relevance_score']:.2%}")

    print("\n" + "="*60)
    print("✅ Vector Store Test Complete!")
    print("="*60 + "\n")
