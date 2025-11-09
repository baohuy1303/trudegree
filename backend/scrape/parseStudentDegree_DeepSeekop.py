import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from enum import Enum
from typing import List, Optional
import json
import re
from timeit import default_timer as timer

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4o", temperature=0.0)

def clean_pdf_text(text : str) -> str:
    """Clean PDF text to reduce tokens"""
    # Remove excessive whitespace
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)
    
    # Remove common boilerplate
    boilerplate_patterns = [
        r'Page \d+ of \d+',
        r'Degree Works.*\n',
        r'Printed:.*\n',
        r'Legend:.*?(?=\n\n|\n[A-Z])',
    ]
    
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, '', text)
    
    return text.strip()


# Your existing Pydantic models remain the same...
class Status(str, Enum):
    COMPLETE = "Complete"
    IN_PROGRESS = "In Progress" 
    INCOMPLETE = "Incomplete"
    
class BlockTitle(str, Enum):
    DEGREE_STATUS = "Degree Status"
    CIVICS_EXAM = "Civics Exam"
    DISCIPLINARY_PERSPECTIVES = "Disciplinary Perspectives"
    COMMUNICATION_SKILLS_PERSPECTIVE = "Communication Skills Perspective"
    SOCIAL_PERSPECTIVE = "Social Perspective"
    STEM_PERSPECTIVE = "STEM Perspective"
    ARTS_HUMANITIES_PERSPECTIVE = "Arts & Humanities Perspective"
    STATISTICS_PERSPECTIVE = "Statistics Perspective"
    INTERCONNECTING_PERSPECTIVES = "Interconnecting Perspectives"
    FIRST_YEAR_SEMINAR = "First Year Seminar / Experience"
    MISSOURI_STATUTE = "Missouri Statute Requirement"
    REQUIRED_SUPPORT = "Required Support & BS Requirements: CS"
    MAJOR_CS = "Major: Computer Science (BS)"
    MINOR_DS = "Minor: Data Science"
    UPPER_LEVEL = "40 Credits in Upper Level Course Requirement"
    FREE_ELECTIVES = "Free Electives"
    IN_PROGRESS = "In-progress and Preregistered"

class Course(BaseModel):
    code: str = Field(..., description="Course code, e.g. 'CS 180'")
    title: str = Field(..., description="Full course title, e.g. 'Foundations of Computer Science I'")
    grade: Optional[str] = Field(None, description="Grade achieved in the course (e.g. 'A', 'IP', 'P')")
    credits: Optional[float] = Field(None, description="Number of credits earned for the course")
    term: Optional[str] = Field(None, description="Academic term when the course was taken (e.g. 'Fall 2025')")
    repeated: Optional[bool] = Field(False, description="Whether the course was repeated")

class Requirement(BaseModel):
    name: str = Field(..., description="Specific requirement name (e.g. 'Statistics Course', 'Senior Seminar')")
    status: Status = Field(..., description="Status of the requirement")
    details: Optional[str] = Field(None, description="Text explaining what's still needed or fulfilled")
    required_credits: Optional[float] = Field(None, description="Total credits required for this requirement")
    applied_credits: Optional[float] = Field(None, description="Credits currently applied")
    still_needed_credits: Optional[float] = Field(None, description="Required credits minus applied credits")
    courses: Optional[List[Course]] = Field(default_factory=list, description="List of courses applied toward this requirement")
    is_reference_only: Optional[bool] = Field(False, description="True if this requirement is a reference to another block")

class Block(BaseModel):
    title: str = Field(..., description="Major block title, e.g. 'Major: Computer Science (BS)' or 'Disciplinary Perspectives'")
    status: Status = Field(..., description="Block completion status")
    catalog_year: Optional[str] = Field(None, description="Catalog year this block follows")
    gpa: Optional[float] = Field(None, description="GPA for this block or section if available")
    requirements: List[Requirement] = Field(default_factory=list, description="All requirements in this block. For Disciplinary Perspectives, the requirements will not have courses, the later blocks will handle these courses.")
    description: Optional[str] = Field(None, description="If there is leftover text after parsing the block, or anything unparsable or doesn't fit into the model, it will be stored here")

class DegreeInfo(BaseModel):
    degree: str = Field(..., description="Degree title, e.g. 'Bachelor of Science'")
    program: str = Field(..., description="Program code or shorthand, e.g. 'CS BS'")
    major: str = Field(..., description="Major name, e.g. 'Computer Science'")
    minor: Optional[str] = Field(None, description="Minor name, if applicable")
    college: Optional[str] = Field(None, description="College or school the program belongs to")
    classification: str = Field(..., description="Student level classification, e.g. 'Freshman', 'Senior'")
    level: str = Field(..., description="Academic level, e.g. 'Undergraduate'")
    catalog_year: str = Field(..., description="Catalog year of the student’s degree plan")
    degree_status: str = Field(..., description="Overall degree completion status, e.g. 'Incomplete'")
    required_credits: Optional[float] = Field(None, description="Credits required to graduate")
    applied_credits: Optional[float] = Field(None, description="Credits already applied")
    gpa: Optional[float] = Field(None, description="Overall GPA")

class StudentProfile(BaseModel):
    name: str = Field(..., description="Student full name as listed in DegreeWorks")
    student_id: str = Field(..., description="Masked or full student ID")
    audit_date: str = Field(..., description="Date and time when the degree audit was generated")
    degree_info: DegreeInfo = Field(..., description="Basic student degree and academic info")
    blocks: List[Block] = Field(default_factory=list, description="List of academic blocks (Includes all of these: Degree Status, Civics Exam, Disciplinary Perspectives, Communication Skills Perspective, Social Perspective, STEM Perspective, Arts & Humanities Perspective, Statistics Perspective, Interconnecting Perspectives, First Year Seminar / Experience, Missouri Statute Requirement, Required Support & BS Requirements: CS, Major: Computer Science (BS), Minor: Data Science, 40 Credits in Upper Level Course Requirement, Free Electives, In-progress and Preregistered")
    in_progress_courses: Optional[List[Course]] = Field(default_factory=list, description="Courses currently in progress or preregistered")
    free_electives: Optional[List[Course]] = Field(default_factory=list, description="Free elective courses")
    legend: Optional[str] = Field(None, description="Legend section text, if parsed")

def parse_degreeworks_pdf(pdf_path: str) -> dict:
    """Parse any DegreeWorks PDF and return structured JSON."""

    start = timer()
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    all_content = "\n".join([page.page_content for page in pages])
    cleaned_content = clean_pdf_text(all_content) 

    parser = JsonOutputParser(pydantic_object=StudentProfile)

    prompt = PromptTemplate(
        template=(
            "You are an expert academic record parser that extracts structured data from DegreeWorks audit PDFs.\n"
            "Your goal is to convert the provided text into valid JSON following the DegreeWorksProfile model.\n\n"
            "Instructions:\n"
            "- Identify the student's basic information (name, ID, degree, program, catalog year, classification, GPA, etc.).\n"
            "- Group all sections (like 'Major', 'Minor', 'Disciplinary Perspectives', etc.) as Blocks.\n"
            "- Within each Block, extract all listed Requirements, their status, and associated courses.\n"
            "- For each course, include code, title, grade, credits, term, and if it’s repeated or in-progress.\n"
            "- Preserve the hierarchy: Student → DegreeInfo → Blocks → Requirements → Courses.\n"
            "- If a requirement name exactly matches a block title, do NOT treat it as a requirement. Instead, store it as a reference note (e.g. 'See [BlockTitle] block below') and continue parsing the other blocks normally.\n"
            "- If a requirement name matches a known block title, set 'is_reference_only' to true and add a 'details' note saying 'See [BlockTitle] block below.'\n"
            "- For missing values, return null.\n"
            "- Pay special attention to the `Required Support & Requirements` and `STEM Perspective` blocks, parse all the requirements thoroughly.\n"
            "{format_instructions}\n\n"
            "RAW TEXT TO PARSE:\n{context}"
        ),
        input_variables=["context"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser
    result = chain.invoke({"context": cleaned_content})

    end = timer()
    time_taken = end - start

    print(f"Time taken: {time_taken:.2f} seconds")

    if isinstance(result, str):
        result = json.loads(result)

    return result


"""     output_dir = "parsedDegree"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "gpt4o_optimized-T2.json")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(valid_json_str) """