import os
from typing import Dict, List, Optional
from openai import OpenAI
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    # Fallback for older langchain versions
    from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


class AIAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY", "")
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000, chunk_overlap=200
        )

    async def analyze_document(self, document_text: str, file_path: str) -> Dict:
        """Analyze document using AI"""
        # Split document into chunks
        chunks = self.text_splitter.split_text(document_text)
        
        # Extract key terms
        extracted_terms = await self._extract_terms(document_text)
        
        # Identify risks
        risk_flags = await self._identify_risks(document_text)
        
        # Check for unusual clauses
        unusual_clauses = await self._find_unusual_clauses(document_text)
        
        return {
            "extracted_terms": extracted_terms,
            "risk_flags": risk_flags,
            "unusual_clauses": unusual_clauses,
            "document_length": len(document_text),
            "chunks": len(chunks),
        }

    async def _extract_terms(self, text: str) -> Dict:
        """Extract key loan terms using LLM"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert loan document analyst. Extract key terms from loan documents and return them in JSON format."),
            ("user", """Extract the following information from this loan document:
            
1. Interest rate (if mentioned)
2. Maturity date
3. Principal amount
4. Transfer restrictions (describe any limitations on assignment/transfer)
5. Consent requirements (list parties that require consent for transfer)
6. Financial covenants (list each covenant with its requirement)

Return the results as JSON with these keys: interest_rate, maturity_date, principal_amount, transfer_restrictions, consent_requirements, financial_covenants.

Document text:
{text}
"""),
        ])
        
        try:
            # Use sync invoke for now (can be made async with proper setup)
            chain = prompt | self.llm
            response = chain.invoke({"text": text[:8000]})  # Limit text length
            
            # Parse JSON response
            content = response.content
            # Try to extract JSON from response
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            
            terms = json.loads(content)
            return terms
        except Exception as e:
            print(f"Error extracting terms: {e}")
            # Return default structure
            return {
                "interest_rate": None,
                "maturity_date": None,
                "principal_amount": None,
                "transfer_restrictions": None,
                "consent_requirements": [],
                "financial_covenants": [],
            }

    async def _identify_risks(self, text: str) -> List[Dict]:
        """Identify potential risks in the document"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a risk analyst. Identify potential risks in loan documents."),
            ("user", """Analyze this loan document and identify potential risks. Return a JSON array of risk objects, each with:
- category: string (credit, legal, operational)
- severity: string (high, medium, low)
- description: string
- location: string (section or page reference if available)

Document text:
{text}
"""),
        ])
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({"text": text[:8000]})
            content = response.content
            
            # Extract JSON
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            
            risks = json.loads(content)
            return risks if isinstance(risks, list) else []
        except Exception as e:
            print(f"Error identifying risks: {e}")
            return []

    async def _find_unusual_clauses(self, text: str) -> List[str]:
        """Find unusual or non-standard clauses"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a loan document expert. Identify unusual or non-standard clauses."),
            ("user", """Review this loan document and identify any unusual, non-standard, or potentially problematic clauses. Return a JSON array of strings describing each unusual clause.

Document text:
{text}
"""),
        ])
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({"text": text[:8000]})
            content = response.content
            
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            
            clauses = json.loads(content)
            return clauses if isinstance(clauses, list) else []
        except Exception as e:
            print(f"Error finding unusual clauses: {e}")
            return []

