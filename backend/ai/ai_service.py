"""
Smart Multi-AI Service
Uses the BEST FREE AI for each task:
- Groq: Main chat, fast responses (FREE, unlimited)
- Google Gemini: Complex reasoning, long context (FREE, 60 req/min)
- Local embeddings: Semantic search (FREE, runs locally)
"""

from groq import Groq
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import asyncio
from backend.app.config import settings
import json

class MultiAIService:
    """
    Intelligent AI service that uses the best FREE AI for each task
    """
    
    def __init__(self):
        # Groq - Main chat AI (FREE, unlimited, FAST!)
        self.groq = Groq(api_key=settings.GROQ_API_KEY)
        self.groq_model = "mixtral-8x7b-32768"  # Best balance
        
        # Google Gemini - Complex reasoning (FREE, 60/min)
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.gemini = genai.GenerativeModel('gemini-pro')
        
        # Local embeddings - Semantic search (FREE, runs locally)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        print("✅ Multi-AI Service initialized (100% FREE!)")
    
    # ============================================
    # GROQ AI - Fast Chat & Quick Tasks
    # ============================================
    
    async def chat(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7
    ) -> Dict:
        """
        Fast chat using Groq (sub-second responses!)
        Perfect for: General chat, quick questions, commands
        """
        try:
            response = self.groq.chat.completions.create(
                model=self.groq_model,
                messages=messages,
                temperature=temperature,
                max_tokens=2048,
                top_p=1,
                stream=False
            )
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model": "groq-mixtral",
                "tokens": response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
        except Exception as e:
            print(f"Groq error: {e}")
            return {
                "success": False,
                "content": "I'm having trouble responding right now. Please try again.",
                "error": str(e)
            }
    
    async def quick_summarize(self, text: str, max_words: int = 100) -> str:
        """
        Fast summarization with Groq
        Perfect for: Notes, files, articles
        """
        messages = [
            {
                "role": "system",
                "content": "You create concise, accurate summaries. Be brief and clear."
            },
            {
                "role": "user",
                "content": f"Summarize in {max_words} words:\n\n{text}"
            }
        ]
        result = await self.chat(messages, temperature=0.3)
        return result.get("content", "Summary unavailable")
    
    async def auto_categorize(
        self, 
        text: str, 
        categories: List[str]
    ) -> str:
        """
        Auto-categorize content with Groq
        Perfect for: Notes, files, tasks
        """
        messages = [
            {
                "role": "system",
                "content": f"Categorize content into ONE of these: {', '.join(categories)}. Reply with ONLY the category name."
            },
            {
                "role": "user",
                "content": text[:500]  # First 500 chars
            }
        ]
        result = await self.chat(messages, temperature=0.2)
        content = result.get("content", categories[0]).strip()
        
        # Return the category if it matches, otherwise first category
        for cat in categories:
            if cat.lower() in content.lower():
                return cat
        return categories[0]
    
    async def extract_tags(self, text: str, max_tags: int = 5) -> List[str]:
        """
        Extract relevant tags with Groq
        Perfect for: Notes, files
        """
        messages = [
            {
                "role": "system",
                "content": f"Extract {max_tags} relevant tags. Reply with comma-separated tags only."
            },
            {
                "role": "user",
                "content": text[:500]
            }
        ]
        result = await self.chat(messages, temperature=0.3)
        content = result.get("content", "")
        return [tag.strip() for tag in content.split(",")[:max_tags]]
    
    # ============================================
    # GEMINI PRO - Complex Reasoning
    # ============================================
    
    async def complex_analysis(self, prompt: str, data: Dict) -> Dict:
        """
        Complex analysis with Gemini Pro
        Perfect for: Analytics, insights, planning
        """
        try:
            full_prompt = f"{prompt}\n\nData:\n{json.dumps(data, indent=2)}"
            response = await asyncio.to_thread(
                self.gemini.generate_content,
                full_prompt
            )
            
            return {
                "success": True,
                "content": response.text,
                "model": "gemini-pro"
            }
        except Exception as e:
            print(f"Gemini error: {e}")
            # Fallback to Groq
            return await self.chat([
                {"role": "system", "content": "You are an analytical assistant."},
                {"role": "user", "content": f"{prompt}\n\n{json.dumps(data)}"}
            ])
    
    async def productivity_insights(self, user_data: Dict) -> Dict:
        """
        Generate deep productivity insights
        Uses: Gemini Pro for complex reasoning
        """
        prompt = """
        Analyze this user's productivity data and provide:
        1. Key productivity patterns
        2. Strengths and weaknesses
        3. Specific actionable recommendations
        4. Weekly improvement plan
        5. Motivational message
        
        Be specific, actionable, and encouraging.
        Respond in JSON format with sections: patterns, strengths, weaknesses, recommendations, plan, message
        """
        return await self.complex_analysis(prompt, user_data)
    
    async def smart_schedule(self, tasks: List[Dict], constraints: Dict) -> Dict:
        """
        AI-powered task scheduling
        Uses: Gemini Pro for optimization
        """
        prompt = """
        Optimize this task schedule considering:
        - Task priorities (1-5)
        - Deadlines
        - Estimated durations
        - User's working hours
        - Energy levels throughout day
        
        Create an optimal schedule that:
        1. Prioritizes urgent/important tasks
        2. Balances workload
        3. Respects energy patterns
        4. Avoids overwhelm
        
        Return JSON with: optimized_schedule, reasoning, tips
        """
        data = {
            "tasks": tasks,
            "constraints": constraints
        }
        return await self.complex_analysis(prompt, data)
    
    # ============================================
    # LOCAL EMBEDDINGS - Semantic Search
    # ============================================
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding vector for semantic search
        100% FREE, runs locally, no API calls!
        """
        embedding = self.embedder.encode(text)
        return embedding.tolist()
    
    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple texts at once
        More efficient for bulk operations
        """
        embeddings = self.embedder.encode(texts)
        return [emb.tolist() for emb in embeddings]
    
    def similarity_search(
        self, 
        query: str, 
        documents: List[Dict],
        top_k: int = 5
    ) -> List[Dict]:
        """
        Find most similar documents to query
        Perfect for: Searching notes, files, tasks
        """
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        
        # Create query embedding
        query_emb = self.create_embedding(query)
        
        # Get document embeddings
        doc_embeddings = [doc['embedding'] for doc in documents]
        
        # Calculate similarities
        similarities = cosine_similarity(
            [query_emb], 
            doc_embeddings
        )[0]
        
        # Get top k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                **documents[idx],
                'similarity': float(similarities[idx])
            })
        
        return results
    
    # ============================================
    # SMART ROUTING - Auto-select best AI
    # ============================================
    
    async def smart_response(
        self, 
        user_message: str, 
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Intelligently route to best AI based on task
        """
        message_lower = user_message.lower()
        
        # Simple/fast queries → Groq
        if any(word in message_lower for word in ['what', 'who', 'when', 'where', 'how', 'quick']):
            return await self.chat([
                {"role": "user", "content": user_message}
            ])
        
        # Complex analysis → Gemini
        if any(word in message_lower for word in ['analyze', 'compare', 'evaluate', 'insights', 'recommend']):
            return await self.complex_analysis(user_message, context or {})
        
        # Default → Groq (fastest)
        return await self.chat([
            {"role": "user", "content": user_message}
        ])
    
    # ============================================
    # STREAMING RESPONSES
    # ============================================
    
    async def stream_chat(self, messages: List[Dict[str, str]]):
        """
        Stream responses in real-time (for better UX)
        Uses: Groq for ultra-fast streaming
        """
        try:
            stream = self.groq.chat.completions.create(
                model=self.groq_model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Error: {str(e)}"

# ============================================
# SINGLETON INSTANCE
# ============================================

_ai_service = None

def get_ai_service() -> MultiAIService:
    """Get or create AI service singleton"""
    global _ai_service
    if _ai_service is None:
        _ai_service = MultiAIService()
    return _ai_service

# ============================================
# CONVENIENCE FUNCTIONS
# ============================================

async def chat_with_ai(messages: List[Dict]) -> Dict:
    """Quick chat function"""
    service = get_ai_service()
    return await service.chat(messages)

async def summarize(text: str) -> str:
    """Quick summarize function"""
    service = get_ai_service()
    return await service.quick_summarize(text)

async def categorize(text: str, categories: List[str]) -> str:
    """Quick categorize function"""
    service = get_ai_service()
    return await service.auto_categorize(text, categories)

async def get_tags(text: str) -> List[str]:
    """Quick tag extraction"""
    service = get_ai_service()
    return await service.extract_tags(text)

async def get_insights(user_data: Dict) -> Dict:
    """Get productivity insights"""
    service = get_ai_service()
    return await service.productivity_insights(user_data)

def create_embedding(text: str) -> List[float]:
    """Create embedding for text"""
    service = get_ai_service()
    return service.create_embedding(text)

def search_similar(query: str, documents: List[Dict], top_k: int = 5) -> List[Dict]:
    """Search similar documents"""
    service = get_ai_service()
    return service.similarity_search(query, documents, top_k)