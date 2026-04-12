import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def analyze_resume(resume_data: dict) -> dict:
    """
    Analyzes the resume data using OpenAI API and returns a structured JSON response.
    
    Args:
        resume_data (dict): A dictionary containing 'raw_resume_text' and optionally 'optional_github_data'.
    
    Returns:
        dict: A structured analysis mimicking the format of ai_analysis_example_response.json
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    client = OpenAI(api_key=openai_api_key)
    
    system_prompt = """
    You are an expert technical recruiter and resume analyzer AI.
    Your task is to analyze the provided resume and optional GitHub data, and output a structured JSON response exactly matching the specified schema.
    Do not include any plain text outside the JSON. Return only the JSON object.

    The expected JSON response format must strictly follow this structure:
    {
      "candidate": {
        "name": "string",
        "email": "string",
        "phone": "string",
        "location": "string",
        "work_authorization": "string",
        "links": {
          "linkedin": "string",
          "github": "string",
          "portfolio": "string"
        }
      },
      "summary_analysis": {
        "claimed_seniority": "junior | mid | senior | lead",
        "years_of_experience_claimed": 0,
        "primary_domain": "backend | frontend | fullstack | devops | ml | mobile | unknown",
        "focus_areas": [],
        "confidence": "low | medium | high"
      },
      "skills": {
        "all_skills": [],
        "inferred_depth": {
          "skill_name": "low | medium | high"
        },
        "consistency_score": 0
      },
      "experience": [
        {
          "company": "string",
          "role": "string",
          "start_date": "YYYY-MM",
          "end_date": "YYYY-MM | present",
          "duration_months": 0,
          "is_current": true,
          "responsibilities": [],
          "technologies_used": [],
          "impact_metrics": [
            {
              "category": "performance | cost | time | scalability | reliability | productivity",
              "description": "string",
              "raw_value": "string",
              "has_baseline": true,
              "confidence": "low | medium | high"
            }
          ],
          "ownership_level": "low | medium | high",
          "seniority_inferred": "junior | mid | senior"
        }
      ],
      "experience_analysis": {
        "total_roles": 0,
        "total_experience_years_actual": 0,
        "average_role_duration_months": 0,
        "overlapping_roles": true,
        "overlap_details": [],
        "employment_gaps": [
          {
            "start": "YYYY-MM",
            "end": "YYYY-MM",
            "duration_months": 0
          }
        ],
        "career_progression": {
          "title_growth": "weak | moderate | strong",
          "promotion_pattern": "clear | unclear",
          "seniority_acceleration_flag": true
        }
      },
      "impact_analysis": {
        "total_metrics_count": 0,
        "metrics_quality_score": 0,
        "metrics_with_baseline_ratio": 0,
        "metric_types_detected": [],
        "inflated_metrics_flag": true
      },
      "skill_validation": {
        "strongly_supported_skills": [],
        "weakly_supported_skills": [],
        "unsupported_skills": [],
        "skill_mismatch_flag": true
      },
      "github_supporting": {
        "github_profile_summary": "string",
        "supported_skills": [],
        "unsupported_skills": [],
        "consistency_score": 0,
        "supported_resume_claims": [
          {
            "claim": "string",
            "evidence": "string",
            "confidence": "low | medium | high"
          }
        ]
      },
      "system_complexity": {
        "level": "low | medium | high",
        "signals": [],
        "confidence": "low | medium | high"
      },
      "ownership_analysis": {
        "overall_level": "low | medium | high",
        "signals": [],
        "consistency_with_roles": true
      },
      "ambiguities": [
        {
          "type": "metric_without_context | vague_claim | scale_without_evidence | role_unclear | tech_usage_unclear",
          "text": "string",
          "severity": "low | medium | high",
          "suggested_question": "string"
        }
      ],
      "risk_signals": [
        {
          "type": "timeline | seniority | metrics | inconsistency",
          "description": "string",
          "severity": "low | medium | high"
        }
      ],
      "strength_signals": [
        {
          "type": "technical | impact | ownership | consistency",
          "description": "string",
          "confidence": "low | medium | high"
        }
      ],
      "interview_questions": [
        {
          "question": "string",
          "target_area": "architecture | metrics | ownership | timeline | skills",
          "priority": "low | medium | high"
        }
      ],
      "confidence_assessment": {
        "overall_confidence": "low | medium | high",
        "evidence_coverage": 0,
        "key_gaps": []
      }
    }
    """
    
    user_prompt = f"""
    Please analyze the following application data:

    RAW RESUME TEXT:
    {resume_data.get('raw_resume_text', '')}

    OPTIONAL GITHUB DATA:
    {json.dumps(resume_data.get('optional_github_data', {}), indent=2)}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        result_json = response.choices[0].message.content
        data = json.loads(result_json)
        with open("ai_response_pretty.json", "w") as f:
            json.dump(data, f, indent=4)
            
        return data
    except Exception as e:
        logger.error(f"Error during OpenAI AI analysis: {e}")
        raise
