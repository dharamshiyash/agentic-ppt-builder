from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from agentic_ppt_builder.state import AgentState
from agentic_ppt_builder.utils.image_fetcher import fetch_image_url
from agentic_ppt_builder.utils.logger import get_logger
from agentic_ppt_builder.utils.config import Config

logger = get_logger(__name__)

def image_agent(state: AgentState):
    logger.info("--- IMAGE AGENT STARTED ---")
    slides = state.get('slide_content', [])
    
    if not slides:
        logger.warning("No slides to process in Image Agent.")
        return {"slide_content": []}
    
    # We can process slides in parallel or batch. simpler to loop for now or simple llm call.
    # Let's do a simple loop since LangChain invocation overhead is small vs stability.
    # OR better: Ask LLM to generate keywords for ALL slides in one go.
    
    llm = ChatGroq(model=Config.LLM_MODEL, temperature=0.5)

    prompt = ChatPromptTemplate.from_template(
        """
        You are a visual design assistant.
        For the following slide, provide a SINGLE specific search keyword or short phrase (2-3 words) to find a relevant high-quality stock image.
        Return ONLY the keyword. No quotes.

        Slide Title: {title}
        Slide Content: {content}
        """
    )
    
    chain = prompt | llm | StrOutputParser()

    updated_slides = []
    
    for slide in slides:
        try:
            keyword = chain.invoke({"title": slide['title'], "content": slide['content']})
            keyword = keyword.strip()
            logger.info(f"Generated Keyword for '{slide['title']}': {keyword}")
            
            url = fetch_image_url(keyword)
            
            # Create new dict to update
            new_slide = slide.copy()
            new_slide['image_keyword'] = keyword
            new_slide['image_url'] = url
            updated_slides.append(new_slide)
            
        except Exception as e:
            logger.error(f"Image Agent Error for slide {slide['title']}: {e}", exc_info=False)
            updated_slides.append(slide)

    return {"slide_content": updated_slides}
