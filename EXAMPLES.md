# Canvas MCP Server - Usage Examples

This document provides practical examples of using the Canvas MCP Server tools.

## Setup

Before using any tools, ensure you have:

1. Set the `CANVAS_API_URL` environment variable (e.g., `https://canvas.instructure.com/api/v1`)
2. Set the `CANVAS_API_TOKEN` environment variable with your Canvas API token

## Common Use Cases

### 1. Getting Started - View Your Courses

```python
# List all your active courses
list_courses(enrollment_state="active")

# Get detailed information about a specific course
get_course(course_id=12345, include="syllabus_body,term,teachers")

# View the syllabus
get_course_syllabus(course_id=12345)
```

### 2. Working with Assignments

```python
# List all assignments in a course with submission status
list_assignments(course_id=12345, include="submission", order_by="due_at")

# Get details about a specific assignment
get_assignment(course_id=12345, assignment_id=67890, include="submission,rubric")

# View the grading rubric
get_assignment_rubric(course_id=12345, assignment_id=67890)

# Submit a text assignment
submit_assignment(
    course_id=12345,
    assignment_id=67890,
    submission_type="online_text_entry",
    body="<p>My assignment submission...</p>"
)

# Submit a URL assignment
submit_assignment(
    course_id=12345,
    assignment_id=67890,
    submission_type="online_url",
    url="https://example.com/my-project"
)

# Check your submission and grade
get_submission(
    course_id=12345,
    assignment_id=67890,
    user_id="self",
    include="submission_comments,rubric_assessment"
)
```

### 3. Participating in Discussions

```python
# List all discussion topics in a course
list_discussions(course_id=12345, order_by="recent_activity")

# Read a specific discussion with all replies
get_discussion(course_id=12345, topic_id=54321)

# Post a new discussion entry
create_discussion_entry(
    course_id=12345,
    topic_id=54321,
    message="Great point! I think that..."
)

# Reply to a specific discussion entry
create_discussion_entry(
    course_id=12345,
    topic_id=54321,
    message="I agree with your perspective because...",
    parent_id=98765
)
```

### 4. Taking Quizzes

```python
# List all quizzes in a course
list_quizzes(course_id=12345)

# Get quiz details
get_quiz(course_id=12345, quiz_id=11111)

# Start a quiz attempt
submission = start_quiz_submission(course_id=12345, quiz_id=11111)
submission_id = submission['id']

# Get the quiz questions
questions = get_quiz_questions(
    course_id=12345,
    quiz_id=11111,
    submission_id=submission_id
)

# Answer a question
answer_quiz_question(
    course_id=12345,
    quiz_id=11111,
    submission_id=submission_id,
    question_id=22222,
    answer="The answer text"
)

# Complete and submit the quiz
complete_quiz_submission(
    course_id=12345,
    quiz_id=11111,
    submission_id=submission_id
)
```

### 5. Tracking Progress in Modules

```python
# List all modules in a course
list_modules(course_id=12345, include="items")

# Get items in a specific module
get_module_items(course_id=12345, module_id=33333, include="content_details")

# Mark a module item as completed
mark_module_item_done(
    course_id=12345,
    module_id=33333,
    item_id=44444
)
```

### 6. Checking Grades and Progress

```python
# Get your overall grade for a course
get_course_grades(course_id=12345, user_id="self")

# Get all assignments with grades
get_user_assignments_with_grades(course_id=12345)

# View course outcomes and learning objectives
list_course_outcomes(course_id=12345)
```

### 7. Managing Files and Content

```python
# List all files in a course
list_course_files(course_id=12345)

# Search for specific files
list_course_files(course_id=12345, search_term="syllabus")

# Filter files by type
list_course_files(
    course_id=12345,
    content_types="application/pdf,image/png"
)

# Get file details and download URL
get_file(file_id=55555)

# Browse folder structure
list_course_folders(course_id=12345)

# List course pages
list_pages(course_id=12345, sort="title", order="asc")

# Read a specific page
get_page(course_id=12345, page_url="introduction")
```

### 8. Staying Organized

```python
# View upcoming assignments across all courses
get_upcoming_assignments()

# Get your to-do list
get_todo_items()

# View calendar events for a date range
list_calendar_events(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# Filter calendar events by course
list_calendar_events(
    start_date="2024-01-01",
    end_date="2024-01-31",
    context_codes="course_12345"
)

# Get details about a specific event
get_calendar_event(event_id=66666)
```

### 9. Checking Announcements

```python
# List all announcements for a course
list_announcements(course_id=12345)

# Filter announcements by date range
list_announcements(
    course_id=12345,
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

### 10. Working with Groups

```python
# List all your groups
list_user_groups()

# Get details about a specific group
get_group(group_id=77777, include="users")
```

### 11. Sending Messages

```python
# List your messages
list_conversations(scope="inbox")

# View unread messages
list_conversations(scope="unread")

# Read a specific conversation
get_conversation(conversation_id=88888)

# Send a new message
create_conversation(
    recipients="123,456",  # User IDs
    subject="Project collaboration",
    body="Hi! Let's discuss our group project...",
    context_code="course_12345"
)
```

### 12. Viewing Your Profile and Activity

```python
# Get your profile information
get_user_profile()

# View all your course enrollments
get_user_enrollments()

# Check recent activity and notifications
get_user_activity_stream()
```

## Advanced Examples

### Study Planning Assistant

```python
# Get a comprehensive view of your workload
courses = list_courses(enrollment_state="active")

for course in courses:
    course_id = course['id']
    print(f"Course: {course['name']}")
    
    # Get upcoming assignments
    assignments = list_assignments(
        course_id=course_id,
        include="submission",
        order_by="due_at"
    )
    
    # Get current grade
    grades = get_course_grades(course_id=course_id)
    
    print(f"  Grade: {grades[0].get('grades', {}).get('current_score', 'N/A')}")
    print(f"  Assignments: {len(assignments)}")
```

### Assignment Submission Workflow

```python
# Complete workflow for submitting an assignment
course_id = 12345
assignment_id = 67890

# 1. Get assignment details and requirements
assignment = get_assignment(
    course_id=course_id,
    assignment_id=assignment_id,
    include="rubric"
)

print(f"Assignment: {assignment['name']}")
print(f"Due: {assignment['due_at']}")
print(f"Points: {assignment['points_possible']}")

# 2. View the rubric if available
rubric = get_assignment_rubric(course_id=course_id, assignment_id=assignment_id)

# 3. Submit your work
submit_assignment(
    course_id=course_id,
    assignment_id=assignment_id,
    submission_type="online_text_entry",
    body="<p>My completed assignment...</p>"
)

# 4. Confirm submission
submission = get_submission(
    course_id=course_id,
    assignment_id=assignment_id,
    include="submission_comments"
)

print(f"Submitted at: {submission['submitted_at']}")
```

### Discussion Participation

```python
# Comprehensive discussion workflow
course_id = 12345
topic_id = 54321

# 1. Read the discussion topic
discussion = get_discussion(course_id=course_id, topic_id=topic_id)
print(f"Topic: {discussion['title']}")
print(f"Replies: {discussion['discussion_subentry_count']}")

# 2. Post your response
create_discussion_entry(
    course_id=course_id,
    topic_id=topic_id,
    message="Here's my perspective on this topic..."
)
```

## Tips and Best Practices

1. **Check Due Dates**: Use `get_upcoming_assignments()` and `list_calendar_events()` to stay on top of deadlines

2. **Track Progress**: Use `mark_module_item_done()` to track your progress through course materials

3. **Use Include Parameters**: Many tools support an `include` parameter to get additional data in a single request

4. **Handle Pagination**: For large result sets, use pagination parameters if available

5. **Error Handling**: Always check for errors in responses, especially with API token authentication

6. **Rate Limiting**: Be mindful of Canvas API rate limits when making many requests

## Getting Help

- Review the [TOOLS.md](TOOLS.md) file for complete tool documentation
- Check the [Canvas API Documentation](https://canvas.instructure.com/doc/api/) for detailed API information
- Use `get_server_info()` to verify your server configuration

## Example AI Assistant Prompts

Here are some example prompts you can use with AI assistants that have access to this MCP server:

- "Show me all my active courses and their current grades"
- "What assignments are due this week?"
- "Help me submit my essay for assignment 12345 in course 67890"
- "Read the latest discussion posts in my Biology class and help me write a thoughtful response"
- "Show me my to-do list and upcoming calendar events"
- "Check if I have any unread messages in Canvas"
- "What's on the syllabus for my Math course?"
- "Help me track my progress through the course modules"
