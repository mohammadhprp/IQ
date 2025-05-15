from typing import List, Dict, TypedDict, Annotated, Sequence
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolNode
from app.models.product import Product, AnalysisResponse
from app.core.config import get_settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalysisState(TypedDict):
    """State for the analysis workflow."""

    product_name: str
    product_description: str
    comments_text: str
    rating: float
    summary: str
    fake_comments: List[str]
    keywords: List[str]
    pros: List[str]
    cons: List[str]


class ProductAnalyzer:
    """Analyzes products and their comments using AI."""

    def __init__(self, model_name: str, temperature: float):
        """Initialize the analyzer with the specified model settings."""
        settings = get_settings()
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=settings.GOOGLE_API_KEY,
        )
        self.analysis_graph = self._create_analysis_graph()

    def _log_node_execution(self, node_func):
        """Wrapper function to log state before and after node execution."""

        def wrapper(state: AnalysisState) -> AnalysisState:
            node_name = node_func.__name__
            logger.info(f"Executing node: {node_name}")
            # logger.info(f"Input state for {node_name}: {state}")

            result = node_func(state)

            # logger.info(f"Output state from {node_name}: {result}")
            return result

        return wrapper

    def _create_analysis_graph(self) -> Graph:
        """Create the analysis workflow graph."""
        workflow = StateGraph(AnalysisState)

        # Add nodes with logging wrapper
        workflow.add_node(
            "prepare_comments", self._log_node_execution(self._prepare_comments)
        )
        workflow.add_node(
            "analyze_rating", self._log_node_execution(self._analyze_rating)
        )
        workflow.add_node(
            "generate_summary", self._log_node_execution(self._generate_summary)
        )
        workflow.add_node(
            "detect_fake_comments", self._log_node_execution(self._detect_fake_comments)
        )
        workflow.add_node(
            "extract_keywords", self._log_node_execution(self._extract_keywords)
        )
        workflow.add_node(
            "analyze_pros_cons", self._log_node_execution(self._analyze_pros_cons)
        )

        # Define the edges
        workflow.add_edge("prepare_comments", "analyze_rating")
        workflow.add_edge("analyze_rating", "generate_summary")
        workflow.add_edge("generate_summary", "detect_fake_comments")
        workflow.add_edge("detect_fake_comments", "extract_keywords")
        workflow.add_edge("extract_keywords", "analyze_pros_cons")

        # Set the entry point
        workflow.set_entry_point("prepare_comments")

        return workflow.compile()

    def _prepare_comments(self, state: AnalysisState) -> AnalysisState:
        """Prepare the comments text for analysis."""
        return state

    def _analyze_rating(self, state: AnalysisState) -> AnalysisState:
        """Analyze and rate the product based on comments."""
        rating_prompt = ChatPromptTemplate.from_template(
            """You are an expert product analyst. Analyze the following product comments and provide a rating from 1 to 5.
            Product: {product_name}
            Description: {product_description}
            Comments: {comments_text}
            
            Provide a rating from 1 to 5 based on the sentiment and content of the comments.
            Only respond with the number, nothing else.
            Rating:"""
        )

        rating_chain = rating_prompt | self.llm
        rating_response = rating_chain.invoke(
            {
                "product_name": state["product_name"],
                "product_description": state["product_description"],
                "comments_text": state["comments_text"],
            }
        )

        try:
            rating = float(rating_response.content.strip())
            rating = max(1.0, min(5.0, rating))
        except ValueError:
            rating = 3.0

        return {**state, "rating": rating}

    def _generate_summary(self, state: AnalysisState) -> AnalysisState:
        """Generate a summary of the product comments."""
        summary_prompt = ChatPromptTemplate.from_template(
            """You are an expert product analyst. Create a concise summary of the following product comments.
            Product: {product_name}
            Comments: {comments_text}
            
            Provide a clear and concise summary of the main points from the comments.
            Summary:"""
        )

        summary_chain = summary_prompt | self.llm
        summary_response = summary_chain.invoke(
            {
                "product_name": state["product_name"],
                "comments_text": state["comments_text"],
            }
        )

        return {**state, "summary": summary_response.content.strip()}

    def _detect_fake_comments(self, state: AnalysisState) -> AnalysisState:
        """Detect potentially fake comments."""
        fake_detection_prompt = ChatPromptTemplate.from_template(
            """You are an expert in detecting fake reviews. Analyze the following comments and identify which ones appear to be fake or suspicious.
            Comments: {comments_text}
            
            List only the IDs of suspicious comments, one per line. If no suspicious comments are found, respond with 'None'.
            Suspicious comment IDs:"""
        )

        fake_detection_chain = fake_detection_prompt | self.llm
        fake_comments_response = fake_detection_chain.invoke(
            {"comments_text": state["comments_text"]}
        )

        fake_comments = [
            c.strip()
            for c in fake_comments_response.content.split("\n")
            if c.strip() and c.strip().lower() != "none"
        ]

        return {**state, "fake_comments": fake_comments}

    def _extract_keywords(self, state: AnalysisState) -> AnalysisState:
        """Extract keywords from the comments."""
        keyword_prompt = ChatPromptTemplate.from_template(
            """You are an expert in keyword extraction. Extract the 3 most important keywords from the following product comments.
            Product: {product_name}
            Comments: {comments_text}
            
            List exactly 3 keywords, one per line. Each keyword should be a single word or short phrase.
            Keywords:"""
        )

        keyword_chain = keyword_prompt | self.llm
        keywords_response = keyword_chain.invoke(
            {
                "product_name": state["product_name"],
                "comments_text": state["comments_text"],
            }
        )

        keywords = [
            k.strip() for k in keywords_response.content.split("\n") if k.strip()
        ][:3]

        return {**state, "keywords": keywords}

    def _analyze_pros_cons(self, state: AnalysisState) -> AnalysisState:
        """Analyze and extract pros and cons from the comments."""
        pros_cons_prompt = ChatPromptTemplate.from_template(
            """You are an expert product analyst. Extract the main pros and cons from the following product comments.
            Product: {product_name}
            Comments: {comments_text}
            
            List the pros and cons as separate bullet points. Each point should be concise (max 5 words).
            Format your response exactly like this:
            PROS:
            - [pro1]
            - [pro2]
            - [pro3]
            
            CONS:
            - [con1]
            - [con2]
            - [con3]
            """
        )

        pros_cons_chain = pros_cons_prompt | self.llm
        pros_cons_response = pros_cons_chain.invoke(
            {
                "product_name": state["product_name"],
                "comments_text": state["comments_text"],
            }
        )

        # Parse the response to extract pros and cons
        response_text = pros_cons_response.content.strip()
        pros_section = response_text.split("PROS:")[1].split("CONS:")[0].strip()
        cons_section = response_text.split("CONS:")[1].strip()

        pros = [p.strip("- ").strip() for p in pros_section.split("\n") if p.strip()]
        cons = [c.strip("- ").strip() for c in cons_section.split("\n") if c.strip()]

        return {**state, "pros": pros, "cons": cons}

    def analyze_product(self, product: Product) -> AnalysisResponse:
        """
        Analyze a product and its comments.

        Args:
            product: The product to analyze

        Returns:
            AnalysisResponse containing the analysis results
        """
        # Prepare initial state
        initial_state = {
            "product_name": product.name,
            "product_description": product.description,
            "comments_text": "\n".join(
                [f"Comment {c.id}: {c.text}" for c in product.comments]
            ),
            "rating": 0.0,
            "summary": "",
            "fake_comments": [],
            "keywords": [],
            "pros": [],
            "cons": [],
        }

        # Run the analysis graph
        final_state = self.analysis_graph.invoke(initial_state)

        # Create and return the response
        return AnalysisResponse(
            rating=final_state["rating"],
            summary=final_state["summary"],
            fake_comments=final_state["fake_comments"],
            keywords=final_state["keywords"],
            pros=final_state["pros"],
            cons=final_state["cons"],
        )
