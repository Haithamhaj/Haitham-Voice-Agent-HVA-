"""
Tests for Email LLM Helpers
"""

import pytest
import asyncio
from haitham_voice_agent.tools.gmail.llm_helper import get_email_llm_helpers


# Test data
TEST_EMAIL = """
Hi Team,

I wanted to follow up on the Q4 project timeline we discussed in yesterday's meeting.

Action Items:
1. Sarah - Complete the design mockups by Friday, December 1st
2. Mike - Review and update the API documentation by next Monday
3. Everyone - Please review the requirements doc I sent earlier

We also need to schedule a client meeting for next Tuesday at 2 PM to present our progress.

Let me know if you have any questions or concerns.

Best regards,
John Smith
Project Manager
"""

TEST_THREAD = [
    {
        "from": "john@example.com",
        "date": "2024-11-20",
        "body": "Hi team, we need to finalize the project scope by Friday."
    },
    {
        "from": "sarah@example.com",
        "date": "2024-11-21",
        "body": "I can have the design ready by Thursday. Mike, can you review?"
    },
    {
        "from": "mike@example.com",
        "date": "2024-11-22",
        "body": "Yes, I'll review on Thursday evening and provide feedback Friday morning."
    }
]


from unittest.mock import AsyncMock, MagicMock, patch
from haitham_voice_agent.tools.gmail.llm_helper import get_email_llm_helpers


@pytest.fixture
def llm_helpers():
    """Get EmailLLMHelpers instance with mocked router"""
    helpers = get_email_llm_helpers()
    
    # Mock the router methods
    helpers.router.generate_with_gemini = AsyncMock()
    helpers.router.generate_with_gpt = AsyncMock()
    
    # Setup default mock returns
    helpers.router.generate_with_gemini.return_value = "Mocked Gemini Summary"
    helpers.router.generate_with_gpt.return_value = "Mocked GPT Reply"
    
    return helpers


# ==================== SUMMARIZATION TESTS ====================

@pytest.mark.asyncio
async def test_summarize_email_wrapper(llm_helpers):
    """Test unified summarize_email wrapper"""
    email_obj = {
        "subject": "Project Timeline",
        "from": "john@example.com",
        "body_text": TEST_EMAIL
    }
    
    # Setup mock
    llm_helpers.router.generate_with_gemini.return_value = "Mocked Gemini Summary"
    
    result = await llm_helpers.summarize_email(email_obj)
    
    assert not result.get("error")
    assert "summary" in result
    assert result["model"] == "gemini"
    assert result["summary"] == "Mocked Gemini Summary"
    
    print(f"\n✓ Wrapper Summary: {result['summary'][:100]}...")


@pytest.mark.asyncio
async def test_summarize_email_basic(llm_helpers):
    """Test basic email summarization"""
    llm_helpers.router.generate_with_gemini.return_value = "Mocked Gemini Summary"
    
    result = await llm_helpers.summarize_email_content(TEST_EMAIL)
    
    assert not result.get("error")
    assert "summary" in result
    assert result["model"] == "gemini"
    assert result["summary"] == "Mocked Gemini Summary"
    
    print(f"\n✓ Basic Summary: {result['summary'][:100]}...")


@pytest.mark.asyncio
async def test_summarize_email_detailed(llm_helpers):
    """Test detailed email summarization"""
    llm_helpers.router.generate_with_gemini.return_value = "Detailed Mocked Summary"
    
    result = await llm_helpers.summarize_email_content(TEST_EMAIL, detailed=True)
    
    assert not result.get("error")
    assert "summary" in result
    assert result["model"] == "gemini"
    assert result["detailed"] is True
    assert result["summary"] == "Detailed Mocked Summary"
    
    print(f"\n✓ Detailed Summary generated")


@pytest.mark.asyncio
async def test_summarize_thread(llm_helpers):
    """Test thread summarization"""
    llm_helpers.router.generate_with_gemini.return_value = "Thread Summary"
    
    result = await llm_helpers.summarize_thread(TEST_THREAD)
    
    assert not result.get("error")
    assert "summary" in result
    assert result["model"] == "gemini"
    assert result["message_count"] == 3
    
    print(f"\n✓ Thread Summary: {result['summary'][:100]}...")


# ==================== ACTION EXTRACTION TESTS ====================

@pytest.mark.asyncio
async def test_extract_actions(llm_helpers):
    """Test action item extraction"""
    llm_helpers.router.generate_with_gemini.return_value = "1. Sarah: Design\n2. Mike: API"
    
    result = await llm_helpers.extract_email_actions(TEST_EMAIL)
    
    assert not result.get("error")
    assert "actions" in result
    assert result["model"] == "gemini"
    assert result["has_actions"] is True
    
    print(f"\n✓ Actions extracted: {result['has_actions']}")


@pytest.mark.asyncio
async def test_extract_actions_none(llm_helpers):
    """Test action extraction with no actions"""
    llm_helpers.router.generate_with_gemini.return_value = "No action items found."
    
    no_action_email = "Hi, just wanted to say thanks for the update. Have a great day!"
    
    result = await llm_helpers.extract_email_actions(no_action_email)
    
    assert not result.get("error")
    assert "actions" in result
    # Should detect no actions based on text analysis or LLM return
    # Our implementation checks for "no action" string
    assert result["has_actions"] is False
    
    print(f"\n✓ No actions detected correctly")


@pytest.mark.asyncio
async def test_extract_thread_actions(llm_helpers):
    """Test action extraction from thread"""
    llm_helpers.router.generate_with_gemini.return_value = "Action items from thread"
    
    result = await llm_helpers.extract_thread_actions(TEST_THREAD)
    
    assert not result.get("error")
    assert "actions" in result
    assert result["model"] == "gemini"
    assert result["message_count"] == 3
    
    print(f"\n✓ Thread actions extracted")


# ==================== SMART REPLY TESTS ====================

@pytest.mark.asyncio
async def test_generate_smart_reply_wrapper(llm_helpers):
    """Test unified generate_smart_reply wrapper"""
    llm_helpers.router.generate_with_gpt.return_value = "Yes, let's meet."
    
    result = await llm_helpers.generate_smart_reply(TEST_EMAIL)
    
    assert not result.get("error")
    assert "reply" in result
    assert result["model"] == "gpt"
    assert result["reply"] == "Yes, let's meet."
    
    print(f"\n✓ Wrapper Smart Reply generated")


@pytest.mark.asyncio
async def test_generate_reply_professional(llm_helpers):
    """Test professional reply generation"""
    llm_helpers.router.generate_with_gpt.return_value = "Professional reply."
    
    result = await llm_helpers.generate_reply_suggestion(
        from_email="john@example.com",
        subject="Project Timeline",
        body=TEST_EMAIL,
        style="professional",
        tone="neutral"
    )
    
    assert not result.get("error")
    assert "reply" in result
    assert result["model"] == "gpt"
    assert result["style"] == "professional"
    assert result["tone"] == "neutral"
    assert result["reply"] == "Professional reply."
    
    print(f"\n✓ Professional reply generated")


@pytest.mark.asyncio
async def test_generate_reply_styles(llm_helpers):
    """Test different reply styles"""
    styles = ["professional", "casual", "brief"]
    llm_helpers.router.generate_with_gpt.return_value = "Styled reply."
    
    for style in styles:
        result = await llm_helpers.generate_reply_suggestion(
            from_email="test@example.com",
            subject="Test",
            body="Quick question about the project.",
            style=style,
            tone="neutral"
        )
        
        assert not result.get("error"), f"Failed for style: {style}"
        assert result["style"] == style
        
        print(f"\n✓ {style.capitalize()} reply generated")


@pytest.mark.asyncio
async def test_generate_reply_types(llm_helpers):
    """Test different reply types"""
    reply_types = ["accept", "decline", "acknowledge"]
    llm_helpers.router.generate_with_gpt.return_value = "Typed reply."
    
    for reply_type in reply_types:
        result = await llm_helpers.generate_reply_suggestion(
            from_email="test@example.com",
            subject="Meeting Invitation",
            body="Would you like to join our meeting on Friday?",
            reply_type=reply_type
        )
        
        assert not result.get("error"), f"Failed for type: {reply_type}"
        assert result["reply_type"] == reply_type
        
        print(f"\n✓ {reply_type.capitalize()} reply generated")


# ==================== TRANSLATION TESTS ====================

@pytest.mark.asyncio
async def test_translate_to_arabic(llm_helpers):
    """Test translation to Arabic"""
    english_text = "Hello, how are you? I hope you are doing well."
    llm_helpers.router.generate_with_gemini.return_value = "مرحبا، كيف حالك؟"
    
    result = await llm_helpers.translate_email_content(english_text, "ar")
    
    assert not result.get("error")
    assert "translated_text" in result
    assert result["model"] == "gemini"
    assert result["target_language"] == "ar"
    assert result["language_name"] == "Arabic"
    assert result["translated_text"] == "مرحبا، كيف حالك؟"
    
    print(f"\n✓ Translated to Arabic")


@pytest.mark.asyncio
async def test_translate_to_spanish(llm_helpers):
    """Test translation to Spanish"""
    english_text = "Thank you for your email. I will review it soon."
    llm_helpers.router.generate_with_gemini.return_value = "Gracias por su correo."
    
    result = await llm_helpers.translate_email_content(english_text, "es")
    
    assert not result.get("error")
    assert result["target_language"] == "es"
    assert result["language_name"] == "Spanish"
    
    print(f"\n✓ Translated to Spanish")


# ==================== SENTIMENT ANALYSIS TESTS ====================

@pytest.mark.asyncio
async def test_analyze_sentiment(llm_helpers):
    """Test sentiment analysis"""
    llm_helpers.router.generate_with_gemini.return_value = "Positive sentiment."
    
    result = await llm_helpers.analyze_email_sentiment(TEST_EMAIL)
    
    assert not result.get("error")
    assert "analysis" in result
    assert result["model"] == "gemini"
    assert result["analysis"] == "Positive sentiment."
    
    print(f"\n✓ Sentiment analyzed")


@pytest.mark.asyncio
async def test_analyze_sentiment_positive(llm_helpers):
    """Test sentiment analysis on positive email"""
    positive_email = "Thank you so much! This is exactly what we needed. Great work!"
    llm_helpers.router.generate_with_gemini.return_value = "Very Positive"
    
    result = await llm_helpers.analyze_email_sentiment(positive_email)
    
    assert not result.get("error")
    # Should detect positive sentiment
    analysis_lower = result["analysis"].lower()
    assert "positive" in analysis_lower
    
    print(f"\n✓ Positive sentiment detected")


@pytest.mark.asyncio
async def test_analyze_sentiment_urgent(llm_helpers):
    """Test sentiment analysis on urgent email"""
    urgent_email = "URGENT: We need this completed by end of day today!"
    llm_helpers.router.generate_with_gemini.return_value = "Urgent priority"
    
    result = await llm_helpers.analyze_email_sentiment(urgent_email)
    
    assert not result.get("error")
    # Should detect urgency
    analysis_lower = result["analysis"].lower()
    assert "urgent" in analysis_lower
    
    print(f"\n✓ Urgency detected")


# ==================== ERROR HANDLING TESTS ====================

@pytest.mark.asyncio
async def test_empty_email_handling(llm_helpers):
    """Test handling of empty email"""
    result = await llm_helpers.summarize_email_content("")
    
    # Should handle gracefully (either error or empty summary)
    assert "summary" in result or "error" in result
    
    print(f"\n✓ Empty email handled")


@pytest.mark.asyncio
async def test_very_long_email(llm_helpers):
    """Test handling of very long email"""
    long_email = "This is a test email. " * 1000  # Very long email
    llm_helpers.router.generate_with_gemini.return_value = "Summary of long email"
    
    result = await llm_helpers.summarize_email_content(long_email)
    
    assert not result.get("error")
    assert "summary" in result
    assert result["summary"] == "Summary of long email"
    
    print(f"\n✓ Long email summarized")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
