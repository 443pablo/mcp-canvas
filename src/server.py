#!/usr/bin/env python3
import os
import httpx
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("Canvas LMS MCP Server")

# Canvas API Configuration
CANVAS_API_URL = os.environ.get("CANVAS_API_URL", "")
CANVAS_API_TOKEN = os.environ.get("CANVAS_API_TOKEN", "")

def get_headers() -> dict:
    """Get headers for Canvas API requests."""
    if not CANVAS_API_TOKEN:
        raise ValueError("CANVAS_API_TOKEN environment variable is not set")
    return {
        "Authorization": f"Bearer {CANVAS_API_TOKEN}",
        "Content-Type": "application/json"
    }

async def make_canvas_request(
    method: str, 
    endpoint: str, 
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None
) -> Any:
    """Make a request to Canvas API."""
    url = f"{CANVAS_API_URL}/{endpoint}"
    headers = get_headers()
    
    async with httpx.AsyncClient() as client:
        if method.upper() == "GET":
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
        elif method.upper() == "POST":
            response = await client.post(url, headers=headers, json=data, params=params, timeout=30.0)
        elif method.upper() == "PUT":
            response = await client.put(url, headers=headers, json=data, params=params, timeout=30.0)
        elif method.upper() == "DELETE":
            response = await client.delete(url, headers=headers, timeout=30.0)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        
        # Handle empty responses
        if response.status_code == 204:
            return {"success": True}
        
        return response.json()

# ===== COURSE MANAGEMENT TOOLS =====

@mcp.tool(description="List all courses the current user is enrolled in. Returns course ID, name, course code, enrollment status, and term.")
async def list_courses(
    enrollment_state: str = "active",
    include: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List all courses for the current user.
    
    Args:
        enrollment_state: Filter by enrollment state (active, invited_or_pending, completed, all)
        include: Additional information to include (e.g., 'term,syllabus_body,total_scores')
    """
    params = {"enrollment_state": enrollment_state}
    if include:
        params["include[]"] = include.split(",")
    
    courses = await make_canvas_request("GET", "courses", params=params)
    return courses

@mcp.tool(description="Get detailed information about a specific course including description, syllabus, and settings.")
async def get_course(course_id: int, include: Optional[str] = None) -> Dict[str, Any]:
    """
    Get details for a specific course.
    
    Args:
        course_id: The Canvas course ID
        include: Additional information to include (e.g., 'syllabus_body,term,teachers')
    """
    params = {}
    if include:
        params["include[]"] = include.split(",")
    
    course = await make_canvas_request("GET", f"courses/{course_id}", params=params)
    return course

@mcp.tool(description="Get the syllabus for a specific course.")
async def get_course_syllabus(course_id: int) -> Dict[str, Any]:
    """Get the syllabus body for a course."""
    course = await make_canvas_request("GET", f"courses/{course_id}", params={"include[]": "syllabus_body"})
    return {
        "course_id": course_id,
        "course_name": course.get("name"),
        "syllabus_body": course.get("syllabus_body", "No syllabus available")
    }

# ===== ASSIGNMENT TOOLS =====

@mcp.tool(description="List all assignments in a course with their due dates, points, and submission status.")
async def list_assignments(
    course_id: int,
    include: Optional[str] = None,
    order_by: str = "due_at"
) -> List[Dict[str, Any]]:
    """
    List all assignments in a course.
    
    Args:
        course_id: The Canvas course ID
        include: Additional information to include (e.g., 'submission,rubric,score_statistics')
        order_by: How to order assignments (due_at, name, position)
    """
    params = {"order_by": order_by}
    if include:
        params["include[]"] = include.split(",")
    
    assignments = await make_canvas_request("GET", f"courses/{course_id}/assignments", params=params)
    return assignments

@mcp.tool(description="Get detailed information about a specific assignment including description, due date, and submission requirements.")
async def get_assignment(
    course_id: int,
    assignment_id: int,
    include: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get details for a specific assignment.
    
    Args:
        course_id: The Canvas course ID
        assignment_id: The assignment ID
        include: Additional information to include (e.g., 'submission,rubric')
    """
    params = {}
    if include:
        params["include[]"] = include.split(",")
    
    assignment = await make_canvas_request("GET", f"courses/{course_id}/assignments/{assignment_id}", params=params)
    return assignment

@mcp.tool(description="Submit an assignment with text content or a URL. Use this to turn in homework.")
async def submit_assignment(
    course_id: int,
    assignment_id: int,
    submission_type: str,
    body: Optional[str] = None,
    url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Submit an assignment.
    
    Args:
        course_id: The Canvas course ID
        assignment_id: The assignment ID
        submission_type: Type of submission (online_text_entry, online_url, online_upload)
        body: Text body for text submissions
        url: URL for URL submissions
    """
    data = {
        "submission": {
            "submission_type": submission_type
        }
    }
    
    if submission_type == "online_text_entry" and body:
        data["submission"]["body"] = body
    elif submission_type == "online_url" and url:
        data["submission"]["url"] = url
    
    submission = await make_canvas_request("POST", f"courses/{course_id}/assignments/{assignment_id}/submissions", data=data)
    return submission

@mcp.tool(description="Get submission details for an assignment including grade, comments, and submitted content.")
async def get_submission(
    course_id: int,
    assignment_id: int,
    user_id: str = "self",
    include: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get submission details for an assignment.
    
    Args:
        course_id: The Canvas course ID
        assignment_id: The assignment ID
        user_id: User ID (default: 'self' for current user)
        include: Additional information to include (e.g., 'submission_comments,rubric_assessment')
    """
    params = {}
    if include:
        params["include[]"] = include.split(",")
    
    submission = await make_canvas_request("GET", f"courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}", params=params)
    return submission

# ===== MODULE TOOLS =====

@mcp.tool(description="List all modules in a course with their names, positions, and completion requirements.")
async def list_modules(course_id: int, include: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all modules in a course.
    
    Args:
        course_id: The Canvas course ID
        include: Additional information to include (e.g., 'items,content_details')
    """
    params = {}
    if include:
        params["include[]"] = include.split(",")
    
    modules = await make_canvas_request("GET", f"courses/{course_id}/modules", params=params)
    return modules

@mcp.tool(description="Get all items within a specific module including pages, assignments, quizzes, and files.")
async def get_module_items(
    course_id: int,
    module_id: int,
    include: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get items in a module.
    
    Args:
        course_id: The Canvas course ID
        module_id: The module ID
        include: Additional information to include (e.g., 'content_details')
    """
    params = {}
    if include:
        params["include[]"] = include.split(",")
    
    items = await make_canvas_request("GET", f"courses/{course_id}/modules/{module_id}/items", params=params)
    return items

@mcp.tool(description="Mark a module item as completed. This tracks your progress through course modules.")
async def mark_module_item_done(
    course_id: int,
    module_id: int,
    item_id: int
) -> Dict[str, Any]:
    """
    Mark a module item as done.
    
    Args:
        course_id: The Canvas course ID
        module_id: The module ID
        item_id: The module item ID
    """
    result = await make_canvas_request("PUT", f"courses/{course_id}/modules/{module_id}/items/{item_id}/done")
    return result

# ===== DISCUSSION TOOLS =====

@mcp.tool(description="List all discussion topics in a course including titles, authors, and reply counts.")
async def list_discussions(
    course_id: int,
    order_by: str = "position",
    scope: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List discussion topics in a course.
    
    Args:
        course_id: The Canvas course ID
        order_by: How to order discussions (position, recent_activity, title)
        scope: Filter scope (e.g., 'locked', 'unlocked', 'pinned', 'unpinned')
    """
    params = {"order_by": order_by}
    if scope:
        params["scope"] = scope
    
    discussions = await make_canvas_request("GET", f"courses/{course_id}/discussion_topics", params=params)
    return discussions

@mcp.tool(description="Get detailed information about a discussion topic including the full message and all replies.")
async def get_discussion(course_id: int, topic_id: int) -> Dict[str, Any]:
    """
    Get a specific discussion topic with full view.
    
    Args:
        course_id: The Canvas course ID
        topic_id: The discussion topic ID
    """
    discussion = await make_canvas_request("GET", f"courses/{course_id}/discussion_topics/{topic_id}/view")
    return discussion

@mcp.tool(description="Post a reply to a discussion topic. Use this to participate in class discussions.")
async def create_discussion_entry(
    course_id: int,
    topic_id: int,
    message: str,
    parent_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create an entry in a discussion topic.
    
    Args:
        course_id: The Canvas course ID
        topic_id: The discussion topic ID
        message: The message body (HTML or plain text)
        parent_id: Optional parent entry ID for replies
    """
    data = {"message": message}
    endpoint = f"courses/{course_id}/discussion_topics/{topic_id}/entries"
    
    if parent_id:
        endpoint = f"courses/{course_id}/discussion_topics/{topic_id}/entries/{parent_id}/replies"
    
    entry = await make_canvas_request("POST", endpoint, data=data)
    return entry

# ===== QUIZ TOOLS =====

@mcp.tool(description="List all quizzes in a course with their due dates, time limits, and question counts.")
async def list_quizzes(course_id: int) -> List[Dict[str, Any]]:
    """
    List all quizzes in a course.
    
    Args:
        course_id: The Canvas course ID
    """
    quizzes = await make_canvas_request("GET", f"courses/{course_id}/quizzes")
    return quizzes

@mcp.tool(description="Get detailed information about a specific quiz including instructions and settings.")
async def get_quiz(course_id: int, quiz_id: int) -> Dict[str, Any]:
    """
    Get details for a specific quiz.
    
    Args:
        course_id: The Canvas course ID
        quiz_id: The quiz ID
    """
    quiz = await make_canvas_request("GET", f"courses/{course_id}/quizzes/{quiz_id}")
    return quiz

@mcp.tool(description="Start a quiz submission. This begins a timed quiz attempt.")
async def start_quiz_submission(course_id: int, quiz_id: int) -> Dict[str, Any]:
    """
    Start a quiz submission (quiz-taking session).
    
    Args:
        course_id: The Canvas course ID
        quiz_id: The quiz ID
    """
    submission = await make_canvas_request("POST", f"courses/{course_id}/quizzes/{quiz_id}/submissions")
    return submission

@mcp.tool(description="Get questions for a quiz submission. Use this to see quiz questions during an attempt.")
async def get_quiz_questions(course_id: int, quiz_id: int, submission_id: int) -> List[Dict[str, Any]]:
    """
    Get questions for a quiz submission.
    
    Args:
        course_id: The Canvas course ID
        quiz_id: The quiz ID
        submission_id: The quiz submission ID
    """
    questions = await make_canvas_request("GET", f"courses/{course_id}/quizzes/{quiz_id}/submissions/{submission_id}/questions")
    return questions

@mcp.tool(description="Answer a quiz question. Submit your answer during a quiz attempt.")
async def answer_quiz_question(
    course_id: int,
    quiz_id: int,
    submission_id: int,
    question_id: int,
    answer: Any
) -> Dict[str, Any]:
    """
    Answer a question in a quiz submission.
    
    Args:
        course_id: The Canvas course ID
        quiz_id: The quiz ID
        submission_id: The quiz submission ID
        question_id: The question ID
        answer: The answer (format depends on question type)
    """
    data = {
        "attempt": 1,
        "validation_token": "",
        "quiz_questions": [{
            "id": question_id,
            "answer": answer
        }]
    }
    
    result = await make_canvas_request("POST", f"courses/{course_id}/quizzes/{quiz_id}/submissions/{submission_id}/questions", data=data)
    return result

@mcp.tool(description="Complete and submit a quiz. This finalizes your quiz attempt.")
async def complete_quiz_submission(
    course_id: int,
    quiz_id: int,
    submission_id: int
) -> Dict[str, Any]:
    """
    Complete (submit) a quiz submission.
    
    Args:
        course_id: The Canvas course ID
        quiz_id: The quiz ID
        submission_id: The quiz submission ID
    """
    result = await make_canvas_request("POST", f"courses/{course_id}/quizzes/{quiz_id}/submissions/{submission_id}/complete")
    return result

# ===== GRADE TOOLS =====

@mcp.tool(description="Get all grades for a specific course including current score and grade breakdown.")
async def get_course_grades(course_id: int, user_id: str = "self") -> Dict[str, Any]:
    """
    Get grades for a course.
    
    Args:
        course_id: The Canvas course ID
        user_id: User ID (default: 'self' for current user)
    """
    enrollments = await make_canvas_request("GET", f"courses/{course_id}/enrollments", params={"user_id": user_id})
    return enrollments

@mcp.tool(description="Get all assignments with their grades for the current user in a course.")
async def get_user_assignments_with_grades(course_id: int) -> List[Dict[str, Any]]:
    """
    Get all assignments with submission and grade information for current user.
    
    Args:
        course_id: The Canvas course ID
    """
    assignments = await make_canvas_request(
        "GET",
        f"courses/{course_id}/assignments",
        params={"include[]": ["submission", "score_statistics"]}
    )
    return assignments

# ===== FILE AND CONTENT TOOLS =====

@mcp.tool(description="List all files in a course including names, sizes, and download URLs.")
async def list_course_files(
    course_id: int,
    search_term: Optional[str] = None,
    content_types: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List files in a course.
    
    Args:
        course_id: The Canvas course ID
        search_term: Search for files by name
        content_types: Filter by content type (e.g., 'application/pdf,image/png')
    """
    params = {}
    if search_term:
        params["search_term"] = search_term
    if content_types:
        params["content_types[]"] = content_types.split(",")
    
    files = await make_canvas_request("GET", f"courses/{course_id}/files", params=params)
    return files

@mcp.tool(description="Get detailed information about a specific file including download URL and metadata.")
async def get_file(file_id: int) -> Dict[str, Any]:
    """
    Get details for a specific file.
    
    Args:
        file_id: The file ID
    """
    file_info = await make_canvas_request("GET", f"files/{file_id}")
    return file_info

@mcp.tool(description="List all folders in a course to browse course file organization.")
async def list_course_folders(course_id: int) -> List[Dict[str, Any]]:
    """
    List folders in a course.
    
    Args:
        course_id: The Canvas course ID
    """
    folders = await make_canvas_request("GET", f"courses/{course_id}/folders")
    return folders

# ===== ANNOUNCEMENT TOOLS =====

@mcp.tool(description="List all announcements in a course with their titles and posted dates.")
async def list_announcements(
    course_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List announcements in a course.
    
    Args:
        course_id: The Canvas course ID
        start_date: Filter announcements after this date (ISO 8601 format)
        end_date: Filter announcements before this date (ISO 8601 format)
    """
    params = {"context_codes[]": f"course_{course_id}"}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    
    announcements = await make_canvas_request("GET", "announcements", params=params)
    return announcements

# ===== CALENDAR TOOLS =====

@mcp.tool(description="List calendar events including assignments, quizzes, and other due dates.")
async def list_calendar_events(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    context_codes: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List calendar events.
    
    Args:
        start_date: Start date for events (ISO 8601 format, e.g., '2024-01-01')
        end_date: End date for events (ISO 8601 format)
        context_codes: Filter by context (e.g., 'course_123,user_456')
    """
    params = {"type": "event"}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if context_codes:
        params["context_codes[]"] = context_codes.split(",")
    
    events = await make_canvas_request("GET", "calendar_events", params=params)
    return events

@mcp.tool(description="Get detailed information about a specific calendar event.")
async def get_calendar_event(event_id: int) -> Dict[str, Any]:
    """
    Get details for a specific calendar event.
    
    Args:
        event_id: The calendar event ID
    """
    event = await make_canvas_request("GET", f"calendar_events/{event_id}")
    return event

# ===== USER PROFILE TOOLS =====

@mcp.tool(description="Get the current user's profile information including name, email, and avatar.")
async def get_user_profile() -> Dict[str, Any]:
    """Get the current user's profile."""
    profile = await make_canvas_request("GET", "users/self/profile")
    return profile

@mcp.tool(description="Get all course enrollments for the current user including role and enrollment state.")
async def get_user_enrollments() -> List[Dict[str, Any]]:
    """Get enrollments for the current user."""
    enrollments = await make_canvas_request("GET", "users/self/enrollments")
    return enrollments

@mcp.tool(description="Get upcoming assignments and events across all courses for the current user.")
async def get_upcoming_assignments() -> List[Dict[str, Any]]:
    """Get upcoming assignments for the current user."""
    upcoming = await make_canvas_request("GET", "users/self/upcoming_events")
    return upcoming

@mcp.tool(description="Get recent activity and notifications for the current user.")
async def get_user_activity_stream() -> List[Dict[str, Any]]:
    """Get the activity stream for the current user."""
    stream = await make_canvas_request("GET", "users/self/activity_stream")
    return stream

# ===== PAGE TOOLS =====

@mcp.tool(description="List all pages in a course including titles and URLs.")
async def list_pages(
    course_id: int,
    sort: str = "title",
    order: str = "asc"
) -> List[Dict[str, Any]]:
    """
    List pages in a course.
    
    Args:
        course_id: The Canvas course ID
        sort: Sort by (title, created_at, updated_at)
        order: Sort order (asc, desc)
    """
    params = {"sort": sort, "order": order}
    pages = await make_canvas_request("GET", f"courses/{course_id}/pages", params=params)
    return pages

@mcp.tool(description="Get the content of a specific page in a course.")
async def get_page(course_id: int, page_url: str) -> Dict[str, Any]:
    """
    Get a specific page.
    
    Args:
        course_id: The Canvas course ID
        page_url: The page URL or ID
    """
    page = await make_canvas_request("GET", f"courses/{course_id}/pages/{page_url}")
    return page

# ===== GROUP TOOLS =====

@mcp.tool(description="List all groups the current user is a member of.")
async def list_user_groups() -> List[Dict[str, Any]]:
    """List groups for the current user."""
    groups = await make_canvas_request("GET", "users/self/groups")
    return groups

@mcp.tool(description="Get details about a specific group including members and description.")
async def get_group(group_id: int, include: Optional[str] = None) -> Dict[str, Any]:
    """
    Get details for a specific group.
    
    Args:
        group_id: The group ID
        include: Additional information to include (e.g., 'users,tabs')
    """
    params = {}
    if include:
        params["include[]"] = include.split(",")
    
    group = await make_canvas_request("GET", f"groups/{group_id}", params=params)
    return group

# ===== TODO ITEMS =====

@mcp.tool(description="Get all to-do items for the current user including assignments and other tasks.")
async def get_todo_items() -> List[Dict[str, Any]]:
    """Get to-do items for the current user."""
    todos = await make_canvas_request("GET", "users/self/todo")
    return todos

# ===== CONVERSATION TOOLS =====

@mcp.tool(description="List all conversations (messages) for the current user.")
async def list_conversations(scope: str = "inbox") -> List[Dict[str, Any]]:
    """
    List conversations for the current user.
    
    Args:
        scope: Filter by scope (inbox, unread, starred, sent, archived, all)
    """
    params = {"scope": scope}
    conversations = await make_canvas_request("GET", "conversations", params=params)
    return conversations

@mcp.tool(description="Get details about a specific conversation including all messages.")
async def get_conversation(conversation_id: int) -> Dict[str, Any]:
    """
    Get a specific conversation.
    
    Args:
        conversation_id: The conversation ID
    """
    conversation = await make_canvas_request("GET", f"conversations/{conversation_id}")
    return conversation

@mcp.tool(description="Send a message to other users in Canvas.")
async def create_conversation(
    recipients: str,
    subject: str,
    body: str,
    context_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new conversation (send a message).
    
    Args:
        recipients: Comma-separated list of recipient IDs (e.g., '123,456')
        subject: Message subject
        body: Message body
        context_code: Optional context (e.g., 'course_123')
    """
    data = {
        "recipients[]": recipients.split(","),
        "subject": subject,
        "body": body
    }
    if context_code:
        data["context_code"] = context_code
    
    conversation = await make_canvas_request("POST", "conversations", data=data)
    return conversation

# ===== RUBRIC TOOLS =====

@mcp.tool(description="Get the rubric for an assignment to understand grading criteria.")
async def get_assignment_rubric(course_id: int, assignment_id: int) -> Dict[str, Any]:
    """
    Get the rubric for an assignment.
    
    Args:
        course_id: The Canvas course ID
        assignment_id: The assignment ID
    """
    assignment = await make_canvas_request(
        "GET",
        f"courses/{course_id}/assignments/{assignment_id}",
        params={"include[]": ["rubric", "rubric_assessment"]}
    )
    return {
        "assignment_id": assignment_id,
        "assignment_name": assignment.get("name"),
        "rubric": assignment.get("rubric"),
        "rubric_settings": assignment.get("rubric_settings")
    }

# ===== OUTCOME TOOLS =====

@mcp.tool(description="List learning outcomes for a course.")
async def list_course_outcomes(course_id: int) -> List[Dict[str, Any]]:
    """
    List outcomes for a course.
    
    Args:
        course_id: The Canvas course ID
    """
    outcomes = await make_canvas_request("GET", f"courses/{course_id}/outcome_group_links")
    return outcomes

# ===== SERVER INFO =====

@mcp.tool(description="Get information about this Canvas MCP server including version and configuration.")
def get_server_info() -> dict:
    """Get information about the Canvas MCP server."""
    return {
        "server_name": "Canvas LMS MCP Server",
        "version": "1.0.0",
        "description": "Model Context Protocol server for Canvas LMS (Student perspective)",
        "canvas_api_url": CANVAS_API_URL,
        "api_token_configured": bool(CANVAS_API_TOKEN),
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting Canvas LMS MCP Server on {host}:{port}")
    print(f"Canvas API URL: {CANVAS_API_URL}")
    print(f"API Token configured: {bool(CANVAS_API_TOKEN)}")
    
    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )
