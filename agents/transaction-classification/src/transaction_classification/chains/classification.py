"""Classification chain for transaction categorization."""

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from langchain.schema.language_model import BaseLanguageModel
from langchain.schema.runnable import RunnablePassthrough
from pydantic import BaseModel, Field


class ClassificationOutput(BaseModel):
    """Output model for classification chain."""
    
    category: str = Field(..., description="Transaction category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    merchant_name: str = Field(..., description="Normalized merchant name")
    subcategory: str = Field(None, description="Subcategory if applicable")
    tags: list[str] = Field(default_factory=list, description="Additional tags")
    reasoning: str = Field(..., description="Reasoning for classification")


def create_classification_chain(llm: BaseLanguageModel):
    """Create the classification chain.
    
    Args:
        llm: Language model to use
        
    Returns:
        Runnable chain for classification
    """
    parser = PydanticOutputParser(pydantic_object=ClassificationOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a financial transaction classification expert. 
Your task is to categorize transactions based on their description, amount, and date.

Available categories: {categories}

Analyze the transaction and provide:
1. The most appropriate category
2. A confidence score (0.0 to 1.0)
3. The normalized merchant name
4. A subcategory if applicable
5. Any relevant tags
6. Brief reasoning for your classification

{format_instructions}"""),
        ("human", """Classify this transaction:
Description: {description}
Amount: {amount}
Date: {date}"""),
    ])
    
    chain = (
        {"format_instructions": lambda _: parser.get_format_instructions()}
        | prompt
        | llm
        | parser
    )
    
    return chain


def create_merchant_extraction_chain(llm: BaseLanguageModel):
    """Create chain for merchant name extraction and normalization.
    
    Args:
        llm: Language model to use
        
    Returns:
        Runnable chain for merchant extraction
    """
    
    class MerchantOutput(BaseModel):
        """Output for merchant extraction."""
        merchant_name: str = Field(..., description="Normalized merchant name")
        merchant_category: str = Field(..., description="Merchant business category")
        location: str = Field(None, description="Location if available")
    
    parser = PydanticOutputParser(pydantic_object=MerchantOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert at extracting and normalizing merchant names from transaction descriptions.

Extract the merchant name and normalize it by:
1. Removing store numbers and codes
2. Standardizing capitalization
3. Removing unnecessary punctuation
4. Identifying the merchant category

{format_instructions}"""),
        ("human", "Extract merchant from: {description}"),
    ])
    
    chain = (
        {"format_instructions": lambda _: parser.get_format_instructions()}
        | prompt
        | llm
        | parser
    )
    
    return chain