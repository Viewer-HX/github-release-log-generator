from crewai import Task
from typing import Dict, Any

def create_github_analysis_task(agent, repository: str, from_commit: str, to_commit: str):
    """Create task for GitHub repository analysis"""
    return Task(
        description=f"""
        Analyze the GitHub repository '{repository}' and extract detailed information about 
        changes between commits '{from_commit}' and '{to_commit}'.
        
        Your analysis should include:
        1. Repository basic information (name, description, language)
        2. Detailed file changes (additions, deletions, modifications)
        3. Summary of overall changes
        4. List of affected files and their change types
        
        Use the available tools to fetch this information from GitHub and provide a comprehensive
        analysis that will be used by other agents for further processing.
        
        Repository: {repository}
        From Commit: {from_commit}
        To Commit: {to_commit}
        """,
        agent=agent,
        expected_output="""
        A detailed JSON-formatted analysis containing:
        - Repository information
        - Commit comparison results
        - File changes with statistics
        - Summary of changes
        """
    )

def create_code_analysis_task(agent, github_analysis_result: str):
    """Create task for code change analysis"""
    return Task(
        description=f"""
        Analyze the code changes provided from the GitHub analysis and categorize them into:
        
        1. **New Features**: New functionality, new files, new capabilities
        2. **Bug Fixes**: Fixes to existing issues, error corrections, patches
        3. **Breaking Changes**: Changes that might break existing functionality
        4. **Improvements**: Performance improvements, refactoring, optimizations
        5. **Documentation**: Documentation updates, README changes, comment updates
        6. **Dependencies**: Package updates, dependency changes
        
        Based on this GitHub analysis:
        {github_analysis_result}
        
        For each category, provide:
        - A clear description of what changed
        - The impact of the change
        - Which files were affected
        
        Focus on understanding the purpose and impact of each change rather than just listing files.
        """,
        agent=agent,
        expected_output="""
        A structured analysis with:
        - Categorized changes (features, bug fixes, breaking changes, etc.)
        - Impact assessment for each change
        - Technical details about modifications
        - Recommended version bump (major/minor/patch)
        """
    )

def create_release_log_task(agent, code_analysis_result: str, repository: str):
    """Create task for release log generation"""
    return Task(
        description=f"""
        Generate a comprehensive release log based on the code analysis provided.
        
        The release log should be professional, well-formatted, and include:
        
        1. **Release Header**: Version, date, repository name
        2. **Summary**: Brief overview of the release
        3. **New Features**: List of new functionality
        4. **Bug Fixes**: List of issues resolved
        5. **Breaking Changes**: Important changes that might affect users
        6. **Improvements**: Performance and other improvements
        7. **Technical Details**: Additional technical information
        
        Based on this code analysis:
        {code_analysis_result}
        
        Repository: {repository}
        
        Format the release log in a clear, professional manner that would be suitable
        for sending to stakeholders, users, or team members. Use markdown formatting
        for better readability.
        """,
        agent=agent,
        expected_output="""
        A well-formatted release log in markdown format containing:
        - Professional header with version and date
        - Executive summary
        - Categorized changes
        - Technical details
        - Clear, user-friendly language
        """
    )

def create_email_sending_task(agent, release_log: str, recipient_email: str, repository: str):
    """Create task for sending email notification"""
    return Task(
        description=f"""
        Create and send a professional email notification containing the release log.
        
        Email details:
        - Recipient: {recipient_email}
        - Subject: Release Log for {repository}
        - Body: Professional email with the release log
        
        The email should:
        1. Have a professional and engaging subject line
        2. Include a brief introduction
        3. Present the release log in a clear format
        4. Include a professional closing
        5. Be formatted for HTML email if possible
        
        Release log to include:
        {release_log}
        
        Repository: {repository}
        Recipient: {recipient_email}
        
        Make sure the email is professional, informative, and easy to read.
        """,
        agent=agent,
        expected_output="""
        Confirmation that the email has been successfully formatted and sent, including:
        - Email subject used
        - Recipient confirmation
        - Summary of email content
        - Send status
        """
    )
