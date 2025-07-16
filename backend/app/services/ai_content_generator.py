import os
import requests
import json
from typing import Tuple, Optional
from ..core.config import settings
from ..models import EmailData
import logging

logger = logging.getLogger(__name__)

class AIContentGenerator:
    """
    AI-powered content generation using FREE services:
    - Groq (free tier with fast inference)
    - Hugging Face (free inference API)
    - OpenAI (backup if you have credits)
    """
    
    def __init__(self):
        self.service = settings.AI_SERVICE
        logger.info(f"Initializing AI Content Generator with service: {self.service}")
        
        # Initialize the appropriate service
        if self.service == "groq":
            self._init_groq()
        elif self.service == "huggingface":
            self._init_huggingface()
        elif self.service == "openai":
            self._init_openai()
        else:
            logger.warning(f"Unknown AI service: {self.service}, falling back to Groq")
            self.service = "groq"
            self._init_groq()
    
    def _init_groq(self):
        """Initialize Groq client (FREE tier available)"""
        try:
            from groq import Groq
            if not settings.GROQ_API_KEY:
                logger.error("GROQ_API_KEY not found. Get free API key from https://console.groq.com/")
                return
            
            # Initialize Groq client with only the API key (no other parameters)
            self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
            
            # Test the connection with a simple request
            try:
                # Quick test to verify API key works
                test_response = self.groq_client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=5
                )
                logger.info("✅ Groq client initialized and tested successfully")
            except Exception as test_error:
                logger.warning(f"Groq API key may be invalid: {test_error}")
                logger.info("✅ Groq client initialized (API key not tested)")
                
        except ImportError:
            logger.error("Groq library not installed. Run: pip install groq")
        except Exception as e:
            logger.error(f"Failed to initialize Groq: {e}")
            # Set client to None to avoid further errors
            self.groq_client = None
    
    def _init_huggingface(self):
        """Initialize Hugging Face client (FREE)"""
        if not settings.HUGGINGFACE_API_KEY:
            logger.error("HUGGINGFACE_API_KEY not found. Get free token from https://huggingface.co/settings/tokens")
            return
        
        self.hf_headers = {
            "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        # Using Meta's Llama model (free on HF)
        self.hf_model_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
        logger.info("✅ Hugging Face client initialized successfully")
    
    def _init_openai(self):
        """Initialize OpenAI client (backup option)"""
        try:
            import openai
            if not settings.OPENAI_API_KEY:
                logger.error("OPENAI_API_KEY not found")
                return
            self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("✅ OpenAI client initialized successfully")
        except ImportError:
            logger.error("OpenAI library not installed. Run: pip install openai")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI: {e}")
    
    async def generate_email_content(self, context: str, recipient: str) -> Tuple[str, str]:
        """
        Generate professional email subject and body based on context
        
        Args:
            context: The purpose/context of the email (e.g., "leave application for Monday to Wednesday")
            recipient: Email recipient (e.g., "manager@company.com")
        
        Returns:
            Tuple of (subject, body)
        """
        try:
            if self.service == "groq":
                return await self._generate_with_groq(context, recipient)
            elif self.service == "huggingface":
                return await self._generate_with_huggingface(context, recipient)
            elif self.service == "openai":
                return await self._generate_with_openai(context, recipient)
            else:
                return self._generate_fallback_content(context, recipient)
                
        except Exception as e:
            logger.error(f"Failed to generate email content with {self.service}: {e}")
            return self._generate_fallback_content(context, recipient)
    
    async def _generate_with_groq(self, context: str, recipient: str) -> Tuple[str, str]:
        """Generate content using Groq (FREE tier)"""
        try:
            prompt = self._build_email_prompt(context, recipient)
            
            # Use Groq's fastest and most reliable model for email generation
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",  # Fast and reliable model on Groq
                messages=[
                    {"role": "system", "content": "You are a professional email writing assistant. Generate clear, courteous, and well-structured business emails. Always format your response with 'SUBJECT:' followed by the subject line, then 'BODY:' followed by the email body."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.3,  # Lower temperature for more consistent formatting
                top_p=1,
                stream=False
            )
            
            content = response.choices[0].message.content
            logger.info(f"Groq API response received: {len(content)} characters")
            return self._parse_email_response(content, context)
            
        except Exception as e:
            logger.error(f"Groq generation failed: {e}")
            return self._generate_fallback_content(context, recipient)
    
    async def _generate_with_huggingface(self, context: str, recipient: str) -> Tuple[str, str]:
        """Generate content using Hugging Face (FREE)"""
        try:
            prompt = self._build_email_prompt(context, recipient)
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 500,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.hf_model_url,
                headers=self.hf_headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    content = result[0].get("generated_text", "")
                    return self._parse_email_response(content, context)
                else:
                    logger.error(f"Unexpected HuggingFace response format: {result}")
            else:
                logger.error(f"HuggingFace API error: {response.status_code} - {response.text}")
            
            return self._generate_fallback_content(context, recipient)
            
        except Exception as e:
            logger.error(f"HuggingFace generation failed: {e}")
            return self._generate_fallback_content(context, recipient)
    
    async def _generate_with_openai(self, context: str, recipient: str) -> Tuple[str, str]:
        """Generate content using OpenAI (backup option)"""
        try:
            prompt = self._build_email_prompt(context, recipient)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional email writing assistant. Generate clear, courteous, and well-structured business emails."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._parse_email_response(content, context)
            
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            return self._generate_fallback_content(context, recipient)
    
    def _build_email_prompt(self, context: str, recipient: str) -> str:
        """Build the prompt for email generation"""
        return f"""
Generate a professional email with the following details:

Context: {context}
Recipient: {recipient}

Please generate:
1. A clear, professional subject line
2. A well-structured email body that is courteous and professional

The email should be formal but friendly, and include all necessary details.
Format your response exactly as:
SUBJECT: [subject line]
BODY: [email body]
"""
    
    def _parse_email_response(self, content: str, context: str) -> Tuple[str, str]:
        """Parse AI response to extract subject and body"""
        try:
            lines = content.split('\n')
            subject = ""
            body = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith("SUBJECT:"):
                    subject = line.replace("SUBJECT:", "").strip()
                elif line.startswith("BODY:"):
                    body = line.replace("BODY:", "").strip()
                elif body and line:  # Continue building body
                    body += "\n" + line
            
            # Clean up the body
            body = body.strip()
            
            # Fallback parsing if format is different
            if not subject or not body:
                content_lines = [line.strip() for line in content.split('\n') if line.strip()]
                if len(content_lines) >= 2:
                    # Try to identify subject (usually shorter, first line)
                    potential_subject = content_lines[0]
                    if len(potential_subject) < 100:  # Reasonable subject length
                        subject = potential_subject
                        body = '\n'.join(content_lines[1:])
                    else:
                        subject = f"Regarding: {context}"
                        body = '\n'.join(content_lines)
                else:
                    subject = f"Regarding: {context}"
                    body = content.strip()
            
            # Ensure we have reasonable content
            if not subject:
                subject = f"Email regarding: {context}"
            
            if not body:
                body = f"Dear recipient,\n\nI hope this email finds you well.\n\n{context}\n\nThank you for your time and consideration.\n\nBest regards"
            
            logger.info(f"Generated email - Subject: {subject[:50]}...")
            return subject, body
            
        except Exception as e:
            logger.error(f"Failed to parse email response: {e}")
            return self._generate_fallback_content(context, "")
    
    def _generate_fallback_content(self, context: str, recipient: str) -> Tuple[str, str]:
        """Generate fallback content when AI services fail"""
        logger.info("Using fallback email content generation")
        
        # Determine email type and generate appropriate content
        context_lower = context.lower()
        
        if "leave" in context_lower or "vacation" in context_lower:
            subject = f"Leave Application Request"
            body = f"""Dear Manager,

I hope this email finds you well.

I would like to formally request time off for {context}.

I will ensure all my current projects are up to date and will coordinate with my team to handle any urgent matters during my absence.

Please let me know if you need any additional information or if there are any concerns regarding this request.

Thank you for your consideration.

Best regards"""
            
        elif "meeting" in context_lower:
            subject = f"Meeting Request - {context}"
            body = f"""Dear Colleague,

I hope this email finds you well.

I would like to schedule a meeting regarding {context}.

Please let me know your availability so we can coordinate a suitable time for both of us.

Looking forward to our discussion.

Best regards"""
            
        else:
            subject = f"Regarding: {context}"
            body = f"""Dear Recipient,

I hope this email finds you well.

I am writing to you regarding {context}.

Please let me know if you need any additional information or if you have any questions.

Thank you for your time and consideration.

Best regards"""
        
        return subject, body
    
    async def generate_leave_application(self, leave_dates: str, manager_email: str) -> Tuple[str, str]:
        """Generate specific leave application email"""
        context = f"leave application for {leave_dates}"
        return await self.generate_email_content(context, manager_email)
    
    async def generate_meeting_email(self, meeting_details: str, recipient: str) -> Tuple[str, str]:
        """Generate meeting-related email"""
        context = f"meeting regarding {meeting_details}"
        return await self.generate_email_content(context, recipient)
    
    async def generate_general_email(self, purpose: str, recipient: str) -> Tuple[str, str]:
        """Generate general purpose email"""
        return await self.generate_email_content(purpose, recipient)
