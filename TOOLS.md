# Canvas MCP Server - Complete Tool Reference

This document lists all 42 tools available in the Canvas MCP Server.

## Course Management (7 tools)

### list_courses
List all courses the current user is enrolled in. Returns course ID, name, course code, enrollment status, and term.

**Parameters:**
- `enrollment_state` (str): Filter by enrollment state (active, invited_or_pending, completed, all)
- `include` (str, optional): Additional information to include (e.g., 'term,syllabus_body,total_scores')

### get_course
Get detailed information about a specific course including description, syllabus, and settings.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `include` (str, optional): Additional information to include (e.g., 'syllabus_body,term,teachers')

### get_course_syllabus
Get the syllabus for a specific course.

**Parameters:**
- `course_id` (int): The Canvas course ID

### get_course_grades
Get all grades for a specific course including current score and grade breakdown.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `user_id` (str): User ID (default: 'self' for current user)

### list_course_files
List all files in a course including names, sizes, and download URLs.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `search_term` (str, optional): Search for files by name
- `content_types` (str, optional): Filter by content type (e.g., 'application/pdf,image/png')

### list_course_folders
List all folders in a course to browse course file organization.

**Parameters:**
- `course_id` (int): The Canvas course ID

### list_course_outcomes
List learning outcomes for a course.

**Parameters:**
- `course_id` (int): The Canvas course ID

## Assignments (6 tools)

### list_assignments
List all assignments in a course with their due dates, points, and submission status.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `include` (str, optional): Additional information to include (e.g., 'submission,rubric,score_statistics')
- `order_by` (str): How to order assignments (due_at, name, position)

### get_assignment
Get detailed information about a specific assignment including description, due date, and submission requirements.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `assignment_id` (int): The assignment ID
- `include` (str, optional): Additional information to include (e.g., 'submission,rubric')

### submit_assignment
Submit an assignment with text content or a URL. Use this to turn in homework.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `assignment_id` (int): The assignment ID
- `submission_type` (str): Type of submission (online_text_entry, online_url, online_upload)
- `body` (str, optional): Text body for text submissions
- `url` (str, optional): URL for URL submissions

### get_submission
Get submission details for an assignment including grade, comments, and submitted content.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `assignment_id` (int): The assignment ID
- `user_id` (str): User ID (default: 'self' for current user)
- `include` (str, optional): Additional information to include (e.g., 'submission_comments,rubric_assessment')

### get_user_assignments_with_grades
Get all assignments with their grades for the current user in a course.

**Parameters:**
- `course_id` (int): The Canvas course ID

### get_assignment_rubric
Get the rubric for an assignment to understand grading criteria.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `assignment_id` (int): The assignment ID

## Modules (3 tools)

### list_modules
List all modules in a course with their names, positions, and completion requirements.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `include` (str, optional): Additional information to include (e.g., 'items,content_details')

### get_module_items
Get all items within a specific module including pages, assignments, quizzes, and files.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `module_id` (int): The module ID
- `include` (str, optional): Additional information to include (e.g., 'content_details')

### mark_module_item_done
Mark a module item as completed. This tracks your progress through course modules.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `module_id` (int): The module ID
- `item_id` (int): The module item ID

## Discussions (3 tools)

### list_discussions
List all discussion topics in a course including titles, authors, and reply counts.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `order_by` (str): How to order discussions (position, recent_activity, title)
- `scope` (str, optional): Filter scope (e.g., 'locked', 'unlocked', 'pinned', 'unpinned')

### get_discussion
Get detailed information about a discussion topic including the full message and all replies.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `topic_id` (int): The discussion topic ID

### create_discussion_entry
Post a reply to a discussion topic. Use this to participate in class discussions.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `topic_id` (int): The discussion topic ID
- `message` (str): The message body (HTML or plain text)
- `parent_id` (int, optional): Optional parent entry ID for replies

## Quizzes (6 tools)

### list_quizzes
List all quizzes in a course with their due dates, time limits, and question counts.

**Parameters:**
- `course_id` (int): The Canvas course ID

### get_quiz
Get detailed information about a specific quiz including instructions and settings.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `quiz_id` (int): The quiz ID

### start_quiz_submission
Start a quiz submission. This begins a timed quiz attempt.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `quiz_id` (int): The quiz ID

### get_quiz_questions
Get questions for a quiz submission. Use this to see quiz questions during an attempt.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `quiz_id` (int): The quiz ID
- `submission_id` (int): The quiz submission ID

### answer_quiz_question
Answer a quiz question. Submit your answer during a quiz attempt.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `quiz_id` (int): The quiz ID
- `submission_id` (int): The quiz submission ID
- `question_id` (int): The question ID
- `answer` (Any): The answer (format depends on question type)

### complete_quiz_submission
Complete and submit a quiz. This finalizes your quiz attempt.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `quiz_id` (int): The quiz ID
- `submission_id` (int): The quiz submission ID

## Pages (2 tools)

### list_pages
List all pages in a course including titles and URLs.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `sort` (str): Sort by (title, created_at, updated_at)
- `order` (str): Sort order (asc, desc)

### get_page
Get the content of a specific page in a course.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `page_url` (str): The page URL or ID

## Files (2 tools)

### get_file
Get detailed information about a specific file including download URL and metadata.

**Parameters:**
- `file_id` (int): The file ID

## Announcements (1 tool)

### list_announcements
List all announcements in a course with their titles and posted dates.

**Parameters:**
- `course_id` (int): The Canvas course ID
- `start_date` (str, optional): Filter announcements after this date (ISO 8601 format)
- `end_date` (str, optional): Filter announcements before this date (ISO 8601 format)

## Calendar (2 tools)

### list_calendar_events
List calendar events including assignments, quizzes, and other due dates.

**Parameters:**
- `start_date` (str, optional): Start date for events (ISO 8601 format, e.g., '2024-01-01')
- `end_date` (str, optional): End date for events (ISO 8601 format)
- `context_codes` (str, optional): Filter by context (e.g., 'course_123,user_456')

### get_calendar_event
Get detailed information about a specific calendar event.

**Parameters:**
- `event_id` (int): The calendar event ID

## User Profile (5 tools)

### get_user_profile
Get the current user's profile information including name, email, and avatar.

### get_user_enrollments
Get all course enrollments for the current user including role and enrollment state.

### get_upcoming_assignments
Get upcoming assignments and events across all courses for the current user.

### get_user_activity_stream
Get recent activity and notifications for the current user.

### get_todo_items
Get all to-do items for the current user including assignments and other tasks.

## Groups (2 tools)

### list_user_groups
List all groups the current user is a member of.

### get_group
Get details about a specific group including members and description.

**Parameters:**
- `group_id` (int): The group ID
- `include` (str, optional): Additional information to include (e.g., 'users,tabs')

## Conversations (3 tools)

### list_conversations
List all conversations (messages) for the current user.

**Parameters:**
- `scope` (str): Filter by scope (inbox, unread, starred, sent, archived, all)

### get_conversation
Get details about a specific conversation including all messages.

**Parameters:**
- `conversation_id` (int): The conversation ID

### create_conversation
Send a message to other users in Canvas.

**Parameters:**
- `recipients` (str): Comma-separated list of recipient IDs (e.g., '123,456')
- `subject` (str): Message subject
- `body` (str): Message body
- `context_code` (str, optional): Optional context (e.g., 'course_123')

## Server Info (1 tool)

### get_server_info
Get information about this Canvas MCP server including version and configuration.

---

## Total: 42 Tools

All tools implement the Canvas LMS REST API from a student perspective and follow Canvas API conventions.
