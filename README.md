# Canvas LMS MCP Server

A comprehensive [FastMCP](https://github.com/jlowin/fastmcp) server for Canvas LMS integration, providing AI assistants with full access to Canvas functionality from a student perspective.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/443pablo/mcp-canvas)

## Overview

This MCP (Model Context Protocol) server enables AI assistants to interact with Canvas LMS on behalf of students. It provides 50+ tools covering all major Canvas features including courses, assignments, discussions, quizzes, grades, files, and more.

## Features

### Course Management
- **list_courses** - List all enrolled courses
- **get_course** - Get detailed course information
- **get_course_syllabus** - View course syllabus

### Assignments
- **list_assignments** - List all assignments in a course
- **get_assignment** - Get assignment details
- **submit_assignment** - Submit assignments (text, URL, or file)
- **get_submission** - View submission status and grades
- **get_assignment_rubric** - View grading rubrics

### Modules
- **list_modules** - List course modules
- **get_module_items** - Get items in a module
- **mark_module_item_done** - Track module progress

### Discussions
- **list_discussions** - List discussion topics
- **get_discussion** - View discussion threads
- **create_discussion_entry** - Post and reply to discussions

### Quizzes
- **list_quizzes** - List all quizzes
- **get_quiz** - Get quiz details
- **start_quiz_submission** - Begin a quiz attempt
- **get_quiz_questions** - View quiz questions
- **answer_quiz_question** - Submit quiz answers
- **complete_quiz_submission** - Finalize quiz submission

### Grades
- **get_course_grades** - View course grades
- **get_user_assignments_with_grades** - See all graded assignments

### Files & Content
- **list_course_files** - Browse course files
- **get_file** - Get file details and download URLs
- **list_course_folders** - View folder structure
- **list_pages** - List course pages
- **get_page** - View page content

### Calendar & Tasks
- **list_calendar_events** - View calendar events
- **get_calendar_event** - Get event details
- **get_upcoming_assignments** - See upcoming due dates
- **get_todo_items** - View to-do list

### Announcements
- **list_announcements** - View course announcements

### Communication
- **list_conversations** - View messages
- **get_conversation** - Read conversation details
- **create_conversation** - Send messages

### Profile & Groups
- **get_user_profile** - View user profile
- **get_user_enrollments** - List enrollments
- **get_user_activity_stream** - View recent activity
- **list_user_groups** - List groups
- **get_group** - Get group details

### Learning Outcomes
- **list_course_outcomes** - View course learning outcomes

## Prerequisites

- Python 3.13 or higher
- Canvas LMS account
- Canvas API token

## Getting Your Canvas API Token

1. Log into your Canvas account
2. Go to Account → Settings
3. Scroll down to "Approved Integrations"
4. Click "+ New Access Token"
5. Enter a purpose (e.g., "MCP Server")
6. Set an expiration date (optional)
7. Click "Generate Token"
8. Copy the token immediately (you won't see it again!)

## Local Development

### Setup

Fork the repo, then run:

```bash
git clone <your-repo-url>
cd mcp-canvas
conda create -n mcp-canvas python=3.13
conda activate mcp-canvas
pip install -r requirements.txt
```

### Configuration

Set up your environment variables:

```bash
export CANVAS_API_URL="https://your-institution.instructure.com/api/v1"
export CANVAS_API_TOKEN="your_token_here"
```

Or create a `.env` file (don't commit this!):

```
CANVAS_API_URL=https://your-institution.instructure.com/api/v1
CANVAS_API_TOKEN=your_token_here
```

**Note:** Replace `your-institution.instructure.com` with your Canvas instance URL (e.g., `canvas.harvard.edu`, `canvas.stanford.edu`, or just `canvas.instructure.com` for free accounts).

### Test

```bash
python src/server.py
# then in another terminal run:
npx @modelcontextprotocol/inspector
```

Open http://localhost:3000 and connect to `http://localhost:8000/mcp` using "Streamable HTTP" transport (NOTE THE `/mcp`!).

### Example Usage

Once connected, you can test tools like:

```
# List all your courses
list_courses(enrollment_state="active")

# Get assignments for a course
list_assignments(course_id=12345, include="submission")

# View your grades
get_course_grades(course_id=12345)

# Submit an assignment
submit_assignment(
    course_id=12345,
    assignment_id=67890,
    submission_type="online_text_entry",
    body="My assignment submission..."
)

# Post to a discussion
create_discussion_entry(
    course_id=12345,
    topic_id=54321,
    message="Great point! I think..."
)
```

## Deployment

### Option 1: One-Click Deploy to Render

Click the "Deploy to Render" button above, then:

1. Set the `CANVAS_API_URL` environment variable
2. Set the `CANVAS_API_TOKEN` environment variable
3. Click "Apply"

Your server will be available at `https://your-service-name.onrender.com/mcp` (NOTE THE `/mcp`!)

### Option 2: Manual Deployment to Render

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service on Render
4. Connect your forked repository
5. Add environment variables:
   - `CANVAS_API_URL` - Your Canvas API URL
   - `CANVAS_API_TOKEN` - Your Canvas API token
   - `ENVIRONMENT` - Set to `production`
6. Render will automatically detect the `render.yaml` configuration

### Option 3: Deploy to Other Platforms

The server can be deployed to any platform that supports Python web applications:

**Heroku:**
```bash
heroku create your-canvas-mcp
heroku config:set CANVAS_API_URL="https://your-canvas-url/api/v1"
heroku config:set CANVAS_API_TOKEN="your_token"
git push heroku main
```

**Railway:**
1. Connect your GitHub repo
2. Add environment variables in settings
3. Deploy

**Fly.io:**
```bash
fly launch
fly secrets set CANVAS_API_URL="https://your-canvas-url/api/v1"
fly secrets set CANVAS_API_TOKEN="your_token"
fly deploy
```

## Integration with AI Assistants

### Claude Desktop

Add to your Claude Desktop config file:

**MacOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "canvas": {
      "url": "https://your-server.onrender.com/mcp",
      "transport": "http"
    }
  }
}
```

### Poke

You can connect your MCP server to Poke at [poke.com/settings/connections](https://poke.com/settings/connections).

To test the connection explicitly, ask Poke something like: 
`Tell the subagent to use the "canvas" integration's "list_courses" tool`.

If you run into persistent issues of Poke not calling the right MCP (e.g., after you've renamed the connection), send `clearhistory` to Poke to delete all message history and start fresh.

### Other MCP Clients

This server implements the standard MCP protocol over HTTP, so it works with any MCP-compatible client. Configure it with:
- URL: `https://your-server-url/mcp`
- Transport: HTTP (Streamable)

## Use Cases

This MCP server enables AI assistants to help students with:

- **Course Management**: View courses, syllabi, and course materials
- **Assignment Help**: Check due dates, view requirements, submit work
- **Study Planning**: Track upcoming assignments and create study schedules
- **Discussion Participation**: Read and respond to class discussions
- **Grade Tracking**: Monitor grades and academic progress
- **Quiz Preparation**: Review quiz details and time limits
- **File Access**: Find and access course files and resources
- **Communication**: Send messages to instructors and classmates
- **Calendar Management**: View and organize academic calendar
- **Group Work**: Access group information and collaborate

## API Coverage

This server implements the Canvas LMS REST API from a student perspective, based on the official [Canvas API Documentation](https://canvas.instructure.com/doc/api/). It covers:

- ✅ Courses API
- ✅ Assignments API
- ✅ Submissions API
- ✅ Modules API
- ✅ Discussion Topics API
- ✅ Quizzes API
- ✅ Files API
- ✅ Pages API
- ✅ Announcements API
- ✅ Calendar Events API
- ✅ Users API
- ✅ Enrollments API
- ✅ Groups API
- ✅ Conversations API
- ✅ Rubrics API
- ✅ Outcomes API
- ✅ To-Do Items API

## Security Considerations

- **Never commit your Canvas API token** to version control
- Store tokens in environment variables or secure secret management
- Use token expiration dates to limit exposure
- Rotate tokens periodically
- Be cautious when sharing your deployed server URL
- Consider implementing additional authentication for production use
- Review Canvas API rate limits and implement appropriate throttling

## Troubleshooting

### "CANVAS_API_TOKEN environment variable is not set"
Make sure you've set the `CANVAS_API_TOKEN` environment variable with your Canvas API token.

### "Unauthorized" or 401 errors
- Check that your API token is valid and hasn't expired
- Verify you have the correct permissions in Canvas
- Ensure the token has been properly set in your environment

### "Not Found" or 404 errors
- Verify the Canvas API URL is correct for your institution
- Check that course IDs, assignment IDs, etc. are valid
- Ensure you're enrolled in the course you're trying to access

### Connection errors
- Verify your Canvas instance URL is accessible
- Check network connectivity
- Confirm the API endpoint paths are correct

## Development

### Adding New Tools

To add new Canvas API endpoints:

```python
@mcp.tool(description="Your tool description here")
async def your_tool_name(param1: type1, param2: type2) -> ReturnType:
    """
    Detailed documentation.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    """
    result = await make_canvas_request("GET", "endpoint/path", params={...})
    return result
```

### Testing

Test individual tools using the MCP Inspector or by making requests directly to your running server.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Resources

- [Canvas API Documentation](https://canvas.instructure.com/doc/api/)
- [Canvas API Live](https://canvas.instructure.com/doc/api/live) - Interactive API explorer
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/443pablo/mcp-canvas/issues)
- Canvas API Support: [Canvas Community](https://community.canvaslms.com/)

## Acknowledgments

Built with [FastMCP](https://github.com/jlowin/fastmcp) by [Marvin AI](https://www.askmarvin.ai/)

---

**Note:** This is an unofficial Canvas integration. It is not affiliated with, endorsed by, or supported by Instructure, Inc.
